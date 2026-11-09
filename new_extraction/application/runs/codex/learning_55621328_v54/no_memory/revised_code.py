# %%
%%writefile predict_exp302.py
import json
from pathlib import Path
import sys
sys.path.append("/kaggle/input/omegaconf")
sys.path.append("/kaggle/input/aes2-code/kaggle-aes2-v0/kaggle-aes2-v0")
from argparse import ArgumentParser

import datasets
import torch
import torch.utils.data
import numpy as np
import pandas as pd
from datasets import Dataset
from omegaconf import OmegaConf
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AddedToken

from aes2.utils.collators.sequence_bucket import SequenceBucketPadCollator
from aes2.utils.dataset.simple import CompetitionDataset
from aes2.utils.metrics import OptimizedRounder

parser = ArgumentParser()
parser.add_argument("--config", default=None, required=False)
parser.add_argument("--checkpoints", type=str)
parser.add_argument("--save-name", type=str)
parser.add_argument("--weights", type=str)
parser.add_argument("--calibration-dir", type=str, default=None)

args, unknown_args = parser.parse_known_args()


def tokenize(example, tokenizer, max_length=1024):
    full_text = example["full_text"]
    truncation = True
    encoding = tokenizer(full_text, return_token_type_ids=False, truncation=truncation, max_length=max_length)

    return {
        "input_ids": encoding["input_ids"],
        "attention_mask": encoding["attention_mask"]
    }


def loc_datasets(ds, keep_columns):
    return Dataset.from_dict({col: ds[col] for col in keep_columns})



@torch.no_grad()
def inference(model, dataloader):
    predictions = []
    model.eval()
    for x in tqdm(dataloader, total=len(dataloader)):
        predictions.append(model({key: x[key].to("cuda") for key in x}).cpu().numpy())
    return np.concatenate(predictions, axis=0)



def validation_thresholds(checkpoints, initial):
    """Calibrate using saved held-out predictions, never test labels.

    Select the shrinkage strength by stratified cross-validation. An artifact
    must be from this exact experiment, identify essays, and match train labels.
    No checkpoint is run on training essays to manufacture calibration data.
    """
    from scipy.optimize import minimize
    from sklearn.metrics import cohen_kappa_score
    from sklearn.model_selection import StratifiedKFold
    import re

    initial = np.asarray(initial, dtype=float)
    if initial.shape != (5,) or not np.all(np.diff(initial) > 0):
        raise ValueError("Expected five strictly increasing score thresholds")
    root = Path(args.calibration_dir or Path(args.config).parent)
    train = pd.read_csv(
        "/kaggle/input/learning-agency-lab-automated-essay-scoring-2/train.csv",
        usecols=["essay_id", "score"],
    )
    pieces = []
    # A fold-specific artifact must correspond to a selected checkpoint.
    fold_ids = [re.search(r"model_fold(\d+)", Path(c).name) for c in checkpoints]
    fold_ids = [int(m.group(1)) for m in fold_ids if m]
    paths = [(root / f"pred_df_fold{f}.csv", f) for f in fold_ids]
    if not any(path.is_file() for path, _ in paths):
        paths = [(root / "oof.csv", None), (root / "oof_predictions.csv", None)]
    for path, fold_id in paths:
        if not path.is_file():
            continue
        frame = pd.read_csv(path)
        pred_col = next((c for c in ["raw_pred", "prediction", "pred", "oof_pred"]
                         if c in frame.columns), None)
        if pred_col is None or not {"essay_id", "score"}.issubset(frame.columns):
            continue
        # An all-fold OOF table cannot calibrate one selected fold unfiltered.
        if fold_id is None and len(fold_ids) == 1:
            fold_col = next((c for c in ["fold", "kfold"] if c in frame.columns), None)
            if fold_col is None:
                continue
            frame = frame.loc[frame[fold_col] == fold_ids[0]]
        if frame.essay_id.duplicated().any():
            continue
        checked = frame[["essay_id", "score", pred_col]].merge(
            train, on="essay_id", how="inner", suffixes=("", "_truth"), validate="one_to_one")
        if len(checked) != len(frame) or not np.array_equal(checked.score, checked.score_truth):
            continue
        checked = checked.rename(columns={pred_col: "raw_prediction"})
        pieces.append(checked[["essay_id", "score", "raw_prediction"]])
        if fold_id is None:
            break
    if not pieces:
        print("No compatible held-out predictions found; retaining prior cutoffs.")
        return initial
    data = pd.concat(pieces, ignore_index=True)
    if data.essay_id.duplicated().any():
        print("Overlapping validation artifacts; retaining prior cutoffs.")
        return initial
    y = data.score.to_numpy(dtype=int)
    pred = data.raw_prediction.to_numpy(dtype=float)
    if (len(y) < 600 or not np.isfinite(pred).all()
            or not np.array_equal(np.unique(y), np.arange(1, 7))
            or np.bincount(y, minlength=7)[1:].min() < 5
            or np.std(pred) < 0.2 or np.mean((pred >= 0) & (pred <= 7)) < 0.99):
        print("Validation artifact failed calibration sanity checks; retaining prior cutoffs.")
        return initial

    def qwk(target, values, thresholds):
        return cohen_kappa_score(target, np.digitize(values, thresholds) + 1,
                                weights="quadratic", labels=np.arange(1, 7))

    def fit(target, values):
        def loss(t):
            if np.any(np.diff(t) < 0.15):
                return 10.0
            # Penalize unstable cutoffs, especially at scarce endpoint classes.
            return -qwk(target, values, t) + 0.01 * np.mean((t - initial) ** 2)
        bounds = [(float(t - 0.40), float(t + 0.40)) for t in initial]
        starts = [initial, np.clip(np.arange(1.5, 6.0), initial - 0.39, initial + 0.39)]
        candidates = [initial]
        for start in starts:
            result = minimize(loss, start, method="Powell", bounds=bounds,
                              options={"maxiter": 100, "xtol": 1e-4, "ftol": 1e-6})
            if np.isfinite(result.x).all() and np.all(np.diff(result.x) >= 0.15):
                candidates.append(result.x)
        return min(candidates, key=loss)

    strengths = [0.0, 0.25, 0.5, 0.75, 1.0]
    heldout = np.zeros((len(strengths), len(y)), dtype=int)
    splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=2024)
    for train_idx, valid_idx in splitter.split(pred, y):
        fitted = fit(y[train_idx], pred[train_idx])
        for j, strength in enumerate(strengths):
            cuts = initial + strength * (fitted - initial)
            heldout[j, valid_idx] = np.digitize(pred[valid_idx], cuts) + 1
    scores = [cohen_kappa_score(y, values, weights="quadratic", labels=np.arange(1, 7))
              for values in heldout]
    best = int(np.argmax(scores))
    print("Cross-validated calibration QWK:", dict(zip(strengths, scores)))
    # Demand an improvement, then prefer the smallest near-optimal adjustment.
    if scores[best] < scores[0] + 0.001:
        return initial
    best = next(j for j in range(1, len(strengths))
                if scores[j] >= scores[best] - 0.0002 and scores[j] >= scores[0] + 0.001)
    thresholds = initial + strengths[best] * (fit(y, pred) - initial)
    print("Selected score thresholds:", thresholds.tolist())
    return thresholds

DEBUG = False
config = OmegaConf.load(args.config)
config.merge_with_dotlist(unknown_args)
df = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/test.csv")
tokenizer = AutoTokenizer.from_pretrained(config.model.path)
tokenizer.add_tokens([AddedToken("\n\n", normalized=False)])
tokenizer.add_tokens([AddedToken("\n", normalized=False)])

if DEBUG:
    df["full_text"] = df["full_text"].apply(lambda x: x + "\n" + x + "\n" + x)
    df = pd.concat([df] * 2000, axis=0).reset_index(drop=True)
ds = datasets.Dataset.from_pandas(df)
ds = ds.map(lambda x: tokenize(x, tokenizer, max_length=config.train.validate_max_length), num_proc=2)
ds = loc_datasets(ds, ["input_ids", "attention_mask"])

collate_fn = SequenceBucketPadCollator(max_length=config.train.validate_max_length, tokenizer=tokenizer)
dataloader = torch.utils.data.DataLoader(
    CompetitionDataset(x=ds), batch_size=config.train.batch_size,
    shuffle=False, num_workers=2,
    collate_fn=collate_fn
)
checkpoints = json.loads(args.checkpoints)
# if config.train.exp_name in ["exp302", "exp301"]:
from training.two_stage.models import AESRegressionModel as ModelClass

model = ModelClass(config).to("cuda")
model.backbone.resize_token_embeddings(len(tokenizer))

predictions = []
for checkpoint in checkpoints:
    print(f"<<< process: {checkpoint}")
    model.load_state_dict(torch.load(checkpoint, map_location="cpu"))
    prediction = inference(model, dataloader)
    predictions.append(prediction)

preds = np.mean(predictions, axis=0).reshape(-1, )
if len(preds) != len(df) or not np.isfinite(preds).all():
    raise ValueError("Invalid regression predictions")
thresholds = validation_thresholds(checkpoints, json.loads(args.weights))
scores = (np.digitize(preds, thresholds) + 1).astype(np.int64)
prediction_frame = pd.DataFrame({"essay_id": df.essay_id, "score": scores})
sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")
sub = sub[["essay_id"]].merge(prediction_frame, on="essay_id", how="left", validate="one_to_one")
if sub.score.isna().any() or not sub.score.between(1, 6).all():
    raise ValueError("Submission IDs or scores are invalid")
sub["score"] = sub.score.astype(int)
sub.to_csv(args.save_name, index=False)
pd.DataFrame({"essay_id": df.essay_id, "raw_pred": preds}).to_csv("raw_predictions.csv", index=False)
Path("calibration.json").write_text(json.dumps({"checkpoints": checkpoints,
                                              "thresholds": thresholds.tolist()}, indent=2))

# %%
%%writefile predict_pet.py
import json
import sys
sys.path.append("/kaggle/input/omegaconf")
sys.path.append("/kaggle/input/aes2-code/kaggle-aes2-v1.3/kaggle-aes2-v1.3")
from argparse import ArgumentParser

import datasets
import torch
import torch.utils.data
import numpy as np
import pandas as pd
from datasets import Dataset
from omegaconf import OmegaConf
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AddedToken

from aes2.utils.collators.sequence_bucket import SequenceBucketPadCollator
from aes2.utils.dataset.simple import CompetitionDataset
from aes2.utils.metrics import OptimizedRounder
from training.lang_model.models import AESRegressionModel as ModelClass

parser = ArgumentParser()
parser.add_argument("--config", default=None, required=False)
parser.add_argument("--checkpoints", type=str)
parser.add_argument("--save-name", type=str)

args, unknown_args = parser.parse_known_args()


def tokenize(example, tokenizer, max_length=1024):
    full_text = example["full_text"]
    truncation = True
    text = f"Student Writing Evaluate\n\nThe score(1 to 6) of the following essay is: {tokenizer.mask_token}."
    text += tokenizer.sep_token + full_text
    encoding = tokenizer(text, return_token_type_ids=False, truncation=truncation, max_length=max_length)
    mask_token_indexes = []
    for i, input_id in enumerate(encoding["input_ids"]):
        if input_id == tokenizer.mask_token_id:
            mask_token_indexes.append(i)
            break

    return {
        "input_ids": encoding["input_ids"],
        "attention_mask": encoding["attention_mask"],
        "mask_token_indexes": mask_token_indexes[0]
    }


def loc_datasets(ds, keep_columns):
    return Dataset.from_dict({col: ds[col] for col in keep_columns})



@torch.no_grad()
def inference(model, dataloader):
    predictions = []
    model.eval()
    for x in tqdm(dataloader, total=len(dataloader)):
        predictions.append(model({key: x[key].to("cuda") for key in x}).cpu().numpy())
    return np.concatenate(predictions, axis=0)


DEBUG = False
config = OmegaConf.load(args.config)
config.merge_with_dotlist(unknown_args)
df = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/test.csv")
tokenizer = AutoTokenizer.from_pretrained(config.model.path)
tokenizer.add_tokens([AddedToken("\n\n", normalized=False)])
tokenizer.add_tokens([AddedToken("\n", normalized=False)])

if DEBUG:
    df["full_text"] = df["full_text"].apply(lambda x: x + "\n" + x + "\n" + x)
    df = pd.concat([df] * 2000, axis=0).reset_index(drop=True)
ds = datasets.Dataset.from_pandas(df)
ds = ds.map(lambda x: tokenize(x, tokenizer, max_length=config.train.validate_max_length), num_proc=2)
ds = loc_datasets(ds, ["input_ids", "attention_mask", "mask_token_indexes"])

collate_fn = SequenceBucketPadCollator(max_length=config.train.validate_max_length, tokenizer=tokenizer)
dataloader = torch.utils.data.DataLoader(
    CompetitionDataset(x=ds), batch_size=config.train.batch_size,
    shuffle=False, num_workers=2,
    collate_fn=collate_fn
)
checkpoints = json.loads(args.checkpoints)

model = ModelClass(config).to("cuda")
model.backbone.resize_token_embeddings(len(tokenizer))

predictions = []
for checkpoint in checkpoints:
    print(f"<<< process: {checkpoint}")
    model.load_state_dict(torch.load(checkpoint))
    prediction = inference(model, dataloader)
    predictions.append(prediction)

preds = np.mean(predictions, axis=0).reshape(-1, )
optimized_rounder = OptimizedRounder()
if DEBUG:
    sub = df[["essay_id"]]
else:
    sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")
    
sub.loc[:, "score"] = optimized_rounder.predict(preds, np.array([1.59976018, 2.51349702, 3.4728789, 4.38860353, 5.12977217]))
# sub.loc[:, "score"] = preds.round(0).astype(int)
sub.to_csv(args.save_name, index=False)

# %%
%%writefile predict_clf.py
import json
import sys
sys.path.append("/kaggle/input/omegaconf")
sys.path.append("/kaggle/input/aes2-code/kaggle-aes2-v1.2/kaggle-aes2-v1.2")
from argparse import ArgumentParser

import datasets
import torch
import torch.utils.data
import numpy as np
import pandas as pd
from datasets import Dataset
from omegaconf import OmegaConf
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AddedToken

from aes2.utils.collators.sequence_bucket import SequenceBucketPadCollator
from aes2.utils.dataset.simple import CompetitionDataset
from aes2.utils.metrics import OptimizedRounder

parser = ArgumentParser()
parser.add_argument("--config", default=None, required=False)
parser.add_argument("--checkpoints", type=str)
parser.add_argument("--save-name", type=str)

args, unknown_args = parser.parse_known_args()


def tokenize(example, tokenizer, max_length=1024):
    full_text = example["full_text"]
    truncation = True
    encoding = tokenizer(full_text, return_token_type_ids=False, truncation=truncation, max_length=max_length)

    return {
        "input_ids": encoding["input_ids"],
        "attention_mask": encoding["attention_mask"]
    }


def loc_datasets(ds, keep_columns):
    return Dataset.from_dict({col: ds[col] for col in keep_columns})



@torch.no_grad()
def inference(model, dataloader):
    predictions = []
    model.eval()
    for x in tqdm(dataloader, total=len(dataloader)):
        predictions.append(model({key: x[key].to("cuda") for key in x}).softmax(-1).cpu().numpy())
    return np.concatenate(predictions, axis=0)


DEBUG = False
config = OmegaConf.load(args.config)
config.merge_with_dotlist(unknown_args)
df = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/test.csv")
tokenizer = AutoTokenizer.from_pretrained(config.model.path)
tokenizer.add_tokens([AddedToken("\n\n", normalized=False)])
tokenizer.add_tokens([AddedToken("\n", normalized=False)])

if DEBUG:
    df["full_text"] = df["full_text"].apply(lambda x: x + "\n" + x + "\n" + x)
    df = pd.concat([df] * 2000, axis=0).reset_index(drop=True)
ds = datasets.Dataset.from_pandas(df)
ds = ds.map(lambda x: tokenize(x, tokenizer, max_length=config.train.validate_max_length), num_proc=2)
ds = loc_datasets(ds, ["input_ids", "attention_mask"])

collate_fn = SequenceBucketPadCollator(max_length=config.train.validate_max_length, tokenizer=tokenizer)
dataloader = torch.utils.data.DataLoader(
    CompetitionDataset(x=ds), batch_size=config.train.batch_size,
    shuffle=False, num_workers=2,
    collate_fn=collate_fn
)
checkpoints = json.loads(args.checkpoints)
# if config.train.exp_name in ["exp302", "exp301"]:
from training.baseline_reg.models import AESRegressionModel as ModelClass

model = ModelClass(config).to("cuda")
model.backbone.resize_token_embeddings(len(tokenizer))

predictions = []
for checkpoint in checkpoints:
    print(f"<<< process: {checkpoint}")
    model.load_state_dict(torch.load(checkpoint))
    prediction = inference(model, dataloader)
    predictions.append(prediction)

preds = np.mean(predictions, axis=0)
# optimized_rounder = OptimizedRounder()
if DEBUG:
    sub = df[["essay_id"]]
else:
    sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")

sub.loc[:, "score"] = preds.argmax(-1).astype(int) + 1
# sub.loc[:, "score"] = optimized_rounder.predict(preds, np.array([1.82042385, 2.79213896, 3.53041305, 4.2013425, 5.38434595]))
# sub.loc[:, "score"] = preds.round(0).astype(int)
sub.to_csv(args.save_name, index=False)

# %%
# !python predict_clf.py \
#   --config "/kaggle/input/exp301-base-rk2-f0/config.yaml" \
#   --checkpoints '["/kaggle/input/exp301-base-rk2-f0/model_fold0.pth"]' \
#   --save-name "submission.csv" \
#   model.path="/kaggle/input/deberta-v3-base/deberta-v3-base"

# %%
# !python predict_pet.py \
#   --config "/kaggle/input/exp303d-pet-base-itpt10-015-f0/config.yaml" \
#   --checkpoints '["/kaggle/input/exp303d-pet-base-itpt10-015-f0/model_fold0.pth"]' \
#   --save-name "submission.csv" \
#   model.path="/kaggle/input/deberta-v3-base/deberta-v3-base" model.vocab_size=128003

# %%
# Prefer the experiment behind v52 (0.81978); retain the mounted v54
# ensemble if the older single-fold assets are unavailable in this notebook.
from pathlib import Path
import json
import subprocess
import sys

preferred = Path("/kaggle/input/exp301-1-large-itpt10-f0")
fallback = Path("/kaggle/input/exp301-1-large-itpt10-all")
preferred_checkpoint = next((preferred / name for name in
                             ["model_fold0_last.pth", "model_fold0.pth"]
                             if (preferred / name).is_file()), None)
if (preferred / "config.yaml").is_file() and preferred_checkpoint is not None:
    experiment = preferred
    selected_checkpoints = [str(preferred_checkpoint)]
else:
    experiment = fallback
    selected_checkpoints = [str(fallback / f"model_fold{fold}.pth") for fold in range(4)]
for required in [experiment / "config.yaml", *map(Path, selected_checkpoints)]:
    if not required.is_file():
        raise FileNotFoundError(f"Missing required Kaggle model artifact: {required}")

# These are ordered score cutoffs, not ensemble coefficients. The exact v52
# cutoffs are absent from history; retain the known prior unless validation
# supports a change. Do not tune against the tiny public test sample.
prior_thresholds = [1.68702789, 2.59396091, 3.35737494, 4.41395307, 5.1408953]
print("Selected experiment:", experiment)
subprocess.run([
    sys.executable, "predict_exp302.py",
    "--config", str(experiment / "config.yaml"),
    "--checkpoints", json.dumps(selected_checkpoints),
    "--save-name", "submission.csv",
    "--weights", json.dumps(prior_thresholds),
    "--calibration-dir", str(experiment),
    "model.path=/kaggle/input/deberta-v3-large/deberta-v3-large",
], check=True)

# %%
import pandas as pd


pd.read_csv("submission.csv")

# %%
# import pandas as pd
# import sys
# sys.path.append("/kaggle/input/omegaconf/omegaconf")
# sys.path.append("/kaggle/input/aes2-code/kaggle-aes2-v0")
# from aes2.utils.metrics import OptimizedRounder


# df = pd.read_csv("/kaggle/input/aes-exp302-two-stage-f0/pred_df_fold0.csv")
# optimized_rounder = OptimizedRounder()
# optimized_rounder.fit(df["raw_pred"], df["score"])
# print(optimized_rounder._coef)

# %%
# df[df["essay_id"] == "000d118"]

# %%


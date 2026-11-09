# %%
%%writefile predict_exp302.py
import json
import sys
from pathlib import Path
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
# Historical --weights values are ordinal cutpoints, not model weights.
parser.add_argument("--thresholds", "--weights", dest="thresholds", type=str, required=True)
parser.add_argument("--calibration-ids", type=str, default=None)

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
    model.load_state_dict(torch.load(checkpoint))
    prediction = inference(model, dataloader)
    predictions.append(prediction)

preds = np.mean(predictions, axis=0).reshape(-1, )
thresholds = np.asarray(json.loads(args.thresholds), dtype=np.float64)
if thresholds.shape != (5,) or not np.isfinite(thresholds).all() or not (np.diff(thresholds) > 0).all():
    raise ValueError("Expected five finite, increasing score thresholds")
if len(preds) != len(df) or not np.isfinite(preds).all():
    raise ValueError("Invalid test predictions")


def qwk(y, p, cuts):
    labels = np.searchsorted(cuts, p, side="right") + 1
    # QWK's expected squared disagreement under independent marginals.
    expected = np.mean(y ** 2) + np.mean(labels ** 2) - 2 * np.mean(y) * np.mean(labels)
    return 1.0 - np.mean((y - labels) ** 2) / max(expected, 1e-12)


def fit_cutpoints(y, p, anchor):
    # Bounded coordinate search keeps this small calibration set from moving
    # cutpoints arbitrarily far. Shrink halfway back to the original mapping.
    cuts = anchor.copy()
    for radius in (0.20, 0.08, 0.03):
        for k in range(5):
            low = max(anchor[k] - 0.30, cuts[k] - radius,
                      cuts[k - 1] + 0.05 if k else 1.05)
            high = min(anchor[k] + 0.30, cuts[k] + radius,
                       cuts[k + 1] - 0.05 if k < 4 else 5.95)
            best_score = qwk(y, p, cuts)
            best = cuts[k]
            for value in np.linspace(low, high, 25):
                candidate = cuts.copy()
                candidate[k] = value
                score = qwk(y, p, candidate)
                if score > best_score + 1e-10:
                    best_score, best = score, value
            cuts[k] = best
    return 0.5 * anchor + 0.5 * cuts


calibration_log = {"initial_thresholds": thresholds.tolist(), "accepted": False}
if args.calibration_ids is not None:
    # Only the selected single-fold run's own held-out ID file is permitted.
    # Recompute predictions: its stored raw_pred may describe a different epoch.
    if len(checkpoints) != 1:
        raise ValueError("Calibration requires one checkpoint with its own held-out IDs")
    heldout = pd.read_csv(args.calibration_ids, dtype={"essay_id": str})
    train = pd.read_csv(
        "/kaggle/input/learning-agency-lab-automated-essay-scoring-2/train.csv",
        dtype={"essay_id": str})
    ids = heldout[["essay_id"]]
    if ids["essay_id"].duplicated().any() or ids["essay_id"].isin(df["essay_id"]).any():
        raise ValueError("Invalid held-out essay IDs")
    valid = ids.merge(train, on="essay_id", how="left", validate="one_to_one")
    if valid[["full_text", "score"]].isna().any().any():
        raise ValueError("Held-out IDs are missing from the labeled training data")
    counts = valid["score"].value_counts().reindex(range(1, 7), fill_value=0)
    if len(valid) >= 600 and counts.min() >= 6:
        from sklearn.model_selection import StratifiedKFold
        valid_ds = Dataset.from_pandas(valid[["full_text"]], preserve_index=False)
        valid_ds = valid_ds.map(
            lambda x: tokenize(x, tokenizer, max_length=config.train.validate_max_length), num_proc=2)
        valid_ds = loc_datasets(valid_ds, ["input_ids", "attention_mask"])
        valid_loader = torch.utils.data.DataLoader(
            CompetitionDataset(x=valid_ds), batch_size=config.train.batch_size,
            shuffle=False, num_workers=2, collate_fn=collate_fn)
        valid_preds = inference(model, valid_loader).reshape(-1)
        y = valid["score"].to_numpy(dtype=np.float64)
        if len(valid_preds) != len(y) or not np.isfinite(valid_preds).all():
            raise ValueError("Invalid calibration predictions")
        baseline_labels = np.searchsorted(thresholds, valid_preds, side="right") + 1
        crossfit_labels = np.empty(len(y), dtype=np.int64)
        gains = []
        for fit_idx, eval_idx in StratifiedKFold(3, shuffle=True, random_state=2024).split(valid_preds, y):
            candidate = fit_cutpoints(y[fit_idx], valid_preds[fit_idx], thresholds)
            crossfit_labels[eval_idx] = np.searchsorted(candidate, valid_preds[eval_idx], side="right") + 1
            gains.append(qwk(y[eval_idx], valid_preds[eval_idx], candidate)
                         - qwk(y[eval_idx], valid_preds[eval_idx], thresholds))
        from sklearn.metrics import cohen_kappa_score
        baseline_score = cohen_kappa_score(y, baseline_labels, weights="quadratic")
        candidate_score = cohen_kappa_score(y, crossfit_labels, weights="quadratic")
        calibration_log.update(baseline_qwk=float(baseline_score),
                               crossfit_qwk=float(candidate_score), fold_gains=gains)
        if candidate_score >= baseline_score + 0.001 and sum(g > 0 for g in gains) >= 2:
            thresholds = fit_cutpoints(y, valid_preds, thresholds)
            calibration_log["accepted"] = True
        pd.DataFrame({"essay_id": valid["essay_id"], "score": y,
                      "raw_pred": valid_preds}).to_csv("calibration_predictions.csv", index=False)
    else:
        calibration_log["reason"] = "Too few held-out examples for stable cutpoint tuning"

calibration_log["final_thresholds"] = thresholds.tolist()
Path("calibration.json").write_text(json.dumps(calibration_log, indent=2))
# Preserve raw predictions for subsequent calibration without another GPU run.
raw = df[["essay_id"]].copy()
raw["raw_pred"] = preds
raw.to_csv("test_raw_predictions.csv", index=False)
raw["score"] = (np.searchsorted(thresholds, preds, side="right") + 1).astype(np.int64)
if DEBUG:
    sub = raw[["essay_id", "score"]]
else:
    sample = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")
    sub = sample[["essay_id"]].merge(raw[["essay_id", "score"]], on="essay_id",
                                      how="left", sort=False, validate="one_to_one")
    if sub["score"].isna().any():
        raise ValueError("Missing submission predictions")
    sub["score"] = sub["score"].astype(np.int64)
sub.to_csv(args.save_name, index=False)

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
# Restore the single-fold experiment family that scored 0.81978 in v52
# and 0.81104 in v53. The exact v52 cutpoints are not in the supplied history.
# Keep the known v54 paths as an explicit fallback if the older mount is absent.
import json
import subprocess
import sys
from pathlib import Path

preferred = Path("/kaggle/input/exp301-1-large-itpt10-f0")
fallback = Path("/kaggle/input/exp301-1-large-itpt10-all")
preferred_checkpoint = preferred / "model_fold0_last.pth"
calibration_ids = None
if (preferred / "config.yaml").is_file() and preferred_checkpoint.is_file():
    experiment = preferred
    checkpoints = [str(preferred_checkpoint)]
    # This filename is the held-out prediction convention documented in the
    # original notebook. Never use an unrelated run's predictions to calibrate.
    candidate_ids = preferred / "pred_df_fold0.csv"
    if candidate_ids.is_file():
        import pandas as pd
        # Older exported validation tables need not retain their essay IDs.
        # Such a table cannot establish the held-out input rows safely.
        if "essay_id" in pd.read_csv(candidate_ids, nrows=0).columns:
            calibration_ids = candidate_ids
        else:
            print("Validation table has no essay_id column; retaining initial thresholds.")
else:
    experiment = fallback
    checkpoints = [str(experiment / f"model_fold{fold}.pth") for fold in range(4)]
    print("Preferred historical checkpoint is not mounted; using the original v54 ensemble.")

for artifact in [str(experiment / "config.yaml")] + checkpoints:
    if not Path(artifact).is_file():
        raise FileNotFoundError(artifact)
thresholds = [1.68702789, 2.59396091, 3.35737494, 4.41395307, 5.1408953]
command = [sys.executable, "predict_exp302.py",
           "--config", str(experiment / "config.yaml"),
           "--checkpoints", json.dumps(checkpoints),
           "--save-name", "submission.csv",
           "--thresholds", json.dumps(thresholds)]
if calibration_ids is not None:
    command.extend(["--calibration-ids", str(calibration_ids)])
command.append("model.path=/kaggle/input/deberta-v3-large/deberta-v3-large")
Path("inference_manifest.json").write_text(json.dumps({
    "experiment": str(experiment), "checkpoints": checkpoints,
    "initial_thresholds": thresholds,
    "calibration_ids": str(calibration_ids) if calibration_ids is not None else None
}, indent=2))
subprocess.run(command, check=True)

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


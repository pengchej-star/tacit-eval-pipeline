# %%
%%writefile predict_exp302.py
import json
import re
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
# Kept for compatibility: --weights contains ordinal CUTPOINTS, not model weights.
parser.add_argument("--weights", type=str)
parser.add_argument("--tail-weight", type=float, default=0.15)
parser.add_argument("--skip-oof-calibration", action="store_true")

args, unknown_args = parser.parse_known_args()


def make_views(text, tokenizer, max_length):
    # Preserve the checkpoint's original prefix input exactly. Only essays that
    # exceed its context window receive a second, conclusion-aware view.
    ids = tokenizer(str(text), add_special_tokens=False, truncation=False)["input_ids"]
    budget = int(max_length) - tokenizer.num_special_tokens_to_add(pair=False)
    if budget < 8:
        raise ValueError("Validation context length is too small")
    def pack(tokens):
        values = tokenizer.build_inputs_with_special_tokens(tokens)
        return {"input_ids": values, "attention_mask": [1] * len(values)}
    prefix = pack(ids[:budget])
    if len(ids) <= budget:
        return prefix, None
    head = (2 * budget) // 3
    tail = pack(ids[:head] + ids[-(budget - head):])
    return prefix, tail


def prepare_loader(frame, tokenizer, config):
    rows, tail_indices = [], []
    tails = []
    for i, text in enumerate(frame["full_text"].fillna("")):
        prefix, tail = make_views(text, tokenizer, config.train.validate_max_length)
        rows.append(prefix)
        if tail is not None and args.tail_weight > 0:
            tail_indices.append(i)
            tails.append(tail)
    rows.extend(tails)
    # Bucket globally by length to reduce padding, then undo the permutation.
    order = np.argsort([len(row["input_ids"]) for row in rows], kind="stable")
    ds = Dataset.from_dict({key: [rows[int(i)][key] for i in order]
                            for key in ("input_ids", "attention_mask")})
    loader = torch.utils.data.DataLoader(
        CompetitionDataset(x=ds), batch_size=config.train.batch_size,
        shuffle=False, num_workers=2, pin_memory=True,
        collate_fn=SequenceBucketPadCollator(
            max_length=config.train.validate_max_length, tokenizer=tokenizer))
    return loader, order, np.asarray(tail_indices, dtype=np.int64), len(frame)


@torch.inference_mode()
def inference(model, prepared):
    dataloader, order, tail_indices, n = prepared
    predictions = []
    model.eval()
    for x in tqdm(dataloader, total=len(dataloader)):
        pred = model({key: x[key].to("cuda", non_blocking=True) for key in x})
        predictions.append(pred.float().cpu().numpy().reshape(-1))
    sorted_predictions = np.concatenate(predictions)
    if len(sorted_predictions) != len(order):
        raise ValueError("Expected one regression output per essay view")
    restored = np.empty_like(sorted_predictions)
    restored[order] = sorted_predictions
    prefix = restored[:n].copy()
    blended = prefix.copy()
    blended[tail_indices] = ((1.0 - args.tail_weight) * prefix[tail_indices]
                            + args.tail_weight * restored[n:])
    if not np.isfinite(blended).all():
        raise ValueError("Nonfinite predictions")
    return blended, prefix


def load_holdouts(checkpoints):
    # Only consume explicit per-fold validation exports, never arbitrary train
    # predictions. Reject overlapping folds, duplicate IDs, or incorrect labels.
    if args.skip_oof_calibration:
        return None
    files = []
    for checkpoint in checkpoints:
        match = re.fullmatch(r"model_fold(\d+)(?:_last)?\.pth", Path(checkpoint).name)
        if match is None:
            return None
        artifact = Path(checkpoint).parent / ("pred_df_fold" + match.group(1) + ".csv")
        if not artifact.is_file():
            print("No complete held-out exports; retaining supplied cutpoints")
            return None
        files.append(artifact)
    train = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/train.csv")
    train = train.set_index("essay_id", verify_integrity=True)
    seen, frames = set(), []
    for artifact in files:
        saved = pd.read_csv(artifact)
        if not {"essay_id", "score", "raw_pred"}.issubset(saved.columns):
            return None
        ids = saved["essay_id"]
        if len(ids) < 500 or ids.duplicated().any() or not ids.isin(train.index).all():
            return None
        if seen.intersection(ids):
            print("Overlapping validation exports rejected")
            return None
        frame = train.loc[ids].reset_index()
        if not np.array_equal(frame["score"].to_numpy(), saved["score"].to_numpy()):
            return None
        if frame["score"].nunique() != 6:
            return None
        seen.update(ids)
        frames.append(frame)
    return frames if len(frames) >= 3 else None


def apply_cutpoints(pred, cutpoints):
    return (np.searchsorted(cutpoints, pred, side="right") + 1).astype(np.int64)


def qwk(y, pred):
    # Algebraically identical to six-class quadratic weighted Cohen's kappa.
    y, pred = np.asarray(y, dtype=float), np.asarray(pred, dtype=float)
    expected = np.mean(y*y) + np.mean(pred*pred) - 2*np.mean(y)*np.mean(pred)
    return 1.0 - np.mean((y-pred)**2) / max(expected, 1e-12)


def fit_cutpoints(y, pred, initial):
    cuts = initial.copy()
    # A bounded, deterministic search, anchored to the existing calibration.
    for radius in (0.20, 0.08, 0.025):
        for j in range(5):
            low = max(initial[j] - 0.35, cuts[j] - radius,
                      cuts[j-1] + 0.15 if j else 1.0)
            high = min(initial[j] + 0.35, cuts[j] + radius,
                       cuts[j+1] - 0.15 if j < 4 else 6.0)
            best = qwk(y, apply_cutpoints(pred, cuts))
            value = cuts[j]
            for candidate in np.linspace(low, high, 33):
                trial = cuts.copy()
                trial[j] = candidate
                score = qwk(y, apply_cutpoints(pred, trial))
                if score > best + 1e-10:
                    best, value = score, candidate
            cuts[j] = value
    return cuts


def calibrated_cutpoints(y, pred, fold_ids, initial):
    # Select shrinkage using predictions calibrated WITHOUT that fold's labels.
    strengths = (0.0, 0.25, 0.5, 1.0)
    scores = {strength: np.zeros(len(y), dtype=np.int64) for strength in strengths}
    fold_gains = {strength: [] for strength in strengths}
    for fold in np.unique(fold_ids):
        valid = fold_ids == fold
        fitted = fit_cutpoints(y[~valid], pred[~valid], initial)
        baseline = qwk(y[valid], apply_cutpoints(pred[valid], initial))
        for strength in strengths:
            values = apply_cutpoints(pred[valid], initial + strength*(fitted-initial))
            scores[strength][valid] = values
            fold_gains[strength].append(qwk(y[valid], values) - baseline)
    baseline = qwk(y, scores[0.0])
    selected, best = 0.0, baseline
    for strength in strengths[1:]:
        score = qwk(y, scores[strength])
        gains = np.asarray(fold_gains[strength])
        if score > best + 0.0005 and np.sum(gains >= 0) >= len(gains)-1:
            selected, best = strength, score
    cuts = initial if selected == 0 else initial + selected*(fit_cutpoints(y, pred, initial)-initial)
    print("Cross-fitted calibration QWK:", baseline, best, "shrinkage:", selected)
    Path("calibration.json").write_text(json.dumps({
        "baseline_qwk": float(baseline), "cross_fitted_qwk": float(best),
        "shrinkage": selected, "cutpoints": cuts.tolist()}, indent=2))
    return cuts


DEBUG = False
config = OmegaConf.load(args.config)
config.merge_with_dotlist(unknown_args)
df = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/test.csv")
tokenizer = AutoTokenizer.from_pretrained(config.model.path)
tokenizer.add_tokens([AddedToken("\n\n", normalized=False)])
tokenizer.add_tokens([AddedToken("\n", normalized=False)])

if not 0.0 <= args.tail_weight <= 0.5:
    raise ValueError("tail-weight must be between 0 and 0.5")
prepared_test = prepare_loader(df, tokenizer, config)
checkpoints = json.loads(args.checkpoints)
# if config.train.exp_name in ["exp302", "exp301"]:
from training.two_stage.models import AESRegressionModel as ModelClass

model = ModelClass(config).to("cuda")
model.backbone.resize_token_embeddings(len(tokenizer))

holdouts = load_holdouts(checkpoints)
predictions, oof_preds, oof_labels, oof_folds, oof_ids = [], [], [], [], []
test_prefixes, oof_prefixes = [], []
for fold, checkpoint in enumerate(checkpoints):
    print(f"<<< process: {checkpoint}")
    # Load on CPU first to avoid a second full checkpoint allocation on GPU.
    state = torch.load(checkpoint, map_location="cpu")
    model.load_state_dict(state)
    del state
    prediction, prefix = inference(model, prepared_test)
    predictions.append(prediction)
    test_prefixes.append(prefix)
    np.savez_compressed(f"test_predictions_fold{fold}.npz",
                       essay_id=df["essay_id"].to_numpy(dtype=str),
                       prediction=prediction, prefix=prefix)
    if holdouts is not None:
        valid = holdouts[fold]
        prepared_valid = prepare_loader(valid, tokenizer, config)
        valid_pred, valid_prefix = inference(model, prepared_valid)
        del prepared_valid
        oof_preds.append(valid_pred)
        oof_prefixes.append(valid_prefix)
        oof_labels.append(valid["score"].to_numpy())
        oof_folds.append(np.full(len(valid), fold, dtype=int))
        oof_ids.append(valid["essay_id"].to_numpy(dtype=str))
        np.savez_compressed(f"oof_predictions_fold{fold}.npz",
                           essay_id=oof_ids[-1], score=oof_labels[-1],
                           prediction=valid_pred, prefix=valid_prefix)

preds = np.mean(predictions, axis=0).reshape(-1)
cutpoints = np.asarray(json.loads(args.weights), dtype=float)
if cutpoints.shape != (5,) or not np.all(np.diff(cutpoints) > 0):
    raise ValueError("Expected five increasing score cutpoints")
if holdouts is not None:
    labels, folds = np.concatenate(oof_labels), np.concatenate(oof_folds)
    oof_blend, oof_prefix = np.concatenate(oof_preds), np.concatenate(oof_prefixes)
    baseline_qwk = qwk(labels, apply_cutpoints(oof_prefix, cutpoints))
    view_qwk = qwk(labels, apply_cutpoints(oof_blend, cutpoints))
    gains = [qwk(labels[folds == f], apply_cutpoints(oof_blend[folds == f], cutpoints))
             - qwk(labels[folds == f], apply_cutpoints(oof_prefix[folds == f], cutpoints))
             for f in np.unique(folds)]
    use_tail = view_qwk > baseline_qwk + 0.0005 and np.sum(np.asarray(gains) >= 0) >= len(gains)-1
    print("Held-out prefix QWK:", baseline_qwk, "head-tail blend QWK:", view_qwk,
          "use head-tail:", use_tail)
    if not use_tail:
        preds = np.mean(test_prefixes, axis=0).reshape(-1)
    selected_oof = oof_blend if use_tail else oof_prefix
    cutpoints = calibrated_cutpoints(labels, selected_oof, folds, cutpoints)
# Join on the competition key, rather than relying on sample/test row order.
result = pd.DataFrame({"essay_id": df["essay_id"], "score": apply_cutpoints(preds, cutpoints)})
sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")
sub = sub[["essay_id"]].merge(result, on="essay_id", how="left", validate="one_to_one", sort=False)
assert sub["score"].notna().all()
sub["score"] = sub["score"].astype(int)
assert sub["score"].between(1, 6).all()
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
!python predict_exp302.py \
  --config "/kaggle/input/exp301-1-large-itpt10-all/config.yaml" \
  --checkpoints '["/kaggle/input/exp301-1-large-itpt10-all/model_fold0.pth", \
                  "/kaggle/input/exp301-1-large-itpt10-all/model_fold1.pth", \
                  "/kaggle/input/exp301-1-large-itpt10-all/model_fold2.pth", \
                  "/kaggle/input/exp301-1-large-itpt10-all/model_fold3.pth"]' \
  --save-name "submission.csv" \
  --weights '[1.68702789, 2.59396091, 3.35737494, 4.41395307, 5.1408953]' \
  model.path="/kaggle/input/deberta-v3-large/deberta-v3-large"

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


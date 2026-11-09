# %%
%%writefile predict_exp302.py
import json
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
optimized_rounder = OptimizedRounder()
if DEBUG:
    sub = df[["essay_id"]]
else:
    sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")
    
sub.loc[:, "score"] = np.clip(optimized_rounder.predict(preds, np.array(json.loads(args.weights))), 1, 6).astype(int)
# sub.loc[:, "score"] = preds.round(0).astype(int)
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
# v55: restore the proven v52 configuration (best LB 0.81978): the single
# exp301-1-large-itpt10-f0 checkpoint. v53 (thresholds only) and v54 (new 4-fold
# checkpoint set + new thresholds) both regressed from it. The v54 threshold set had
# an outlying 3/4 cutpoint (3.357 vs ~3.47 in every other fitted set); use a balanced
# threshold set (mean of the two fitted sets present in this notebook) instead.
!python predict_exp302.py \
  --config "/kaggle/input/exp301-1-large-itpt10-f0/config.yaml" \
  --checkpoints '["/kaggle/input/exp301-1-large-itpt10-f0/model_fold0.pth"]' \
  --save-name "submission.csv" \
  --weights '[1.64339404, 2.55372897, 3.41512692, 4.40127830, 5.13533374]' \
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


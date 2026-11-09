# %% [markdown]
# # Inference topics

# %%
%%writefile inference_topics.py
import os
import copy

import torch
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datasets import Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments, EvalPrediction
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay

train_df = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/test.csv")

label2id = {
    'Car-free cities': 1,
    'Does the electoral college work?': 2,
    '"A Cowboy Who Rode the Waves"': 0,
    'Exploring Venus': 4,
    'Driverless cars': 3,
    'Facial action coding system': 5,
    'The Face on Mars': 6
}
id2label = dict(zip(label2id.values(), label2id.keys()))
print(label2id)

checkpoint = "/kaggle/input/predict-the-prompts/output/fold_0/checkpoint-405"

class ModelInit:
    def __init__(self, checkpoint, label2id, id2label):
        self.model = AutoModelForSequenceClassification.from_pretrained(
            checkpoint, 
            num_labels=len(label2id),
            label2id=label2id,
            id2label=id2label,
        )
        self.state_dict = copy.deepcopy(self.model.state_dict())
        
    def __call__(self):
        self.model.load_state_dict(self.state_dict)
        return self.model


tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model_init = ModelInit(checkpoint, label2id=label2id, id2label=id2label)

intersection_ds = Dataset.from_pandas(train_df)
intersection_ds = intersection_ds.map(lambda i: tokenizer(i["full_text"], max_length=1024, truncation=True), batched=True)

def compute_metrics(eval_pred: EvalPrediction) -> dict[str, float]:
    predictions = eval_pred.predictions
    y_true = eval_pred.label_ids
    y_pred = predictions.argmax(-1)
    acc = accuracy_score(y_true, y_pred)
    return {"acc": acc}

args = TrainingArguments(
    output_dir="output",
    report_to="none",
    do_train=False,
    do_eval=False,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    per_device_eval_batch_size=8,
    learning_rate=1e-5,
    lr_scheduler_type="constant",
    warmup_ratio=0.0,
    num_train_epochs=1,
    weight_decay=0.01,
    optim="adamw_torch",
    fp16=torch.cuda.is_available()
)

predictions = []

train_ds = None
eval_ds = intersection_ds
trainer = Trainer(
    args=args, 
    model_init=model_init,
    train_dataset=train_ds, 
    eval_dataset=eval_ds, 
    tokenizer=tokenizer, 
    compute_metrics=compute_metrics
)
# trainer.train()
# predict on difference dataset
test_preds = trainer.predict(eval_ds)
predictions.append(test_preds.predictions)
predictions = np.stack(predictions, axis=0).mean(axis=0)  # average the result of 2 folds

essay_id = intersection_ds["essay_id"]
prompt_name = [id2label[i] for i in predictions.argmax(-1)]  # convert prompt id back to prompt name
result_df = pd.DataFrame({"essay_id": essay_id, "prompt_name": prompt_name})
result_df.to_csv("topics.csv", index=False)

# %% [markdown]
# # exp302

# %%
%%writefile predict_exp302.py
import math
import json
import sys
sys.path.append("/kaggle/input/omegaconf")
sys.path.append("/kaggle/input/aes2-code/kaggle-aes2-v2.8/kaggle-aes2-v2.8")
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
parser.add_argument("--only-round", default=False, action="store_true")

args, unknown_args = parser.parse_known_args()


def tokenize(example, tokenizer, max_length=1024):
    full_text = example["full_text"]
    truncation = True
    encoding = tokenizer(full_text, return_token_type_ids=False, truncation=truncation, max_length=max_length)

    return {
        "input_ids": encoding["input_ids"],
        "attention_mask": encoding["attention_mask"],
        "length": len(encoding["input_ids"])
    }


def loc_datasets(ds, keep_columns):
    return Dataset.from_dict({col: ds[col] for col in keep_columns})



@torch.no_grad()
def inference(model, dataloader, config):
    predictions = []
    model.eval()
    for x in tqdm(dataloader, total=len(dataloader)):
        logits = model({key: x[key].to("cuda") for key in x})
        if config.train.get("do_scale", False):
            logits = logits.sigmoid()
        predictions.append(logits.cpu().numpy())
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
df["length"] = ds["length"]
ds = ds.sort("length")
sorted_ids = ds["essay_id"]
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
    prediction = inference(model, dataloader, config)
    if config.train.get("do_scale", False):
        prediction = prediction * 5 + 1
    predictions.append(prediction)

preds = np.mean(predictions, axis=0).reshape(-1, )
if DEBUG:
    sub = df[["essay_id"]]
else:
    sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")
# sub = df.copy()

# sub = sub.merge(
#     pd.read_csv("topics.csv"), on="essay_id", how="left"
# )
# weights = {
#     '"A Cowboy Who Rode the Waves"': np.array([1.55692357, 2.77643607, 3.49162853, 4.09146394, 5.30628176]), 
#     'Car-free cities': np.array([1.57186639, 2.51445885, 3.68334285, 4.40684699, 5.25254136]), 
#     'Does the electoral college work?': np.array([1.5, 2.5, 3.5, 4.5, 5.5]), 
#     'Driverless cars': np.array([1.59670059, 2.63633308, 3.49125107, 4.4096048 , 5.13121992]), 
#     'Exploring Venus': np.array([1.70012591, 2.59353555, 3.48326817, 4.18691376, 4.58054575]), 
#     'Facial action coding system': np.array([1.63146038, 2.66156668, 3.5461211 , 4.12697535, 5.6006763 ]), 
#     'The Face on Mars': np.array([1.54191336, 2.51675508, 3.3934084 , 4.11961254, 5.77201775]),
#     "default": np.array([1.61849778, 2.67949533, 3.51754736, 4.33670269, 4.81457418])
# }
# sub["prompt_name"] = sub["prompt_name"].apply(lambda x: x if x in weights else "default")

# subs = []
# sub["raw_pred"] = preds
# optimized_rounder = OptimizedRounder()
# for topic_name, temp in sub.groupby("prompt_name"):
#     temp["score"] = optimized_rounder.predict(temp["raw_pred"], weights[topic_name])
#     subs.append(temp)

# sub = pd.concat(subs, axis=0).reset_index(drop=True)

optimized_rounder = OptimizedRounder()
sub = pd.DataFrame({"essay_id": sorted_ids}).merge(sub, on="essay_id", how="left")
sub.loc[:, "score"] = optimized_rounder.predict(preds, np.array(json.loads(args.weights)))
# sub.loc[:, "score"] = preds.round(0).astype(int)
sub[["essay_id", "score"]].to_csv(args.save_name, index=False)

# %% [markdown]
# # exp303

# %%
%%writefile predict_pet.py
import json
import sys
sys.path.append("/kaggle/input/omegaconf")
sys.path.append("/kaggle/input/aes2-code/kaggle-aes2-v2.7/kaggle-aes2-v2.7")
from argparse import ArgumentParser

import datasets
import torch
import torch.utils.data
import numpy as np
import pandas as pd
from accelerate import Accelerator
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
        predictions.append(model(x).cpu().numpy())
    return np.concatenate(predictions, axis=0)


DEBUG = False
accelerator = Accelerator(mixed_precision="no")
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

model = ModelClass(config)
model.backbone.resize_token_embeddings(len(tokenizer))
model, dataloader = accelerator.prepare(model, dataloader)

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

# %% [markdown]
# # exp320

# %%
%%writefile predict_pet2.py
import json
import sys
sys.path.append("/kaggle/input/omegaconf")
sys.path.append("/kaggle/input/aes2-code/kaggle-aes2-v3.2/kaggle-aes2-v3.2")
from argparse import ArgumentParser

import datasets
import torch
import torch.utils.data
import numpy as np
import pandas as pd
from accelerate import Accelerator
from datasets import Dataset
from omegaconf import OmegaConf
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AddedToken

from aes2.utils.collators.sequence_bucket import SequenceBucketPadCollator
from aes2.utils.dataset.simple import CompetitionDataset
from aes2.utils.metrics import OptimizedRounder
from training.pet.models import AESRegressionModel as ModelClass

parser = ArgumentParser()
parser.add_argument("--config", default=None, required=False)
parser.add_argument("--checkpoints", type=str)
parser.add_argument("--save-name", type=str)
parser.add_argument("--weights", type=str)

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
        predictions.append(model({k: v.to("cuda") for k, v in x.items()}).cpu().numpy() * 5 + 1)
    return np.concatenate(predictions, axis=0)


DEBUG = False
# accelerator = Accelerator(mixed_precision="no")
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
# model, dataloader = accelerator.prepare(model, dataloader)

predictions = []
for checkpoint in checkpoints:
    print(f"<<< process: {checkpoint}")
    model.load_state_dict(torch.load(checkpoint, map_location="cpu"))
    prediction = inference(model, dataloader)
    predictions.append(prediction)

# Cache continuous fold predictions before applying the experiment's cutpoints.
# These are test predictions, not OOF validation predictions.
fold_predictions = np.stack([p.reshape(-1) for p in predictions], axis=1)
if fold_predictions.shape != (len(df), len(checkpoints)):
    raise ValueError("Unexpected PET prediction shape")
if not np.isfinite(fold_predictions).all():
    raise ValueError("Non-finite PET predictions")
raw = pd.DataFrame({"essay_id": df["essay_id"].values})
for fold_index in range(len(checkpoints)):
    raw[f"fold_{fold_index}"] = fold_predictions[:, fold_index]
preds = fold_predictions.mean(axis=1)
raw["raw_pred"] = preds
raw.to_csv(args.save_name + ".raw.csv", index=False)
optimized_rounder = OptimizedRounder()
if DEBUG:
    sub = df[["essay_id"]]
else:
    sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")

# --weights contains five ordinal cutpoints, not checkpoint blend weights.
cutpoints = np.asarray(json.loads(args.weights), dtype=float)
if cutpoints.shape != (5,) or not np.all(np.diff(cutpoints) > 0):
    raise ValueError("Expected five strictly increasing score cutpoints")
scored = pd.DataFrame({
    "essay_id": df["essay_id"].values,
    "score": optimized_rounder.predict(preds, cutpoints).astype(int),
})
# Align by ID: test.csv need not have the sample submission's row order.
sub = sub[["essay_id"]].merge(scored, on="essay_id", how="left", validate="one_to_one")
if sub["score"].isna().any() or not sub["score"].between(1, 6).all():
    raise ValueError("Missing or invalid submission scores")
sub["score"] = sub["score"].astype(int)
sub[["essay_id", "score"]].to_csv(args.save_name, index=False)

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

# %% [markdown]
# # exp305

# %%
%%writefile predict_separated.py
import math
import json
import sys
sys.path.append("/kaggle/input/omegaconf")
sys.path.append("/kaggle/input/aes2-code/kaggle-aes2-v2/kaggle-aes2-v2")
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
parser.add_argument("--only-round", default=False, action="store_true")

args, unknown_args = parser.parse_known_args()


def tokenize(example, tokenizer, max_length=1024):
    full_text = example["full_text"]
    truncation = True
    encoding = tokenizer(full_text, return_token_type_ids=False, truncation=truncation, max_length=max_length)

    return {
        "input_ids": encoding["input_ids"],
        "attention_mask": encoding["attention_mask"],
        "length": len(encoding["input_ids"]),
        "is_pc2": 0
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
df["length"] = ds["length"]
ds = ds.sort("length")
sorted_ids = ds["essay_id"]
ds = loc_datasets(ds, ["input_ids", "attention_mask", "is_pc2"])

collate_fn = SequenceBucketPadCollator(max_length=config.train.validate_max_length, tokenizer=tokenizer)
dataloader = torch.utils.data.DataLoader(
    CompetitionDataset(x=ds), batch_size=config.train.batch_size,
    shuffle=False, num_workers=2,
    collate_fn=collate_fn
)
checkpoints = json.loads(args.checkpoints)
# if config.train.exp_name in ["exp302", "exp301"]:
from training.separated.models import AESRegressionModel as ModelClass

model = ModelClass(config).to("cuda")
model.backbone.resize_token_embeddings(len(tokenizer))

predictions = []
for checkpoint in checkpoints:
    print(f"<<< process: {checkpoint}")
    model.load_state_dict(torch.load(checkpoint))
    prediction = inference(model, dataloader)
    predictions.append(prediction)

preds = np.mean(predictions, axis=0).reshape(-1, )
if DEBUG:
    sub = df[["essay_id"]]
else:
    sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")

optimized_rounder = OptimizedRounder()
sub = pd.DataFrame({"essay_id": sorted_ids}).merge(sub, on="essay_id", how="left")
sub.loc[:, "score"] = optimized_rounder.predict(preds, np.array(json.loads(args.weights)))
# sub.loc[:, "score"] = preds.round(0).astype(int)
sub[["essay_id", "score"]].to_csv(args.save_name, index=False)

# %% [markdown]
# # exp307

# %%
%%writefile predict_exp307.py
import math
import json
import sys
sys.path.append("/kaggle/input/omegaconf")
sys.path.append("/kaggle/input/aes2-code/kaggle-aes2-v2.6/kaggle-aes2-v2.6")
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
parser.add_argument("--only-round", default=False, action="store_true")

args, unknown_args = parser.parse_known_args()


def tokenize(example, tokenizer, max_length=1024):
    full_text = example["full_text"]
    truncation = True
    encoding = tokenizer(full_text, return_token_type_ids=False, truncation=truncation, max_length=max_length)

    return {
        "input_ids": encoding["input_ids"],
        "attention_mask": encoding["attention_mask"],
        "length": len(encoding["input_ids"])
    }


def loc_datasets(ds, keep_columns):
    return Dataset.from_dict({col: ds[col] for col in keep_columns})



@torch.no_grad()
def inference(model, dataloader):
    predictions = []
    model.eval()
    for x in tqdm(dataloader, total=len(dataloader)):
        predictions.append(model({key: x[key].to("cuda") for key in x}, do_aux=False).cpu().numpy())
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
df["length"] = ds["length"]
ds = ds.sort("length")
sorted_ids = ds["essay_id"]
ds = loc_datasets(ds, ["input_ids", "attention_mask"])

collate_fn = SequenceBucketPadCollator(max_length=config.train.validate_max_length, tokenizer=tokenizer)
dataloader = torch.utils.data.DataLoader(
    CompetitionDataset(x=ds), batch_size=config.train.batch_size,
    shuffle=False, num_workers=2,
    collate_fn=collate_fn
)
checkpoints = json.loads(args.checkpoints)
# if config.train.exp_name in ["exp302", "exp301"]:
from training.aux.models import AESRegressionModel as ModelClass

model = ModelClass(config).to("cuda")
model.backbone.resize_token_embeddings(len(tokenizer))

predictions = []
for checkpoint in checkpoints:
    print(f"<<< process: {checkpoint}")
    model.load_state_dict(torch.load(checkpoint))
    prediction = inference(model, dataloader)
    predictions.append(prediction)

preds = np.mean(predictions, axis=0).reshape(-1, )
if DEBUG:
    sub = df[["essay_id"]]
else:
    sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")

optimized_rounder = OptimizedRounder()
sub = pd.DataFrame({"essay_id": sorted_ids}).merge(sub, on="essay_id", how="left")
sub.loc[:, "score"] = optimized_rounder.predict(preds, np.array(json.loads(args.weights)))
# sub.loc[:, "score"] = preds.round(0).astype(int)
sub[["essay_id", "score"]].to_csv(args.save_name, index=False)

# %% [markdown]
# # exp306

# %%
%%writefile predict_ordinal.py
import math
import json
import sys
sys.path.append("/kaggle/input/omegaconf")
sys.path.append("/kaggle/input/aes2-code/kaggle-aes2-v3.1/kaggle-aes2-v3.1")
from argparse import ArgumentParser

import datasets
import torch
import torch.utils.data
import numpy as np
import pandas as pd
from accelerate import Accelerator
from datasets import Dataset
from omegaconf import OmegaConf
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AddedToken
from sklearn.preprocessing import MinMaxScaler

from aes2.utils.collators.sequence_bucket import SequenceBucketPadCollator
from aes2.utils.dataset.simple import CompetitionDataset
from aes2.utils.metrics import OptimizedRounder
from aes2.utils.preprocessing import resolve_encodings_and_normalize

parser = ArgumentParser()
parser.add_argument("--config", default=None, required=False)
parser.add_argument("--checkpoints", type=str)
parser.add_argument("--save-name", type=str)
parser.add_argument("--weights", type=str)
parser.add_argument("--only-round", default=False, action="store_true")
parser.add_argument("--do-scale", default=False, action="store_true")

args, unknown_args = parser.parse_known_args()


def tokenize(example, tokenizer, max_length=1024):
    full_text = example["full_text"]
    truncation = True
    encoding = tokenizer(full_text, return_token_type_ids=False, truncation=truncation, max_length=max_length)

    return {
        "input_ids": encoding["input_ids"],
        "attention_mask": encoding["attention_mask"],
        "length": len(encoding["input_ids"]),
        "is_pc2": 0
    }


def loc_datasets(ds, keep_columns):
    return Dataset.from_dict({col: ds[col] for col in keep_columns})



@torch.no_grad()
def inference(model, dataloader):
    predictions = []
    model.eval()
    # .to("cuda")
    for x in tqdm(dataloader, total=len(dataloader)):
        predictions.append(model({key: x[key] for key in x}).sigmoid().sum(dim=-1).cpu().numpy() + 1)
    return np.concatenate(predictions, axis=0)


DEBUG = False
accelerator = Accelerator(mixed_precision="fp16")
config = OmegaConf.load(args.config)
config.merge_with_dotlist(unknown_args)
df = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/test.csv")
df["full_text"] = df["full_text"].apply(resolve_encodings_and_normalize)

tokenizer = AutoTokenizer.from_pretrained(config.model.path)
tokenizer.add_tokens([AddedToken("\n\n", normalized=False)])
tokenizer.add_tokens([AddedToken("\n", normalized=False)])

if DEBUG:
    df["full_text"] = df["full_text"].apply(lambda x: x + "\n" + x + "\n" + x)
    df = pd.concat([df] * 2000, axis=0).reset_index(drop=True)
ds = datasets.Dataset.from_pandas(df)
ds = ds.map(lambda x: tokenize(x, tokenizer, max_length=config.train.validate_max_length), num_proc=2)
df["length"] = ds["length"]
ds = ds.sort("length")
sorted_ids = ds["essay_id"]
ds = loc_datasets(ds, ["input_ids", "attention_mask"])

collate_fn = SequenceBucketPadCollator(max_length=config.train.validate_max_length, tokenizer=tokenizer)
dataloader = torch.utils.data.DataLoader(
    CompetitionDataset(x=ds), batch_size=config.train.batch_size,
    shuffle=False, num_workers=2,
    collate_fn=collate_fn
)
checkpoints = json.loads(args.checkpoints)
# if config.train.exp_name in ["exp302", "exp301"]:
from training.ordinal.models import AESRegressionModel as ModelClass

# .to("cuda")
model = ModelClass(config)
model.backbone.resize_token_embeddings(len(tokenizer))
model, dataloader = accelerator.prepare(model, dataloader)

predictions = []
for checkpoint in checkpoints:
    print(f"<<< process: {checkpoint}")
#     state_dict = 
#     if "head_clf"
    model.load_state_dict(torch.load(checkpoint), strict=False)
    prediction = inference(model, dataloader)
    predictions.append(prediction)

preds = np.mean(predictions, axis=0).reshape(-1, )
if DEBUG:
    sub = df[["essay_id"]]
else:
    sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")

if args.do_scale:
    oof = pd.concat([
        pd.read_csv(f"/kaggle/input/ases-oofs/oof_exp306b_large_clean_last_fold{fold}.csv") 
        for fold in range(4)
    ], axis=0).reset_index(drop=True)
    scaler = MinMaxScaler()
    scaler.fit(oof["raw_pred"].values.reshape(-1, 1))
    preds = scaler.transform(preds.reshape(-1, 1)).reshape(-1, ) * 5 + 1
optimized_rounder = OptimizedRounder()
sub = pd.DataFrame({"essay_id": sorted_ids}).merge(sub, on="essay_id", how="left")
sub.loc[:, "score"] = optimized_rounder.predict(preds, np.array(json.loads(args.weights)))
# sub.loc[:, "score"] = preds.round(0).astype(int)
sub[["essay_id", "score"]].to_csv(args.save_name, index=False)

# %% [markdown]
# # exp311 multiscale

# %%
%%writefile predict_exp311.py
import math
import json
import sys
sys.path.append("/kaggle/input/omegaconf")
sys.path.append("/kaggle/input/aes2-code/kaggle-aes2-v3/kaggle-aes2-v3")
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
from training.multiscale.models import AESRegressionModel as ModelClass
from training.multiscale.yao_datasets import AES2Dataset, NEW_TOKENS
from training.multiscale.collators import CustomDataCollatorWithPadding

parser = ArgumentParser()
parser.add_argument("--config", default=None, required=False)
parser.add_argument("--checkpoints", type=str)
parser.add_argument("--save-name", type=str)
parser.add_argument("--weights", type=str)
parser.add_argument("--only-round", default=False, action="store_true")

args, unknown_args = parser.parse_known_args()


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
df["is_pc2"] = 0
tokenizer = AutoTokenizer.from_pretrained(config.model.path)
tokenizer.add_tokens([AddedToken("\n\n", normalized=False)])
tokenizer.add_tokens([AddedToken("\n", normalized=False)])
for token in NEW_TOKENS:
    tokenizer.add_tokens([AddedToken(token, normalized=False)])

if DEBUG:
    df["full_text"] = df["full_text"].apply(lambda x: x + "\n" + x + "\n" + x)
    df = pd.concat([df] * 2000, axis=0).reset_index(drop=True)
ds = AES2Dataset(config, tokenizer).get_dataset(df, mode="infer")
ds = ds.sort("input_length")
sorted_ids = ds["essay_id"]
ds = loc_datasets(ds, [
    "input_ids", "attention_mask",
    "span_head_idxs", "span_tail_idxs", "sentence_head_idxs", "sentence_tail_idxs", "is_pc2"
])

collate_fn = CustomDataCollatorWithPadding(tokenizer, padding=True, max_length=config.train.validate_max_length)

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
if DEBUG:
    sub = df[["essay_id"]]
else:
    sub = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")

optimized_rounder = OptimizedRounder()
sub = pd.DataFrame({"essay_id": sorted_ids}).merge(sub, on="essay_id", how="left")
sub.loc[:, "score"] = optimized_rounder.predict(preds, np.array(json.loads(args.weights)))
# sub.loc[:, "score"] = preds.round(0).astype(int)
sub[["essay_id", "score"]].to_csv(args.save_name, index=False)

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
# !python inference_topics.py

# %%
# !python predict_exp307.py \
#   --config "/kaggle/input/exp307-large-all/config.yaml" \
#   --checkpoints '["/kaggle/input/exp307-large-all/model_fold0.pth", \
#                   "/kaggle/input/exp307-large-all/model_fold1.pth", \
#                   "/kaggle/input/exp307-large-all/model_fold2.pth", \
#                   "/kaggle/input/exp307-large-all/model_fold3.pth"]' \
#   --save-name "submission.csv" \
#   --weights '[1.6081398, 2.63523588, 3.49321899, 4.21794933, 4.77885755]' \
#   model.path="/kaggle/input/deberta-v3-large/deberta-v3-large"

# %%
# !python predict_separated.py \
#   --config "/kaggle/input/exp305-large-20-all/config.yaml" \
#   --checkpoints '["/kaggle/input/exp305-large-20-all/model_fold0_last.pth", \
#                   "/kaggle/input/exp305-large-20-all/model_fold1_last.pth", \
#                   "/kaggle/input/exp305-large-20-all/model_fold2_last.pth", \
#                   "/kaggle/input/exp305-large-20-all/model_fold3_last.pth"]' \
#   --save-name "submission.csv" \
#   --weights '[1.60461953, 2.54520977, 3.45453864, 4.36134837, 5.29981156]' \
#   model.path="/kaggle/input/deberta-v3-large/deberta-v3-large"

# %%
# Prefer the historical v129 PET ensemble (0.82845) over v136 (0.80526).
# Keep each experiment's own score cutpoints with its checkpoints.
from pathlib import Path
import json
import subprocess
import sys

pet_root = Path("/kaggle/input/exp320-large-last")
pet_backbone = Path("/kaggle/input/deberta-v3-large/deberta-v3-large")
pet_package = Path("/kaggle/input/aes2-code/kaggle-aes2-v3.2/kaggle-aes2-v3.2")
pet_checkpoints = [pet_root / f"model_stage2_fold{fold}_last.pth" for fold in range(4)]
pet_assets = [pet_root / "config.yaml", pet_backbone, pet_package, *pet_checkpoints]
missing_pet_assets = [str(path) for path in pet_assets if not path.exists()]

if not missing_pet_assets:
    # Small batches limit the memory needed by the large backbone; all four
    # fold predictions are still equally averaged before a single rounding.
    command = [
        sys.executable, "predict_pet2.py",
        "--config", str(pet_root / "config.yaml"),
        "--checkpoints", json.dumps([str(path) for path in pet_checkpoints]),
        "--save-name", "submission.csv",
        "--weights", json.dumps([
            1.643716315906825, 2.6716739277111605, 3.5618693723268633,
            4.236181497058755, 4.875353957753833,
        ]),
        f"model.path={pet_backbone}", "model.vocab_size=128003",
        "train.batch_size=4",
    ]
else:
    # The historical datasets may not be attached to every rerun. In that
    # case preserve the complete v136 inference route and its calibration.
    print("Historical PET assets unavailable; using v136 checkpoints:", missing_pet_assets)
    small_root = Path("/kaggle/input/aes2-deberta-v3-small-fit-v5/model/exp305_deberta-v3-small")
    command = [
        sys.executable, "predict_separated.py",
        "--config", str(small_root / "config.yaml"),
        "--checkpoints", json.dumps([str(small_root / f"model_fold{fold}.pth") for fold in range(4)]),
        "--save-name", "submission.csv",
        "--weights", "[1.65, 2.5, 3.5, 4.5, 5.0]",
        "model.path=/kaggle/input/deberta-v3-small/deberta-v3-small",
    ]
# Propagate inference failures rather than accidentally reading a stale CSV.
subprocess.run(command, check=True)

import pandas as pd
sample = pd.read_csv("/kaggle/input/learning-agency-lab-automated-essay-scoring-2/sample_submission.csv")
submission = pd.read_csv("submission.csv")
assert submission.columns.tolist() == ["essay_id", "score"]
assert len(submission) == len(sample)
assert submission["essay_id"].is_unique
assert set(submission["essay_id"]) == set(sample["essay_id"])
assert submission["score"].notna().all()
assert submission["score"].between(1, 6).all()
assert (submission["score"] == submission["score"].astype(int)).all()
submission = sample[["essay_id"]].merge(submission, on="essay_id", how="left", validate="one_to_one")
submission["score"] = submission["score"].astype(int)
submission.to_csv("submission.csv", index=False)

# %%
# !python predict_ordinal.py \
#   --config "/kaggle/input/exp306b-large-clean-last/config.yaml" \
#   --checkpoints '["/kaggle/input/exp306b-large-clean-last/model_stage2_fold0_last.pth", \
#                   "/kaggle/input/exp306b-large-clean-last/model_stage2_fold1_last.pth", \
#                   "/kaggle/input/exp306b-large-clean-last/model_stage2_fold2_last.pth", \
#                   "/kaggle/input/exp306b-large-clean-last/model_stage2_fold3_last.pth"]' \
#   --save-name "submission.csv" \
#   --weights '[1.65, 2.5, 3.5, 4.5, 5]' \
#   model.path="/kaggle/input/deberta-v3-large/deberta-v3-large"

# %%
# !python predict_ordinal.py \
#   --config "/kaggle/input/exp306-hybrid-large-best-last/config.yaml" \
#   --checkpoints '["/kaggle/input/exp306-hybrid-large-best-last/model_stage2_fold0_last.pth", \
#                   "/kaggle/input/exp306-hybrid-large-best-last/model_stage2_fold1_last.pth", \
#                   "/kaggle/input/exp306-hybrid-large-best-last/model_stage2_fold2_last.pth", \
#                   "/kaggle/input/exp306-hybrid-large-best-last/model_stage2_fold3_last.pth"]' \
#   --save-name "submission.csv" \
#   --weights '[1.63965464, 2.75965951, 3.65114977, 4.1301192, 5.25276228]' \
#   model.path="/kaggle/input/deberta-v3-large/deberta-v3-large" train.hyper_loss_factor=0

# %%
# !python predict_pet.py \
#   --config "/kaggle/input/exp303-ts-large-all/config.yaml" \
#   --checkpoints '["/kaggle/input/exp303-ts-large-all/model_stage2_fold0_last.pth", \
#                   "/kaggle/input/exp303-ts-large-all/model_stage2_fold1_last.pth", \
#                   "/kaggle/input/exp303-ts-large-all/model_stage2_fold2_last.pth", \
#                   "/kaggle/input/exp303-ts-large-all/model_stage2_fold3_last.pth"]' \
#   --save-name "submission.csv" \
#   --weights '[1.6899917656288044, 2.670228386942341, 3.5610759259845897, 4.278530651773558, 4.788715093068903]' \
#   model.path="/kaggle/input/deberta-v3-large/deberta-v3-large" model.vocab_size=128003

# %%
# !python predict_exp302.py \
#   --config "/kaggle/input/exp302c-large-stage2-only/config.yaml" \
#   --checkpoints '["/kaggle/input/exp302c-large-stage2-only/model_stage2_fold0_last.pth", \
#                   "/kaggle/input/exp302c-large-stage2-only/model_stage2_fold1_last.pth", \
#                   "/kaggle/input/exp302c-large-stage2-only/model_stage2_fold2_last.pth", \
#                   "/kaggle/input/exp302c-large-stage2-only/model_stage2_fold3_last.pth"]' \
#   --save-name "submission.csv" \
#   --weights '[1.6437270064380882, 2.6365439680164733, 3.442908801623126, 4.235570569253413, 4.842800253947775]' \
#   model.n_labels=1 train.use_cope=false \
#   model.path="/kaggle/input/deberta-v3-large/deberta-v3-large" train.batch_size=16

# %%
# !python predict_exp302.py \
#   --config "/kaggle/input/exp302c-large-scale-best/config.yaml" \
#   --checkpoints '["/kaggle/input/exp302c-large-scale-best/model_stage2_fold0_last.pth", \
#                   "/kaggle/input/exp302c-large-scale-best/model_stage2_fold1_last.pth", \
#                   "/kaggle/input/exp302c-large-scale-best/model_stage2_fold2_last.pth", \
#                   "/kaggle/input/exp302c-large-scale-best/model_stage2_fold3_last.pth"]' \
#   --save-name "submission.csv" \
#   --weights '[1.6702797426175757, 2.6972164719001857, 3.543557859315139, 4.245659402744927, 4.767272513916463]' \
#   model.n_labels=1 train.use_cope=false \
#   model.path="/kaggle/input/deberta-v3-large/deberta-v3-large" train.batch_size=16

# %%
# !python predict_exp311.py \
#   --config "/kaggle/input/exp311-large-sep-multiscale-f0/config.yaml" \
#   --checkpoints '["/kaggle/input/exp311-large-sep-multiscale-f0/model_fold0.pth"]' \
#   --save-name "submission.csv" \
#   --weights '[1.66259118, 2.47181552, 3.27396093, 4.13196292, 4.97328433]' \
#   model.path="/kaggle/input/deberta-v3-large/deberta-v3-large" train.batch_size=16

# %%
# !python predict_exp302.py \
#   --config "/kaggle/input/exp301-topic-large-all/config.yaml" \
#   --checkpoints '["/kaggle/input/exp301-topic-large-all/model_fold0.pth", \
#                   "/kaggle/input/exp301-topic-large-all/model_fold1.pth", \
#                   "/kaggle/input/exp301-topic-large-all/model_fold2.pth", \
#                   "/kaggle/input/exp301-topic-large-all/model_fold3.pth"]' \
#   --save-name "submission.csv" \
#   --weights '[1.5301733266231725, 2.3623673976652846, 3.2269907989706814, 4.145971216130041, 6.026585374097247]' \
#   model.path="/kaggle/input/deberta-v3-large/deberta-v3-large" train.batch_size=16

# %%
# !python predict_pet2.py \
#   --config "/kaggle/input/exp320-large-last/config.yaml" \
#   --checkpoints '["/kaggle/input/exp320-large-last/model_stage2_fold0_last.pth", \
#                   "/kaggle/input/exp320-large-last/model_stage2_fold1_last.pth", \
#                   "/kaggle/input/exp320-large-last/model_stage2_fold2_last.pth", \
#                   "/kaggle/input/exp320-large-last/model_stage2_fold3_last.pth"]' \
#   --save-name "submission.csv" \
#   --weights '[1.643716315906825, 2.6716739277111605, 3.5618693723268633, 4.236181497058755, 4.875353957753833]' \
#   model.path="/kaggle/input/deberta-v3-large/deberta-v3-large" model.vocab_size=128003

# %%
import pandas as pd


# display(pd.read_csv("topics.csv"))
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


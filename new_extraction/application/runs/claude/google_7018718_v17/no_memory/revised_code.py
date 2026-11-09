# %%
!cp -r /kaggle/input/google-qa-libs/projects/kaggle_google_qa_labeling/kaggle_google_qa_labeling ./
!cp -r /kaggle/input/google-qa-libs/projects/prompter/prompter ./
!cp -r /kaggle/input/google-qa-experiments/projects/kaggle_google_qa_labeling/experiments/* ./
!cp -r /kaggle/input/transformersdependencies/dependencies/* ./

# %%
# NOTE: v17 deleted fold_models/model_0..model_5 before inference, which shrank the
# fold ensemble and dropped the score from 0.38513 (v16) to 0.37427. The deletions are
# removed here so that all fold models are blended again.
!ls ./2019_12_15__12_28_32__384/fold_models/

# %%
from pathlib import Path

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data.dataloader import DataLoader

from prompter.Factory import Factory
from prompter.learner.Learner import Learner

from kaggle_google_qa_labeling.evaluator.Evaluator import Evaluator
from kaggle_google_qa_labeling.dataset.cross_dataset_utilities import *
from kaggle_google_qa_labeling.dataset.BiDataset import BiDataset
from kaggle_google_qa_labeling.evaluator.BiEncoderEvaluator import BiEncoderEvaluator

# %%
train_df = pd.read_csv('/kaggle/input/google-quest-challenge/train.csv')
test_df = pd.read_csv('/kaggle/input/google-quest-challenge/test.csv')
subm_df = pd.read_csv('/kaggle/input/google-quest-challenge/sample_submission.csv')
target_cols = list(subm_df.columns[1:])

# %%
experiment_dir = Path('2019_12_15__12_28_32__384')
evaluator = BiEncoderEvaluator(experiment_dir=experiment_dir, device='cuda', bs=16, blend_strategy='sigmoid', models_dir_name='fold_models')

# %%
y_pred = evaluator.run(test_df)
y_pred = np.asarray(y_pred, dtype=np.float64)
y_pred = np.nan_to_num(y_pred, nan=0.5)

# %%
# Spearman-oriented post-processing.
# The metric is mean column-wise Spearman correlation, so only the ranking inside each
# column matters. Many targets take only a handful of discrete levels (averages of a few
# raters) and are heavily tied. Quantile-mapping each prediction column onto the empirical
# train distribution of that target preserves the model's ranking but reproduces the train
# tie structure: samples the model considers near-identical are tied instead of being
# ordered by noise. This is applied only to strongly discrete / skewed columns, with a
# guard that never collapses a column to a single constant value (Spearman would be NaN).

def quantile_map_to_train(pred, train_vals, max_unique=12, min_unique_out=2):
    pred = np.asarray(pred, dtype=np.float64)
    train_vals = np.asarray(train_vals, dtype=np.float64)
    if len(np.unique(train_vals)) > max_unique:
        return pred
    # empirical train distribution (sorted levels + cumulative proportions)
    levels, counts = np.unique(train_vals, return_counts=True)
    cum = np.cumsum(counts) / counts.sum()
    # ranks of predictions in (0, 1]; average ranks keep model ties as ties
    order = pd.Series(pred).rank(method='average').values / len(pred)
    idx = np.searchsorted(cum, order - 1e-12, side='left')
    idx = np.clip(idx, 0, len(levels) - 1)
    mapped = levels[idx]
    if len(np.unique(mapped)) < min_unique_out:
        return pred
    return mapped


y_post = y_pred.copy()
for j, col in enumerate(target_cols):
    if col in train_df.columns:
        y_post[:, j] = quantile_map_to_train(y_pred[:, j], train_df[col].values)

# Safety: any column that ended up constant falls back to the raw (clipped) prediction.
for j in range(y_post.shape[1]):
    if len(np.unique(y_post[:, j])) < 2:
        y_post[:, j] = y_pred[:, j]

y_post = np.clip(y_post, 0.0, 1.0)

# %%
out_df = pd.DataFrame(columns=subm_df.columns)
out_df['qa_id'] = test_df['qa_id'].values
out_df.iloc[:, 1:] = y_post
out_df[target_cols] = out_df[target_cols].astype(float)
out_df.to_csv('submission.csv', index=False)
out_df.head()

# %%


# %%


# %%


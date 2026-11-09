# %%
!cp -r /kaggle/input/google-qa-libs/projects/kaggle_google_qa_labeling/kaggle_google_qa_labeling ./
!cp -r /kaggle/input/google-qa-libs/projects/prompter/prompter ./
!cp -r /kaggle/input/google-qa-experiments/projects/kaggle_google_qa_labeling/experiments/* ./
!cp -r /kaggle/input/transformersdependencies/dependencies/* ./

# %%
# NOTE: v17 deleted fold_models/model_0..model_5 before inference, which removed
# most of the fold ensemble and dropped the score from 0.38513 to 0.37427.
# All fold models are kept here so the evaluator averages over the full ensemble.
!ls ./2019_12_15__12_28_32__384/fold_models/

# %%
from pathlib import Path

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data.dataloader import DataLoader
from scipy.stats import rankdata

from prompter.Factory import Factory
from prompter.learner.Learner import Learner

from kaggle_google_qa_labeling.evaluator.Evaluator import Evaluator
from kaggle_google_qa_labeling.dataset.cross_dataset_utilities import *
from kaggle_google_qa_labeling.dataset.BiDataset import BiDataset
from kaggle_google_qa_labeling.evaluator.BiEncoderEvaluator import BiEncoderEvaluator

# %%
test_df = pd.read_csv('/kaggle/input/google-quest-challenge/test.csv')
subm_df = pd.read_csv('/kaggle/input/google-quest-challenge/sample_submission.csv')
train_df = pd.read_csv('/kaggle/input/google-quest-challenge/train.csv')
target_cols = list(subm_df.columns[1:])

# %%
experiment_dir = Path('2019_12_15__12_28_32__384')
evaluator = BiEncoderEvaluator(experiment_dir=experiment_dir, device='cuda', bs=16, blend_strategy='sigmoid', models_dir_name='fold_models')

# %%
y_pred = np.asarray(evaluator.run(test_df), dtype=np.float64)
y_pred = np.nan_to_num(y_pred, nan=0.5)

# %%
# Post-processing for mean column-wise Spearman.
# 1) Rank-transform each column to a uniform [0,1] scale (Spearman-invariant, keeps
#    predictions in the required range and removes any scale drift between columns).
# 2) For columns whose training distribution is dominated by a single value (very
#    sparse/skewed labels), collapse the lowest-ranked predictions into a single tie
#    at the training frequency of the dominant value. Ties within the dominant group
#    reduce rank noise where the model has no real signal, which raises Spearman.
def rank_to_unit(x):
    r = rankdata(x, method='average')
    return (r - 1.0) / max(len(r) - 1.0, 1.0)

n_test = y_pred.shape[0]
post = np.zeros_like(y_pred)
for j, col in enumerate(target_cols):
    col_pred = rank_to_unit(y_pred[:, j])
    tr = train_df[col].values
    vals, counts = np.unique(tr, return_counts=True)
    dom_val = vals[np.argmax(counts)]
    dom_frac = counts.max() / len(tr)
    # Only tie when the dominant class is very large and sits at an extreme (0 or 1),
    # and apply a conservative fraction (shrunk towards the data) to avoid over-tying.
    if dom_frac >= 0.80 and n_test > 10 and (dom_val <= 0.05 or dom_val >= 0.95):
        tie_frac = 0.5 * dom_frac
        k = int(np.floor(tie_frac * n_test))
        if k >= 2:
            order = np.argsort(y_pred[:, j], kind='mergesort')
            if dom_val <= 0.05:
                idx = order[:k]           # lowest predictions -> tie at bottom
                col_pred[idx] = col_pred[idx].min()
            else:
                idx = order[-k:]          # highest predictions -> tie at top
                col_pred[idx] = col_pred[idx].max()
    post[:, j] = col_pred

# Keep predictions strictly inside [0, 1]
post = np.clip(post, 0.0, 1.0)

# %%
out_df = pd.DataFrame(columns=subm_df.columns)
out_df['qa_id'] = test_df['qa_id']
out_df.iloc[:, 1:] = post
out_df.to_csv('submission.csv', index=False)

# %%
print(out_df.shape)
print(out_df.head())

# %%


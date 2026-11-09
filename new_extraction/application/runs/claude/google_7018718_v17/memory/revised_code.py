# %%
!cp -r /kaggle/input/google-qa-libs/projects/kaggle_google_qa_labeling/kaggle_google_qa_labeling ./
!cp -r /kaggle/input/google-qa-libs/projects/prompter/prompter ./
!cp -r /kaggle/input/google-qa-experiments/projects/kaggle_google_qa_labeling/experiments/* ./
!cp -r /kaggle/input/transformersdependencies/dependencies/* ./

# %%
# v16 (best score, 0.38513) kept all fold models; v17 deleted model_0..model_5 and
# regressed by 0.011. The deletions are removed so the full fold ensemble is used.
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
test_df = pd.read_csv('/kaggle/input/google-quest-challenge/test.csv')
subm_df = pd.read_csv('/kaggle/input/google-quest-challenge/sample_submission.csv')

# %%
experiment_dir = Path('2019_12_15__12_28_32__384')
evaluator = BiEncoderEvaluator(experiment_dir=experiment_dir, device='cuda', bs=16, blend_strategy='sigmoid', models_dir_name='fold_models')

# %%
y_pred = evaluator.run(test_df)

# %%
y_pred = np.asarray(y_pred, dtype=np.float64)
y_pred = np.nan_to_num(y_pred, nan=0.5)
# Spearman is rank-based, so clipping to the required [0,1] range cannot hurt ordering
y_pred = np.clip(y_pred, 0.0, 1.0)
assert y_pred.shape == (len(test_df), len(subm_df.columns) - 1), y_pred.shape

# %%
target_cols = list(subm_df.columns[1:])
out_df = pd.DataFrame(y_pred, columns=target_cols)
out_df.insert(0, 'qa_id', test_df['qa_id'].values)
out_df.to_csv('submission.csv', index=False)
print(out_df.shape)
out_df.head()

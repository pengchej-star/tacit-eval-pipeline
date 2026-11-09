# %%
!cp -r /kaggle/input/google-qa-libs/projects/kaggle_google_qa_labeling/kaggle_google_qa_labeling ./
!cp -r /kaggle/input/google-qa-libs/projects/prompter/prompter ./
!cp -r /kaggle/input/google-qa-experiments/projects/kaggle_google_qa_labeling/experiments/* ./
!cp -r /kaggle/input/transformersdependencies/dependencies/* ./

# %%
# Keep every supplied fold checkpoint in the inference ensemble.
# Removing model_0 through model_5 reduced the recorded score in v17.

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
out_df = pd.DataFrame(columns=subm_df.columns)
out_df['qa_id'] = test_df['qa_id']
out_df.iloc[:,1:] = y_pred
out_df.to_csv('submission.csv', index=False)

# %%


# %%


# %%


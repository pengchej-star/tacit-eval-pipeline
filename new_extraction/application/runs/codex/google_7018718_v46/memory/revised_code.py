# %%
!cp -r /kaggle/input/google-qa-libs/* ./
!cp -r /kaggle/input/2020-02-01-19-10-50-329/* ./
!cp -r /kaggle/input/transformersdependencies/dependencies/* ./
!cp -r /kaggle/input/google-qa-ner/* ./

# %%


# %%
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
import torch
import torch.nn as nn
from torch.utils.data.dataloader import DataLoader

from kaggle_google_qa_labeling.ner_detector import NERDetector
from kaggle_google_qa_labeling.evaluator.bi_encoder_evaluator import BiEncoderEvaluator

# %%


# %%


# %%
test_df = pd.read_csv('/kaggle/input/google-quest-challenge/test.csv')
subm_df = pd.read_csv('/kaggle/input/google-quest-challenge/sample_submission.csv')

# %%
ner_model = NERDetector.from_model_dir(model_dir=Path('./ner/code/bert_base_cased/'), device='cuda', bs=64, threshold=0.8, min_span_len=10)
# ner_model = None
process_math = True

# %%
experiment_dir = Path('2020_02_01__19_10_50__329')
# evaluator = CrossEncoderEvaluator(
#     experiment_dir=experiment_dir, device='cuda', bs=16, blend_strategy='mean', models_dir_name='fold_models', ner_model=ner_model, process_math=process_math
# )
evaluator = BiEncoderEvaluator(
    experiment_dir=experiment_dir, device='cuda', bs=16, blend_strategy='mean', models_dir_name='fold_models', ner_model=ner_model, process_math=process_math
)

# %%
y_pred = np.asarray(evaluator.run(test_df), dtype=np.float64)

# Restore explicit tie-producing postprocessing after the fold ensemble.
# Historical discretized submissions substantially outscored raw submissions.
# Five uniform bins are a deliberately simple candidate: the exact old bin
# settings are not recorded in history.md. Keep the v46 checkpoint/preprocessing.
N_BINS = 5

def discretize_predictions(predictions):
    result = predictions.copy()
    for column in range(predictions.shape[1]):
        values = predictions[:, column]
        # Avoid fitting bins to constant or numerically degenerate predictions.
        if np.ptp(values) <= 1e-8:
            continue
        discretizer = KBinsDiscretizer(
            n_bins=N_BINS, encode='ordinal', strategy='uniform'
        )
        # Fit on this prediction column, using no test labels. Equal-width
        # probability intervals retain larger gaps while tying nearby scores.
        binned = discretizer.fit_transform(values.reshape(-1, 1)).ravel()
        span = np.ptp(binned)
        if span > 0 and np.isfinite(binned).all():
            result[:, column] = (binned - binned.min()) / span
        # Otherwise keep the original continuous column, as in v38/v45.
    return np.clip(result, 0.0, 1.0)


target_columns = subm_df.columns[1:].tolist()
assert y_pred.shape == (len(test_df), len(target_columns)), y_pred.shape
assert np.isfinite(y_pred).all(), 'Evaluator produced nonfinite predictions'
assert test_df['qa_id'].is_unique, 'Duplicate test qa_id'
assert subm_df['qa_id'].is_unique, 'Duplicate sample submission qa_id'
assert set(test_df['qa_id']) == set(subm_df['qa_id']), 'Submission ID mismatch'

# Save the unmodified ensemble as a diagnostic for the next scored comparison.
raw_df = pd.DataFrame(np.clip(y_pred, 0.0, 1.0), columns=target_columns)
raw_df.insert(0, 'qa_id', test_df['qa_id'].to_numpy())
raw_df = raw_df.set_index('qa_id').loc[subm_df['qa_id']].reset_index()
raw_df.to_csv('submission_raw.csv', index=False)
y_pred_new = discretize_predictions(y_pred)

# %%


# %%


# %%


# %%


# %%
out_df = pd.DataFrame(y_pred_new, columns=target_columns)
out_df.insert(0, 'qa_id', test_df['qa_id'].to_numpy())
out_df = out_df.set_index('qa_id').loc[subm_df['qa_id']].reset_index()
out_df = out_df.loc[:, subm_df.columns]
assert np.isfinite(out_df[target_columns].to_numpy()).all()
assert out_df[target_columns].ge(0).all().all()
assert out_df[target_columns].le(1).all().all()
out_df.to_csv('submission.csv', index=False)

# %%


# %%


# %%


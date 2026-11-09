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
y_pred = evaluator.run(test_df)

# %%


# %%


# %%


# %%


# %%
# Spearman evaluates ties as well as ordering. The supplied history shows
# substantially stronger results with discretization than with raw sigmoids.
# Keep inference unchanged and restore a small, fixed ordinal postprocessor.
# Five equal-width bins are a new explicit choice: the history does not retain
# the old discretizer's parameters. Do not fit bins across different targets.
N_BINS = 5


def discretize_predictions(predictions, n_bins=5):
    """Per-target uniform bins, retaining continuous values on collapse.

    Fit each column's bin edges on its own prediction range, as a uniform
    ordinal KBinsDiscretizer would. This only uses unlabeled predictions.
    Return actual tied scores; adding continuous tie breakers would undo the
    intended change to Spearman correlation.
    """
    if n_bins < 2:
        raise ValueError('n_bins must be at least two')
    values = np.asarray(predictions, dtype=np.float64)
    if values.ndim != 2:
        raise ValueError('Predictions must be a two-dimensional matrix')
    if not np.isfinite(values).all():
        raise ValueError('Model predictions contain non-finite values')
    values = np.clip(values, 0.0, 1.0)
    result = values.copy()
    if len(values) < 2:
        return result
    for column in range(values.shape[1]):
        raw = values[:, column]
        low, high = raw.min(), raw.max()
        # Avoid amplifying numerical noise in effectively constant columns.
        if high - low <= 1e-8:
            continue
        edges = np.linspace(low, high, n_bins + 1)
        ordinal = np.searchsorted(edges[1:-1], raw, side='right')
        occupied = np.unique(ordinal)
        if len(occupied) < 2:
            continue
        result[:, column] = (
            (ordinal - occupied[0]) / float(occupied[-1] - occupied[0])
        )
    return result


target_columns = subm_df.columns[1:].tolist()
# The packaged evaluator already returns predictions in submission order,
# as assumed by the original pipeline.
y_pred = np.asarray(y_pred)
if y_pred.shape != (len(test_df), len(target_columns)):
    raise ValueError('Unexpected prediction shape: {}'.format(y_pred.shape))
y_pred_new = discretize_predictions(y_pred, n_bins=N_BINS)

# Keep a raw reference for future validation without a second model pass.
raw_out_df = pd.DataFrame(np.clip(y_pred, 0.0, 1.0), columns=target_columns)
raw_out_df.insert(0, 'qa_id', test_df['qa_id'].to_numpy())
raw_out_df.to_csv('submission_raw.csv', index=False)

out_df = pd.DataFrame(y_pred_new, columns=target_columns)
out_df.insert(0, 'qa_id', test_df['qa_id'].to_numpy())
out_df = out_df.loc[:, subm_df.columns]
out_df.to_csv('submission.csv', index=False)

# %%


# %%


# %%


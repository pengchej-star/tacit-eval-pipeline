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
y_pred = np.asarray(evaluator.run(test_df), dtype=np.float64)
target_columns = subm_df.columns.drop('qa_id').tolist()
if y_pred.shape != (len(test_df), len(target_columns)):
    raise ValueError('Evaluator predictions do not match the submission shape: %r' % (y_pred.shape,))
if not np.isfinite(y_pred).all():
    raise ValueError('Evaluator returned non-finite predictions')
# Retain the fold ensemble before postprocessing for reproducible comparisons.
np.save('predictions_raw.npy', y_pred)

# %%


# %%


# %%


# %%


# %%
# Restore the tied-rank postprocessing that was removed in v46.
# Spearman uses average ranks for ties: this is intentionally a discretization,
# not just a monotone rescaling (which would leave the score unchanged).
# Earlier exact bin settings are unavailable; explicitly use five quantile bins.
# Work on the complete test set, after fold averaging, never per inference batch.
def discretize_predictions(predictions, n_bins=5):
    result = predictions.copy()
    for column_index in range(predictions.shape[1]):
        values = predictions[:, column_index]
        if len(values) < 2 or np.ptp(values) <= 1e-8:
            continue
        # Deterministic equivalent of ordinal quantile KBinsDiscretizer,
        # with no version-dependent fitting subsample or new dependency.
        edges = np.percentile(values, np.linspace(0.0, 100.0, n_bins + 1))
        edges = edges[np.r_[True, np.diff(edges) > 1e-8]]
        if len(edges) < 3:
            continue
        binned = np.searchsorted(edges[1:-1], values, side='right').astype(np.float64)
        spread = np.ptp(binned)
        # Preserve the continuous column if quantization collapses it, as in v45.
        if spread == 0:
            continue
        result[:, column_index] = (binned - binned.min()) / spread
    return np.clip(result, 0.0, 1.0)


y_pred_new = discretize_predictions(y_pred, n_bins=5)
np.save('predictions_discretized.npy', y_pred_new)

# Align by qa_id, including when sample_submission and test have different orders.
if not test_df['qa_id'].is_unique or not subm_df['qa_id'].is_unique:
    raise ValueError('qa_id must be unique')
if set(test_df['qa_id']) != set(subm_df['qa_id']):
    raise ValueError('Test and submission IDs do not match')
prediction_df = pd.DataFrame(y_pred_new, index=test_df['qa_id'], columns=target_columns)
out_df = subm_df.copy()
out_df[target_columns] = prediction_df.loc[subm_df['qa_id'], target_columns].to_numpy()
if not np.isfinite(out_df[target_columns].to_numpy()).all():
    raise ValueError('Submission contains non-finite predictions')
out_df.to_csv('submission.csv', index=False)

# %%


# %%


# %%


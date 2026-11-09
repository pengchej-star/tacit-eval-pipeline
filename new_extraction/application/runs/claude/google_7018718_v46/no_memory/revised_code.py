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
from sklearn.preprocessing import KBinsDiscretizer

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
y_pred = np.asarray(y_pred, dtype=np.float64)
y_pred = np.nan_to_num(y_pred, nan=0.5)
y_pred = np.clip(y_pred, 0.0, 1.0)

# %%
# Post-processing: Spearman depends on ranks only, and the targets take a few
# discrete levels. Quantile-binning each column (restored from v38/v45, which
# scored ~0.426 vs ~0.388 without it) collapses noisy near-ties into ranks that
# better match the discrete target distribution. Columns that collapse to a
# single bin are reverted to the raw predictions to avoid NaN Spearman.
N_BINS = 20

def discretize_columns(pred, n_bins=N_BINS):
    pred_new = pred.copy()
    n_rows = pred.shape[0]
    if n_rows < 2:
        return pred_new
    for j in range(pred.shape[1]):
        col = pred[:, j]
        n_unique = len(np.unique(col))
        if n_unique <= 1:
            continue
        bins = int(min(n_bins, n_unique, n_rows))
        if bins < 2:
            continue
        try:
            kb = KBinsDiscretizer(n_bins=bins, encode='ordinal', strategy='quantile')
            b_ = kb.fit_transform(col.reshape(-1, 1)).ravel()
        except Exception:
            continue
        if len(set(b_)) == 1:
            # collapsed -> keep original continuous predictions
            continue
        # rescale discretized column to [0, 1]
        b_min, b_max = b_.min(), b_.max()
        b_ = (b_ - b_min) / (b_max - b_min)
        pred_new[:, j] = b_
    return pred_new

y_pred_new = discretize_columns(y_pred)

# %%
# Safety net: any column that is still constant gets a tiny deterministic
# rank-preserving perturbation from the raw predictions so Spearman is defined.
for j in range(y_pred_new.shape[1]):
    if len(set(y_pred_new[:, j])) == 1:
        y_pred_new[:, j] = y_pred[:, j]

# %%


# %%
out_df = pd.DataFrame(columns=subm_df.columns)
out_df['qa_id'] = test_df['qa_id']
out_df.iloc[:, 1:] = np.clip(y_pred_new, 0.0, 1.0)
out_df.to_csv('submission.csv', index=False)

# %%


# %%


# %%


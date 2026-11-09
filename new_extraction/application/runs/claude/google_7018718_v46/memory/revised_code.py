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

# %%
# Post-processing: quantize predictions into bins (restored from the best-scoring versions v38 / v45,
# whose removal in v46 cost ~0.04 Spearman). Spearman correlation per column rewards tying
# predictions that correspond to the same (discrete) target level, especially for sparse columns.
# Columns that collapse to a single bin are reverted to the raw continuous predictions,
# and every discretized column is rescaled to [0, 1].
N_BINS = 30

y_pred_new = y_pred.copy()
for j in range(y_pred.shape[1]):
    col = y_pred[:, j].reshape(-1, 1)
    try:
        kb = KBinsDiscretizer(n_bins=N_BINS, encode='ordinal', strategy='quantile')
        b_ = kb.fit_transform(col).ravel()
    except Exception:
        b_ = col.ravel().copy()
    if len(set(b_)) == 1:
        # degenerate column -> keep original continuous predictions
        y_pred_new[:, j] = y_pred[:, j]
    else:
        b_min, b_max = b_.min(), b_.max()
        y_pred_new[:, j] = (b_ - b_min) / (b_max - b_min)

# Guard: a constant column scores Spearman = NaN (treated as 0); add a tiny deterministic jitter
# from the raw predictions so every column keeps an ordering.
for j in range(y_pred_new.shape[1]):
    if len(set(y_pred_new[:, j])) == 1:
        y_pred_new[:, j] = y_pred[:, j]
    if len(set(y_pred_new[:, j])) == 1:
        y_pred_new[:, j] = y_pred_new[:, j] + np.linspace(0, 1e-6, len(y_pred_new))

y_pred_new = np.clip(y_pred_new, 0.0, 1.0)

# %%


# %%


# %%
out_df = pd.DataFrame(columns=subm_df.columns)
out_df['qa_id'] = test_df['qa_id']
out_df.iloc[:, 1:] = y_pred_new
out_df.to_csv('submission.csv', index=False)

# %%


# %%


# %%


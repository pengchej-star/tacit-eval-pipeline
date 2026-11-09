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
from scipy.stats import rankdata
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
# Post-processing (restored from v38-v45, which scored ~0.425 vs ~0.385 without it).
# Spearman is rank based and the targets take only a few discrete levels, so
# discretizing each predicted column into quantile bins (creating ties where the
# model is unsure) improves the metric. Columns that collapse to a single bin are
# reverted to the raw continuous predictions; every column is min-max scaled to [0, 1].
N_BINS = 20

def discretize_column(col, n_bins=N_BINS):
    col = col.reshape(-1, 1)
    n_unique = len(np.unique(col))
    if n_unique < 2:
        return col.ravel()
    n_bins = int(min(n_bins, n_unique))
    try:
        kb = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy='quantile')
        out = kb.fit_transform(col).ravel()
    except Exception:
        return col.ravel()
    if len(set(out)) == 1:
        return col.ravel()
    return out

y_pred_new = y_pred.copy()
for j in range(y_pred.shape[1]):
    y_pred_new[:, j] = discretize_column(y_pred[:, j])

# %%
# Min-max rescale each column into [0, 1] (required submission range).
for j in range(y_pred_new.shape[1]):
    c = y_pred_new[:, j]
    cmin, cmax = c.min(), c.max()
    if cmax - cmin > 0:
        y_pred_new[:, j] = (c - cmin) / (cmax - cmin)
    else:
        # fall back to rank-scaled raw predictions so the column is not constant
        r = rankdata(y_pred[:, j])
        y_pred_new[:, j] = (r - r.min()) / max(r.max() - r.min(), 1.0)

y_pred_new = np.clip(y_pred_new, 0.0, 1.0)

# %%
out_df = pd.DataFrame(columns=subm_df.columns)
out_df['qa_id'] = test_df['qa_id']
out_df.iloc[:,1:] = y_pred_new
out_df.to_csv('submission.csv', index=False)

# %%


# %%

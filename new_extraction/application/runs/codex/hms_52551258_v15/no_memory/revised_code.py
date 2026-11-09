# %%
from tqdm.auto import tqdm
import pandas as pd
import polars as pl
import numpy as np
import os
import sys
import glob
import math
from typing import Union, Tuple, List

import torch
import torch.nn as nn
from scipy.signal import butter, filtfilt

# %%
DATA_DIR = "/kaggle/input/hms-harmful-brain-activity-classification/"
SPEC_DIR = os.path.join(DATA_DIR, "test_spectrograms/")
EEG_DIR = os.path.join(DATA_DIR, "test_eegs/")

df_train = pl.read_csv(os.path.join(DATA_DIR, "train.csv"))
df_test = pl.read_csv(os.path.join(DATA_DIR, "test.csv"))
sample_submission = pl.read_csv(os.path.join(DATA_DIR, "sample_submission.csv"))

LABELS = [
    "seizure_vote", "lpd_vote", "gpd_vote",
    "lrda_vote", "grda_vote", "other_vote"
]
EEG_COLUMNS = [
    "Fp1", "Fp2", "F3", "F4", "F7", "F8", "C3", "C4",
    "P3", "P4", "T3", "T4", "T5", "T6", "O1", "O2"
]

# %%
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)


def load_model(path: str, model: nn.Module) -> nn.Module:
    checkpoint = torch.load(path, map_location=torch.device("cpu"))
    model.load_state_dict(checkpoint["model_state_dict"])
    return model.to(device).eval()

# %%
sys.path.append("/kaggle/input/hms-models/")
from eeg_cnn_rnn_w1 import EegModel as EegModel0
from eeg_cnn_rnn import EegModel as EegModel1

# Restore the raw-EEG ensemble supported by v13's leaderboard result.
# Preserve equal per-checkpoint weighting and each family's original inputs.
model_0_files = sorted(set(
    glob.glob("/kaggle/input/hms-models/new_distil/send_kaggle/*") +
    glob.glob("/kaggle/input/hms-models/new_fold/send_kaggle/*")
))
model_0_files = [path for path in model_0_files if os.path.isfile(path)]
model_1_files = [
    os.path.join(path, "model_best_val_g10.pt")
    for path in sorted(glob.glob("/kaggle/input/hms-models/baseline_eeg_diff/*"))
    if os.path.isdir(path)
]
assert model_0_files, "No eeg_cnn_rnn_w1 checkpoints found"
assert model_1_files, "No baseline_eeg_diff fold directories found"
for path in model_1_files:
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

models_0 = [load_model(path, EegModel0()) for path in model_0_files]
models_1 = [load_model(path, EegModel1()) for path in model_1_files]
print(f"Loaded {len(models_0)} w1 and {len(models_1)} baseline EEG models")

# %%
def butter_filter(eeg_data, fs=200, cutoff_freq=22, order=4, btype="lowpass"):
    b, a = butter(
        N=order, Wn=cutoff_freq / (0.5 * fs), btype=btype, analog=False
    )
    return filtfilt(b, a, eeg_data)

# %%
def bin_array(
    array, 
    bin_size, 
    axis = -1, 
    pad_dir = "symmetric", 
    mode = "edge", 
    return_padding = False,
    **padding_kwargs
) -> Union[np.ndarray, Tuple[np.ndarray, List]]:
    """Given an array and bin size, bins the array along an arbitrary axis into
    bins of size `bin_size`. It will perform padding if the array does not split
    up into equal bin sizes. 

    Args:
        array (np.ndarray): The input array.
        bin_size (int): The size of each bin.
        axis (int): The axis to bin the array along. Default is -1.
        pad_dir (str): The padding direction. One of `left`, `right`, or
            `symmetric` (default).
        return_padding (bool): Option to return the padding width used. 
        mode (str): The padding mode. See the NumPy documentation for options. 

    Returns:
        np.ndarray: The binned array where the number of bins is first. That is,
            the shape will be `(..., n_bins, bin_size, ...)`.

    """
    if axis == -1:
        axis = array.ndim - 1

    curr_len = array.shape[axis]
    n_bins = math.ceil(curr_len / bin_size)
    new_len = n_bins * bin_size

    new_shape = list(array.shape)
    new_shape[axis] = n_bins
    new_shape.insert(axis + 1, bin_size)

    # Perform padding if curr_len does not equal new_len.
    padding = [(0, 0)] * array.ndim
    if curr_len != new_len:
        if pad_dir == "left":
            pad_l = new_len - curr_len
            pad_r = 0
        elif pad_dir == "right":
            pad_l = 0
            pad_r = new_len - curr_len
        else:
            pad_l = (new_len - curr_len) // 2
            pad_r = (new_len - curr_len) - pad_l

        padding[axis] = (pad_l, pad_r)
        array = np.pad(array, padding, mode = mode, **padding_kwargs)

    array = array.reshape(new_shape)

    if return_padding:
        return array, padding

    return array

# %%
def compute_eeg(eeg: np.ndarray) -> np.ndarray:
    eeg = butter_filter(eeg, cutoff_freq = np.array([0.25, 50]), btype = "bandpass")
    eeg = bin_array(eeg, bin_size = 4, mode = "reflect").mean(axis = -1)
    return eeg
    
def compute_eeg_chain(df_eeg: pl.DataFrame) -> np.ndarray:
    Fp1 = df_eeg["Fp1"].to_numpy()
    Fp2 = df_eeg["Fp2"].to_numpy()
    F3  = df_eeg["F3"].to_numpy()
    F4  = df_eeg["F4"].to_numpy()
    F7  = df_eeg["F7"].to_numpy()
    F8  = df_eeg["F8"].to_numpy()
    C3  = df_eeg["C3"].to_numpy()
    C4  = df_eeg["C4"].to_numpy()
    P3  = df_eeg["P3"].to_numpy()
    P4  = df_eeg["P4"].to_numpy()
    T3  = df_eeg["T3"].to_numpy()
    T4  = df_eeg["T4"].to_numpy()
    T5  = df_eeg["T5"].to_numpy()
    T6  = df_eeg["T6"].to_numpy()
    O1  = df_eeg["O1"].to_numpy()
    O2  = df_eeg["O2"].to_numpy()
    
    ll = np.stack([(compute_eeg(Fp1 - F7), compute_eeg(F7 - T3), compute_eeg(T3 - T5), compute_eeg(T5 - O1))])
    lp = np.stack([(compute_eeg(Fp1 - F3), compute_eeg(F3 - C3), compute_eeg(C3 - P3), compute_eeg(P3 - O1))])
    rp = np.stack([(compute_eeg(Fp2 - F4), compute_eeg(F4 - C4), compute_eeg(C4 - P4), compute_eeg(P4 - O2))])
    rl = np.stack([(compute_eeg(Fp2 - F8), compute_eeg(F8 - T4), compute_eeg(T4 - T6), compute_eeg(T6 - O2))])
    
    chain = np.stack([ll, lp, rp, rl])[:, 0]
    
    return chain

def compute_eeg_from_file(filepath: str) -> np.ndarray:
    df_eeg = pl.read_parquet(filepath).fill_null(0).fill_nan(0)
    # Repair infinities before filtering: one nonfinite value can poison a lead.
    df_eeg = df_eeg.with_columns([
        pl.when(pl.col(name).is_infinite()).then(0).otherwise(pl.col(name)).alias(name)
        for name in EEG_COLUMNS
    ])
    chain = compute_eeg_chain(df_eeg)
    
    return chain

# %%
def proc_0(x):
    x = x.copy()
    
    x = x - x.mean(axis = -1, keepdims = True)
    x = x / (np.mean(x.std(axis = -1)) + 1e-5)
    x = x.reshape(4, 4, 2_500)
    
    return x

def proc_1(x):
    x = x.copy()
    
    x = x - x.mean(axis = -1, keepdims = True)
    x = x / (x.std(axis = -1, keepdims = True) + 1e-5)
    x = x.reshape(16, 1, 2_500)
    
    return x


# %%
@torch.no_grad()
def gen_ensemble_pred(df_row: pl.DataFrame) -> np.ndarray:
    eeg_id = df_row["eeg_id"].item()
    filepath = os.path.join(EEG_DIR, f"{eeg_id}.parquet")
    x = compute_eeg_from_file(filepath)
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    if x.shape != (4, 4, 2500):
        raise ValueError(f"Unexpected EEG shape for {eeg_id}: {x.shape}")

    x0 = torch.as_tensor(proc_0(x), dtype=torch.float32, device=device).unsqueeze(0)
    x1 = torch.as_tensor(proc_1(x), dtype=torch.float32, device=device).unsqueeze(0)

    # Identity inference: the flip TTA in v14 worsened the recorded score.
    preds = []
    for models, inputs in ((models_0, x0), (models_1, x1)):
        for model in models:
            log_probs = model(inputs).float().reshape(-1)
            if log_probs.numel() != len(LABELS) or not torch.isfinite(log_probs).all():
                raise ValueError(f"Invalid model output for EEG {eeg_id}")
            # Equivalent to exp(log_probs) for normalized log-probabilities,
            # while keeping the computation stable for very small outputs.
            preds.append(torch.softmax(log_probs, dim=-1).cpu().numpy())

    pred = np.mean(np.stack(preds), axis=0, dtype=np.float64)
    pred = np.clip(pred, 1e-12, 1.0)
    return pred / pred.sum()

# %%
preds_final = []
for i in tqdm(range(len(df_test)), desc="Predicting EEGs"):
    preds_final.append(gen_ensemble_pred(df_test[i]))

# %%
df_sub = pd.DataFrame({"eeg_id": df_test["eeg_id"].to_list()})
df_sub[LABELS] = np.asarray(preds_final).reshape(-1, len(LABELS))
# Use the sample file's ID order and exact column order.
submission_order = pd.DataFrame({"eeg_id": sample_submission["eeg_id"].to_list()})
df_sub = submission_order.merge(df_sub, on="eeg_id", how="left", validate="one_to_one")
df_sub = df_sub[sample_submission.columns]
probabilities = df_sub[LABELS].to_numpy()
assert np.isfinite(probabilities).all(), "Submission contains nonfinite probabilities"
assert (probabilities >= 0).all(), "Submission contains negative probabilities"
assert np.allclose(probabilities.sum(axis=1), 1.0, atol=1e-6)
df_sub.to_csv("submission.csv", index=False)
df_sub

# %%
from tqdm.auto import tqdm
import pandas as pd
import polars as pl
import numpy as np
import argparse
import os

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from typing import Optional
from typing import Tuple
from typing import List
from typing import Dict
from typing import Any

# %%
DATA_DIR = "/kaggle/input/hms-harmful-brain-activity-classification/"
SPEC_DIR = os.path.join(DATA_DIR, "test_spectrograms/")
EEG_DIR = os.path.join(DATA_DIR, "test_eegs/")

df_train = pl.read_csv(os.path.join(DATA_DIR, "train.csv"))
df_test = pl.read_csv(os.path.join(DATA_DIR, "test.csv"))
sample_submission = pl.read_csv(os.path.join(DATA_DIR, "sample_submission.csv"))

df_test.head()

# %%
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)
print()

# %%
def load_model(path: str, model: nn.Module) -> nn.Module:
    model.load_state_dict(torch.load(path, map_location = torch.device("cpu"))["model_state_dict"])
    return model

# %%
import sys
sys.path.append("/kaggle/input/hms-models/")

from eeg_cnn_rnn_w1 import EegModel as EegModel0
from eeg_cnn_rnn import EegModel as EegModel1

# %%
import glob

# Restore the two EEG families used by the strongest recorded version (v13).
# Keep each checkpoint's input layout and normalization unchanged.
model_0_files = sorted(set(
    glob.glob("/kaggle/input/hms-models/new_distil/send_kaggle/*") +
    glob.glob("/kaggle/input/hms-models/new_fold/send_kaggle/*")
))
model_0_files = [path for path in model_0_files if os.path.isfile(path)]
model_1_files = sorted(
    os.path.join(path, "model_best_val_g10.pt")
    for path in glob.glob("/kaggle/input/hms-models/baseline_eeg_diff/*")
    if os.path.isdir(path)
)
if not model_0_files or not model_1_files:
    raise FileNotFoundError("Both pretrained EEG model families are required.")

models_0 = []
for model_path in model_0_files:
    model = load_model(model_path, EegModel0()).to(device).eval()
    models_0.append(model)

models_1 = []
for model_path in model_1_files:
    model = load_model(model_path, EegModel1()).to(device).eval()
    models_1.append(model)

print(f"Loaded {len(models_0)} w1 EEG models and {len(models_1)} baseline EEG models")

# %%
from scipy.signal import butter, filtfilt


def butter_filter(eeg_data, fs=200, cutoff_freq=22, order=4, btype="lowpass"):
    b, a = butter(
        N=order,
        Wn=cutoff_freq / (0.5 * fs),
        btype=btype,
        analog=False,
    )
    return filtfilt(b, a, eeg_data)

# %%
import numpy as np
import math

from typing import Union
from typing import Tuple
from typing import List


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
    df_eeg = pl.read_parquet(filepath).fill_null(0)
    # Clean each electrode before differencing/filtering: filtfilt propagates
    # a single NaN through an entire lead. Match the existing zero-null policy.
    df_eeg = pl.DataFrame({
        name: np.nan_to_num(df_eeg[name].to_numpy(), nan=0.0, posinf=0.0, neginf=0.0)
        for name in df_eeg.columns
    })
    chain = compute_eeg_chain(df_eeg)
    return np.nan_to_num(chain, nan=0.0, posinf=0.0, neginf=0.0)

# %%
LABELS = [
    "seizure_vote", 
    "lpd_vote", 
    "gpd_vote", 
    "lrda_vote", 
    "grda_vote", 
    "other_vote"
]

# %%
# Option for better printing.
np.set_printoptions(formatter = {"all": lambda x: f"{x:0.3f}"})

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


@torch.inference_mode()
def gen_ensemble_pred(df_row: pl.DataFrame) -> np.ndarray:
    eeg_id = df_row["eeg_id"].item()
    filepath = os.path.join(EEG_DIR, f"{eeg_id}.parquet")
    x = compute_eeg_from_file(filepath)

    # Identity-only inference: channel-flip TTA degraded v14 relative to v13.
    # In particular, w1 requires (batch, 4, 4, 2500), whereas the baseline
    # requires (batch, 16, 1, 2500). Do not reshape either family's input for TTA.
    x0 = torch.as_tensor(proc_0(x), dtype=torch.float32, device=device).unsqueeze(0)
    x1 = torch.as_tensor(proc_1(x), dtype=torch.float32, device=device).unsqueeze(0)
    preds = []
    for models, inputs in ((models_0, x0), (models_1, x1)):
        for model in models:
            # These checkpoints return log probabilities. Softmax is equivalent
            # to exp followed by normalization and is numerically stable.
            pred = torch.softmax(model(inputs).float(), dim=-1)
            pred = pred.cpu().numpy().reshape(-1)
            if pred.shape != (len(LABELS),) or not np.isfinite(pred).all():
                raise ValueError(f"Invalid model prediction for EEG {eeg_id}")
            preds.append(pred)

    # Equal checkpoint weights reproduce the successful v13 ensemble rule.
    # Average probabilities, not log probabilities, for the forward KL metric.
    pred = np.mean(np.stack(preds).astype(np.float64), axis=0)
    pred = np.maximum(pred, 1e-15)
    return pred / pred.sum()

# %%
from tqdm.auto import tqdm
    
preds_final = []
for i in tqdm(range(len(df_test)), desc="EEG ensemble inference"):
    pred = gen_ensemble_pred(df_test[i])
    preds_final.append(pred)

# %%
df_sub = pd.DataFrame({"eeg_id": df_test["eeg_id"].to_list()})
df_sub[LABELS] = preds_final
if not np.isfinite(df_sub[LABELS].to_numpy()).all():
    raise ValueError("Submission contains non-finite probabilities")
if not np.allclose(df_sub[LABELS].sum(axis=1), 1.0, atol=1e-7):
    raise ValueError("Submission probabilities must sum to one")
if df_sub["eeg_id"].duplicated().any():
    raise ValueError("Submission must contain one row per EEG")
df_sub.to_csv("submission.csv", index = False)
df_sub

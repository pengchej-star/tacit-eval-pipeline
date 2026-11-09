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
from spc_cnn_rnn import SpectrogramModel

# %%
import glob
import sys

model_0_files = (
    glob.glob("/kaggle/input/hms-models/new_distil/send_kaggle/*") + 
    glob.glob("/kaggle/input/hms-models/new_fold/send_kaggle/*")
)
model_2_files = (
    glob.glob("/kaggle/input/hms-models/send_kaggle_spec/send_kaggle_spec/*") 
)

models_0 = [] 
for fold_path in model_0_files:
    model = EegModel0()
    model = load_model(fold_path, model)
    model = model.to(device)
    model.eval()
    models_0.append(model)

models_1 = [] 
for fold_path in glob.glob("/kaggle/input/hms-models/baseline_eeg_diff/*"):
    model_path = os.path.join(fold_path, "model_best_val_g10.pt")
    model = EegModel1()
    model = load_model(model_path, model)
    model = model.to(device)
    model.eval()
    models_1.append(model)

models_2 = []
for fold_path in model_2_files:
    model = SpectrogramModel()
    model = load_model(fold_path, model)
    model = model.to(device)
    models_2.append(model)

print(len(models_0), len(models_1), len(models_2))

# %%
def MAD(signal, **kwargs):
    """Compute the robust standard deviation (MAD) of a signal."""
    scale_factor = 1.4826  # This is a constant for normal distribution
    absolute_deviations = np.abs(signal - np.median(signal, **kwargs))
    median_absolute_deviation = np.median(absolute_deviations, **kwargs)
    robust_std = median_absolute_deviation * scale_factor
    return robust_std

from scipy.signal import welch
from scipy.stats import linregress
from scipy.signal import butter, filtfilt

def butter_filter(eeg_data, fs = 200, cutoff_freq = 22, order = 4, btype = "lowpass"):
    b, a = butter(
        N = order, 
        Wn = cutoff_freq / (0.5 * fs), 
        btype = btype, 
        analog = False
    )

    return filtfilt(b, a, eeg_data)

# %%
STRIDE = 100
WINDOW_SIZE = 500
NOVERLAP = WINDOW_SIZE - STRIDE 
PARAMS = dict(
    fs = 200, 
    window = ("tukey", 0.25), 
    nperseg = WINDOW_SIZE, 
    noverlap = NOVERLAP, 
    nfft = 1024, 
    detrend = "constant", 
    return_onesided = True, 
    scaling = "density", 
    axis = -1, 
    mode = "psd"
)

# %%
import scipy

def compute_spec(eeg: np.ndarray) -> np.ndarray:
    freqs, _, Sxx = scipy.signal.spectrogram(eeg, **PARAMS)
    valid_freq = (freqs >= 0.5) & (freqs <= 20)
    return Sxx[valid_freq, :]

def compute_spec_eeg(a, b) -> np.ndarray:
    eeg = a - b
    eeg = butter_filter(eeg, cutoff_freq = np.array([0.25, 40.0]), order = 5, btype = "bandpass")
    return eeg

def compute_spec_chain(df_eeg: pl.DataFrame) -> np.ndarray:
    Fp1 = df_eeg["Fp1"].to_numpy() 
    Fp2 = df_eeg["Fp2"].to_numpy()
    Fz  = df_eeg["Fz"].to_numpy()
    Cz  = df_eeg["Cz"].to_numpy()
    Pz  = df_eeg["Pz"].to_numpy()
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
    
    ll = np.stack([(compute_spec_eeg(Fp1 , F7), compute_spec_eeg(F7 , T3), compute_spec_eeg(T3 , T5), compute_spec_eeg(T5 , O1))])
    lp = np.stack([(compute_spec_eeg(Fp1 , F3), compute_spec_eeg(F3 , C3), compute_spec_eeg(C3 , P3), compute_spec_eeg(P3 , O1))])
    rp = np.stack([(compute_spec_eeg(Fp2 , F4), compute_spec_eeg(F4 , C4), compute_spec_eeg(C4 , P4), compute_spec_eeg(P4 , O2))])
    rl = np.stack([(compute_spec_eeg(Fp2 , F8), compute_spec_eeg(F8 , T4), compute_spec_eeg(T4 , T6), compute_spec_eeg(T6 , O2))])
    chain = np.stack([ll, lp, rp, rl])[:, 0]
    
    mads = MAD(chain, axis = -1, keepdims = True)
    mads = np.median(mads.reshape(-1))
    chain = chain / (mads + 1e-5)
    
    outer = []
    for i in range(4):
        inner = []
        for j in range(4):
            inner.append(compute_spec(chain[i, j]))
        outer.append(inner)
        
    chain = np.array(outer)
    chain = np.log(chain.clip(np.exp(-4), np.exp(8)))
    chain = chain.mean(axis = 1, keepdims = True)
    
    return chain

# %%
def compute_spec_from_file(filepath: str) -> np.ndarray:
    df_eeg = pl.read_parquet(filepath).fill_null(0)
    chain = compute_spec_chain(df_eeg)
    return chain

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
    chain = compute_eeg_chain(df_eeg)
    
    return chain

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


def proc_2(spec):
    spec = spec - spec.mean(axis = (-1, -2), keepdims = True)
    spec = spec / (spec.std(axis = (-1, -2), keepdims = True) + 1e-5)
    return spec


def flip_h(eeg):
    temp0 = eeg[0].copy()
    temp1 = eeg[1].copy()

    eeg[0] = eeg[3]
    eeg[1] = eeg[2]
    eeg[3] = temp0
    eeg[2] = temp1
    
    return eeg

def flip_v(eeg):
    temp0 = eeg[:, 0].copy()
    temp1 = eeg[:, 1].copy()

    eeg[:, 0] = eeg[:, 3]
    eeg[:, 1] = eeg[:, 2]
    eeg[:, 3] = temp0
    eeg[:, 2] = temp1
    
    return eeg

def tta(x):
    x0 = x.copy().reshape(4, 4, -1)
    x1 = x.copy().reshape(4, 4, -1)
    x2 = x.copy().reshape(4, 4, -1)

    x0 = flip_v(x0).reshape(16, 1, -1)
    x1 = flip_h(x1).reshape(16, 1, -1)
    x2 = flip_v(flip_h(x2)).reshape(16, 1, -1)
    
    return x, x0, x1, x2

# Family-level blend weights. EEG families (v13 configuration) reached 0.302 on the
# leaderboard; the spectrogram family alone reached 0.439, so it enters with a
# small weight as a diversity member rather than as an equal partner.
W_EEG_0 = 0.40
W_EEG_1 = 0.40
W_SPEC  = 0.20

def _family_mean(models, x) -> Optional[np.ndarray]:
    if len(models) == 0:
        return None
    outs = []
    for model in models:
        model.eval()
        outs.append(model(x).exp().cpu().detach().numpy().reshape(-1))
    p = np.mean(outs, axis = 0)
    return p / (p.sum() + 1e-12)

@torch.no_grad()
def gen_ensemble_pred(df_row: pl.DataFrame) -> np.ndarray:
    eeg_id = df_row["eeg_id"].item()
    filepath = os.path.join(EEG_DIR, f"{eeg_id}.parquet")
    
    # Raw-EEG branch (v13 configuration, no flip TTA which hurt in v14).
    x = compute_eeg_from_file(filepath)
    x[np.isnan(x) | np.isinf(x)] = 0

    x0 = proc_0(x)
    x1 = proc_1(x)
    x0 = torch.Tensor(x0).to(device).unsqueeze(0)
    x1 = torch.Tensor(x1).to(device).unsqueeze(0)
    
    # Spectrogram branch.
    spec = compute_spec_from_file(filepath)
    spec[np.isnan(spec) | np.isinf(spec)] = 0
    spec = proc_2(spec)
    spec = torch.Tensor(spec).to(device).unsqueeze(0)
    
    families = [
        (W_EEG_0, _family_mean(models_0, x0)),
        (W_EEG_1, _family_mean(models_1, x1)),
        (W_SPEC,  _family_mean(models_2, spec)),
    ]
    families = [(w, p) for (w, p) in families if p is not None]
    
    total_w = sum(w for w, _ in families)
    preds = sum(w * p for w, p in families) / total_w
    preds = np.clip(preds, 1e-6, 1.0)
    preds = preds / preds.sum()
    return preds

# %%
from tqdm.auto import tqdm
    
preds_final = []
for i in range(len(df_test)):
    pred = gen_ensemble_pred(df_test[i])
    preds_final.append(pred)

# %%
df_sub = pd.DataFrame({"eeg_id": df_test["eeg_id"].to_list()})
df_sub[LABELS] = preds_final
df_sub.to_csv("submission.csv", index = False)
df_sub

# %% [markdown]
# # About
# 
# I tried the suggested concept in this topic:  
# https://www.kaggle.com/c/ranzcr-clip-catheter-line-classification/discussion/205208
# 
# I'll share all the experimental results in this topic:  
# https://www.kaggle.com/c/ranzcr-clip-catheter-line-classification/discussion/207230
# 
# This is an **inference notebook**.  
# * model:
#     * base: ResNeXt50_32x4d
#     * multi-head: **not use multi-head architecture**
# * image size: 3x448x448
# * CVStrategy: Multi-Label Stratified Group KFold(K=**5**)
# * using mixed precision training
# 
# 
# If you want to know more details of experimental settings, see training notebook:  
# https://www.kaggle.com/ttahara/ranzcr-multi-head-model-training?scriptVersionId=51935970

# %% [markdown]
# # Prepare

# %% [markdown]
# ## import

# %%
import gc
import os
import sys
import time
import copy
import random
import shutil
import typing as tp
from pathlib import Path
from argparse import ArgumentParser

import yaml
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from sklearn.metrics import roc_auc_score

from tqdm import tqdm
from joblib import Parallel, delayed

import cv2
import albumentations

from albumentations.core.transforms_interface import ImageOnlyTransform, DualTransform
from albumentations.pytorch import ToTensorV2

import torch
from torch import nn
from torch.utils import data
from torchvision import models as torchvision_models

sys.path.append('../input/pytorch-image-models/pytorch-image-models-master')
import timm

# %%
ROOT = Path.cwd().parent
INPUT = ROOT / "input"
OUTPUT = ROOT / "output"
DATA = INPUT / "ranzcr-clip-catheter-line-classification"
TRAIN = DATA / "train"
TEST = DATA / "test"


TRAINED_MODEL = INPUT / "ranzcr-clip-weights-for-multi-head-model-v1"
TMP = ROOT / "tmp"
TMP.mkdir(exist_ok=True)

RANDAM_SEED = 1086
N_CLASSES = 11
FOLDS = [0, 1, 2, 3, 4]
N_FOLD = len(FOLDS)
IMAGE_SIZE = (448, 448)

CONVERT_TO_RANK = False
FAST_COMMIT = False
# # test-time augmentation: average original and horizontally flipped views
USE_HFLIP_TTA = True

CLASSES = [
    'ETT - Abnormal',
    'ETT - Borderline',
    'ETT - Normal',
    'NGT - Abnormal',
    'NGT - Borderline',
    'NGT - Incompletely Imaged',
    'NGT - Normal',
    'CVC - Abnormal',
    'CVC - Borderline',
    'CVC - Normal',
    'Swan Ganz Catheter Present'
]

# %% [markdown]
# ## read data

# %%
for p in DATA.iterdir():
    print(p.name)

train = pd.read_csv(DATA / "train.csv")
smpl_sub =  pd.read_csv(DATA / "sample_submission.csv")

# %%
smpl_sub.shape

# %%
if FAST_COMMIT and len(smpl_sub) == 3582:
    smpl_sub = smpl_sub.iloc[:64 * 3].reset_index(drop=True)

# %% [markdown]
# ## split fold

# %%
def multi_label_stratified_group_k_fold(label_arr: np.array, gid_arr: np.array, n_fold: int, seed: int=42):
    """
    create multi-label stratified group kfold indexs.

    reference: https://www.kaggle.com/jakubwasikowski/stratified-group-k-fold-cross-validation
    input:
        label_arr: numpy.ndarray, shape = (n_train, n_class)
            multi-label for each sample's index using multi-hot vectors
        gid_arr: numpy.array, shape = (n_train,)
            group id for each sample's index
        n_fold: int. number of fold.
        seed: random seed.
    output:
        yield indexs array list for each fold's train and validation.
    """
    np.random.seed(seed)
    random.seed(seed)
    start_time = time.time()
    n_train, n_class = label_arr.shape
    gid_unique = sorted(set(gid_arr))
    n_group = len(gid_unique)

    # # aid_arr: (n_train,), indicates alternative id for group id.
    # # generally, group ids are not 0-index and continuous or not integer.
    gid2aid = dict(zip(gid_unique, range(n_group)))
#     aid2gid = dict(zip(range(n_group), gid_unique))
    aid_arr = np.vectorize(lambda x: gid2aid[x])(gid_arr)

    # # count labels by class
    cnts_by_class = label_arr.sum(axis=0)  # (n_class, )

    # # count labels by group id.
    col, row = np.array(sorted(enumerate(aid_arr), key=lambda x: x[1])).T
    cnts_by_group = coo_matrix(
        (np.ones(len(label_arr)), (row, col))
    ).dot(coo_matrix(label_arr)).toarray().astype(int)
    del col
    del row
    cnts_by_fold = np.zeros((n_fold, n_class), int)

    groups_by_fold = [[] for fid in range(n_fold)]
    group_and_cnts = list(enumerate(cnts_by_group))  # pair of aid and cnt by group
    np.random.shuffle(group_and_cnts)
    print("finished preparation", time.time() - start_time)
    for aid, cnt_by_g in sorted(group_and_cnts, key=lambda x: -np.std(x[1])):
        best_fold = None
        min_eval = None
        for fid in range(n_fold):
            # # eval assignment.
            cnts_by_fold[fid] += cnt_by_g
            fold_eval = (cnts_by_fold / cnts_by_class).std(axis=0).mean()
            cnts_by_fold[fid] -= cnt_by_g

            if min_eval is None or fold_eval < min_eval:
                min_eval = fold_eval
                best_fold = fid

        cnts_by_fold[best_fold] += cnt_by_g
        groups_by_fold[best_fold].append(aid)
    print("finished assignment.", time.time() - start_time)

    gc.collect()
    idx_arr = np.arange(n_train)
    for fid in range(n_fold):
        val_groups = groups_by_fold[fid]

        val_indexs_bool = np.isin(aid_arr, val_groups)
        train_indexs = idx_arr[~val_indexs_bool]
        val_indexs = idx_arr[val_indexs_bool]

        print("[fold {}]".format(fid), end=" ")
        print("n_group: (train, val) = ({}, {})".format(n_group - len(val_groups), len(val_groups)), end=" ")
        print("n_sample: (train, val) = ({}, {})".format(len(train_indexs), len(val_indexs)))

        yield train_indexs, val_indexs

# %%
label_arr = train[CLASSES].values
group_id = train.PatientID.values

train_val_indexs = list(
    multi_label_stratified_group_k_fold(label_arr, group_id, N_FOLD, RANDAM_SEED))

# %%
train["fold"] = -1
for fold_id, (trn_idx, val_idx) in enumerate(train_val_indexs):
    train.loc[val_idx, "fold"] = fold_id
    
train.groupby("fold")[CLASSES].sum()

# %% [markdown]
# ## preprocess test images

# %%
def resize_images(img_id, input_dir, output_dir, resize_to=(512, 512), ext="png"):
    img_path = input_dir / f"{img_id}.jpg"
    save_path = output_dir / f"{img_id}.{ext}"
    
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, resize_to)
    cv2.imwrite(str(save_path), img, )

TEST_RESIZED = TMP / "test_{0}x{1}".format(*IMAGE_SIZE)
TEST_RESIZED.mkdir(exist_ok=True)
TEST_RESIZED

_ = Parallel(n_jobs=2, verbose=5)([
    delayed(resize_images)(img_id, TEST, TEST_RESIZED, IMAGE_SIZE, "png")
    for img_id in smpl_sub.StudyInstanceUID.values
])

# %% [markdown]
# # Inference

# %% [markdown]
# ## definition

# %% [markdown]
# ### custom model

# %%
class SSEBlock(nn.Module):
    """channel `S`queeze and `s`patial `E`xcitation Block."""

    def __init__(self, in_channels: int):
        """Initialize."""
        super(SSEBlock, self).__init__()
        self.channel_squeeze = nn.Conv2d(
            in_channels=in_channels, out_channels=1,
            kernel_size=1, stride=1, padding=0, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        """Forward."""
        # # x: (bs, ch, h, w) => h: (bs, 1, h, w)
        h = self.sigmoid(self.channel_squeeze(x))
        # # x, h => return: (bs, ch, h, w)
        h = x * h
        return h 


class MultiHeadResNeXt(nn.Module):
    
    def __init__(
        self, base_name: str='resnext50_32x4d',
        out_dims_head: tp.List[int]=[3, 4, 3, 1], pretrained=False):
        """"""
        self.base_name = base_name
        self.n_heads = len(out_dims_head)
        super(MultiHeadResNeXt, self).__init__()
        
        # # load base model
        base_model = timm.create_model(base_name, pretrained=pretrained)
        in_features = base_model.num_features
        
        # # remove global pooling and head classifier
        base_model.reset_classifier(0, '')
        
        # # Shared CNN Bacbone
        self.backbone = base_model
        
        # # Multi Heads.
        for i, out_dim in enumerate(out_dims_head):
            layer_name = f"head_{i}"
            layer = nn.Sequential(
                SSEBlock(in_features),
                nn.AdaptiveAvgPool2d(output_size=1),
                nn.Flatten(start_dim=1),
                nn.Linear(in_features, in_features),
                nn.ReLU(inplace=True),
                nn.Dropout(0.5),
                nn.Linear(in_features, out_dim))
            setattr(self, layer_name, layer)

    def forward(self, x):
        """"""
        h = self.backbone(x)
        hs = [
            getattr(self, f"head_{i}")(h) for i in range(self.n_heads)]
        y = torch.cat(hs, axis=1)
        return y
    
    
class SingleHeadModel(nn.Module):
    
    def __init__(
        self, base_name: str='resnext50_32x4d', out_dim: int=11, pretrained=False
    ):
        """"""
        self.base_name = base_name
        super(SingleHeadModel, self).__init__()
        
        # # load base model
        base_model = timm.create_model(base_name, pretrained=pretrained)
        in_features = base_model.num_features
        
        # # remove global pooling and head classifier
        # base_model.reset_classifier(0, '')
        base_model.reset_classifier(0)
        
        # # Shared CNN Bacbone
        self.backbone = base_model
        
        # # Single Heads.
        self.head_fc = nn.Sequential(
            nn.Linear(in_features, in_features),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(in_features, out_dim))

    def forward(self, x):
        """"""
        h = self.backbone(x)
        h = self.head_fc(h)
        return h

# %% [markdown]
# ### dataset

# %%
class LabeledImageDataset(data.Dataset):
    """
    Dataset class for (image, label) pairs

    reads images and applys transforms to them.

    Attributes
    ----------
    file_list : List[Tuple[tp.Union[str, Path], tp.Union[int, float, np.ndarray]]]
        list of (image file, label) pair
    transform_list : List[Dict]
        list of dict representing image transform 
    """

    def __init__(
        self,
        file_list: tp.List[
            tp.Tuple[tp.Union[str, Path], tp.Union[int, float, np.ndarray]]],
        transform_list: tp.List[tp.Dict],
    ):
        """Initialize"""
        self.file_list = file_list
        self.transform = ImageTransformForCls(transform_list)

    def __len__(self):
        """Return Num of Images."""
        return len(self.file_list)

    def __getitem__(self, index):
        """Return transformed image and mask for given index."""
        img_path, label = self.file_list[index]
        img = self._read_image_as_array(img_path)
        
        img, label = self.transform((img, label))
        return img, label

    def _read_image_as_array(self, path: str):
        """Read image file and convert into numpy.ndarray"""
        img_arr = cv2.imread(str(path))
        img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
        return img_arr

# %%
def get_dataloaders_for_inference(
    file_list: tp.List[tp.List], batch_size=64,
):
    """Create DataLoader"""
    dataset = LabeledImageDataset(
        file_list,
        transform_list=[
          ["Normalize", {
              "always_apply": True, "max_pixel_value": 255.0,
              "mean": ["0.4887381077884414"], "std": ["0.23064819430546407"]}],
          ["ToTensorV2", {"always_apply": True}],
        ])
    loader = data.DataLoader(
        dataset,
        batch_size=batch_size, shuffle=False,
        num_workers=2, pin_memory=True,
        drop_last=False)

    return loader

# %% [markdown]
# ### image transform

# %%
class ImageTransformBase:
    """
    Base Image Transform class.

    Args:
        data_augmentations: List of tuple(method: str, params :dict), each elems pass to albumentations
    """

    def __init__(self, data_augmentations: tp.List[tp.Tuple[str, tp.Dict]]):
        """Initialize."""
        augmentations_list = [
            self._get_augmentation(aug_name)(**params)
            for aug_name, params in data_augmentations]
        self.data_aug = albumentations.Compose(augmentations_list)

    def __call__(self, pair: tp.Tuple[np.ndarray]) -> tp.Tuple[np.ndarray]:
        """You have to implement this by task"""
        raise NotImplementedError

    def _get_augmentation(self, aug_name: str) -> tp.Tuple[ImageOnlyTransform, DualTransform]:
        """Get augmentations from albumentations"""
        if hasattr(albumentations, aug_name):
            return getattr(albumentations, aug_name)
        else:
            return eval(aug_name)


class ImageTransformForCls(ImageTransformBase):
    """Data Augmentor for Classification Task."""

    def __init__(self, data_augmentations: tp.List[tp.Tuple[str, tp.Dict]]):
        """Initialize."""
        super(ImageTransformForCls, self).__init__(data_augmentations)

    def __call__(self, in_arrs: tp.Tuple[np.ndarray]) -> tp.Tuple[np.ndarray]:
        """Apply Transform."""
        img, label = in_arrs
        augmented = self.data_aug(image=img)
        img = augmented["image"]

        return img, label

# %% [markdown]
# ### utils

# %%
def load_setting_file(path: str):
    """Load YAML setting file."""
    with open(path) as f:
        settings = yaml.safe_load(f)
    return settings


def set_random_seed(seed: int = 42, deterministic: bool = False):
    """Set seeds"""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)  # type: ignore
    torch.backends.cudnn.deterministic = deterministic  # type: ignore
    

def run_inference_loop(stgs, model, loader, device, use_hflip_tta=False):
    model.to(device)
    model.eval()
    pred_list = []
    with torch.no_grad():
        for x, t in tqdm(loader):
            x = x.to(device)
            y = model(x).sigmoid()
            if use_hflip_tta:
                # # x: (bs, ch, h, w) -> flip along width axis
                y_flip = model(torch.flip(x, dims=[3])).sigmoid()
                y = 0.5 * (y + y_flip)
            pred_list.append(y.detach().cpu().numpy())
        
    pred_arr = np.concatenate(pred_list)
    del pred_list
    return pred_arr

# %% [markdown]
# ## inference test data

# %%
if not torch.cuda.is_available():
    device = torch.device("cpu")
else:
    device = torch.device("cuda")
print(device)

# %%
model_dir = TRAINED_MODEL
test_dir = TEST_RESIZED

test_file_list = [
    (test_dir / f"{img_id}.png", [-1] * 11)
    for img_id in smpl_sub["StudyInstanceUID"].values]
test_loader = get_dataloaders_for_inference(test_file_list, batch_size=64)
        
test_preds_arr = np.zeros((N_FOLD, len(smpl_sub), N_CLASSES))    
for fold_id in FOLDS:
    print(f"[fold {fold_id}]")
    stgs = load_setting_file(model_dir / f"fold{fold_id}" / "settings.yml")
    # # prepare 
    stgs["model"]["params"]["pretrained"] = False
    model_path = model_dir / f"best_model_fold{fold_id}.pth"
    state_dict = torch.load(model_path, map_location=device)
    # # choose the architecture matching the checkpoint keys
    # # (multi-head checkpoints have `head_0.*` keys, single-head have `head_fc.*`)
    params = dict(stgs["model"]["params"])
    if any(k.startswith("head_fc") for k in state_dict.keys()):
        params = {k: v for k, v in params.items() if k in ("base_name", "out_dim", "pretrained")}
        model = SingleHeadModel(**params)
    else:
        params = {k: v for k, v in params.items() if k in ("base_name", "out_dims_head", "pretrained")}
        model = MultiHeadResNeXt(**params)
    model.load_state_dict(state_dict)
    del state_dict

    # # inference test
    test_pred = run_inference_loop(
        stgs, model, test_loader, device, use_hflip_tta=USE_HFLIP_TTA)
    test_preds_arr[fold_id] = test_pred
    
    del model
    torch.cuda.empty_cache()
    gc.collect()

# %% [markdown]
# ## make submission

# %%
if CONVERT_TO_RANK:
    # # shape: (fold, n_example, class)
    test_preds_arr = test_preds_arr.argsort(axis=1).argsort(axis=1)

sub = smpl_sub.copy()
sub[CLASSES] = test_preds_arr.mean(axis=0)
    
sub.to_csv("submission.csv", index=False)

# %%
sub.head()

# %%


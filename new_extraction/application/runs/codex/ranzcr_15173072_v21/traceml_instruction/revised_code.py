# %%
import sys
sys.path.append('../input/timm-pytorch-image-models/pytorch-image-models-master')
import timm

# %%
import os
from collections import OrderedDict

import cv2
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from albumentations import Compose, Normalize, Resize
from albumentations.pytorch import ToTensorV2
from tqdm.auto import tqdm

path = '../input/ranzcr-clip-catheter-line-classification/'
TEST_PATH = os.path.join(path, 'test')
# Restore the best documented preprocessing, with a smaller secondary scale.
IMAGE_SIZE = 512
SCALE_WEIGHTS = ((IMAGE_SIZE, 0.8), (640, 0.2))
BATCH_SIZE = 16
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

# %%
# Load on CPU first to avoid transient duplicate GPU allocations.
map_location = 'cpu'

# %%
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
cv2.setNumThreads(0)
if device.type == 'cuda':
    torch.backends.cudnn.benchmark = True

# %%
class TestDataset(Dataset):
    def __init__(self, df, transform=None):
        self.file_names = df['StudyInstanceUID'].values
        self.transform = transform

    def __len__(self):
        return len(self.file_names)

    def __getitem__(self, idx):
        file_path = os.path.join(TEST_PATH, f'{self.file_names[idx]}.jpg')
        image = cv2.imread(file_path)
        if image is None:
            raise FileNotFoundError(f'Could not read image: {file_path}')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if self.transform is not None:
            image = self.transform(image=image)['image']
        return image

# %%
def get_transforms(image_size=IMAGE_SIZE):
    # Full-frame resize preserves tube tips and incompletely imaged devices.
    return Compose([
        Resize(image_size, image_size, interpolation=cv2.INTER_LINEAR),
        Normalize(mean=MEAN, std=STD),
        ToTensorV2(),
    ])

# %%
class ResNet200D(nn.Module):
    def __init__(self, model_name='resnet200d'):
        super().__init__()
        self.model = timm.create_model(model_name, pretrained=False)
        n_features = self.model.fc.in_features
        self.model.global_pool = nn.Identity()
        self.model.fc = nn.Identity()
        self.pooling = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(n_features, 11)

    def forward(self, x):
        bs = x.size(0)
        features = self.model(x)
        pooled_features = self.pooling(features).view(bs, -1)
        return self.fc(pooled_features)

# %%
@torch.no_grad()
def inference(models, test_loader, device):
    # Keep the established probability-space original/flip ensemble.
    # Sequential views and a modest batch size bound the activation memory.
    for model in models:
        model.eval()
    probs = []
    for images in tqdm(test_loader, total=len(test_loader)):
        images = images.to(device, non_blocking=(device.type == 'cuda'))
        batch_probs = None
        for model in models:
            original = model(images).float().sigmoid()
            flipped = model(images.flip(-1)).float().sigmoid()
            member_probs = (original + flipped) * 0.5
            if batch_probs is None:
                batch_probs = member_probs
            else:
                batch_probs += member_probs
        probs.append((batch_probs / len(models)).cpu().numpy())
    if not probs:
        return np.empty((0, 11), dtype=np.float32)
    return np.concatenate(probs, axis=0)

# %%
MODEL_PATH = '../input/resnet200d-baseline-benchmark-public/resnet200d_fold4_cv954.pth'

# %%
model = ResNet200D()
# Accept raw state dicts and common training-checkpoint wrappers. Require every
# parameter to match, rather than silently predicting with uninitialized layers.
try:
    checkpoint = torch.load(MODEL_PATH, map_location=map_location, weights_only=True)
except TypeError:
    # Compatibility with the original Kaggle PyTorch version.
    checkpoint = torch.load(MODEL_PATH, map_location=map_location)
if isinstance(checkpoint, dict):
    for key in ('state_dict', 'model_state_dict', 'model'):
        if key in checkpoint and isinstance(checkpoint[key], dict):
            checkpoint = checkpoint[key]
            break
state_dict = OrderedDict(
    (key[7:] if key.startswith('module.') else key, value)
    for key, value in checkpoint.items()
)
model.load_state_dict(state_dict, strict=True)
del checkpoint, state_dict
model.eval()
models = [model.to(device)]

# %%
test = pd.read_csv(os.path.join(path, 'sample_submission.csv'))
target_cols = test.columns[1:].tolist()
expected_targets = [
    'ETT - Abnormal', 'ETT - Borderline', 'ETT - Normal',
    'NGT - Abnormal', 'NGT - Borderline', 'NGT - Incompletely Imaged',
    'NGT - Normal', 'CVC - Abnormal', 'CVC - Borderline', 'CVC - Normal',
    'Swan Ganz Catheter Present',
]
assert target_cols == expected_targets, 'Unexpected checkpoint/submission label order'
assert np.isclose(sum(weight for _, weight in SCALE_WEIGHTS), 1.0)
predictions = np.zeros((len(test), len(target_cols)), dtype=np.float32)
for image_size, weight in SCALE_WEIGHTS:
    test_dataset = TestDataset(test, transform=get_transforms(image_size))
    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=4,
        pin_memory=(device.type == 'cuda'),
    )
    scale_predictions = inference(models, test_loader, device)
    assert scale_predictions.shape == predictions.shape
    assert np.isfinite(scale_predictions).all()
    # Cache each full-frame / horizontal-flip member for reproducible blending.
    np.savez_compressed(
        f'test_predictions_{image_size}.npz',
        StudyInstanceUID=test['StudyInstanceUID'].to_numpy(dtype=str),
        target_cols=np.asarray(target_cols, dtype=str),
        predictions=scale_predictions,
    )
    predictions += weight * scale_predictions
    del test_loader, test_dataset, scale_predictions

# %%
# AUC depends on ranking: multiplying probabilities by 100 cannot improve it.
# Write actual probabilities in the exact sample-submission row/column order.
assert np.isfinite(predictions).all()
assert ((predictions >= 0.0) & (predictions <= 1.0)).all()
test[target_cols] = predictions
test[['StudyInstanceUID'] + target_cols].to_csv('submission.csv', index=False)
print(test.head())

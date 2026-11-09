# %%
import sys
sys.path.append('../input/timm-pytorch-image-models/pytorch-image-models-master')
import timm

# %%
import numpy as np # linear algebra
import pandas as pd
import os
import glob
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam, SGD
import torchvision.models as models
from torch.nn.parameter import Parameter
from torch.utils.data import DataLoader, Dataset
import pandas as pd
from albumentations import (
    Compose, OneOf, Normalize, Resize, RandomResizedCrop, RandomCrop, HorizontalFlip, VerticalFlip, 
    RandomBrightness, RandomContrast, RandomBrightnessContrast, Rotate, ShiftScaleRotate, Cutout, 
    IAAAdditiveGaussianNoise, Transpose
    )
from albumentations.pytorch import ToTensorV2
from albumentations import ImageOnlyTransform
path = '../input/ranzcr-clip-catheter-line-classification/'
train_labels = pd.read_csv(path+'train.csv')
import timm
import cv2
from tqdm.notebook import tqdm
# Images are loaded at the largest resolution; extra TTA resolutions are produced on-GPU by interpolation.
IMAGE_SIZE = 640
TTA_SIZES = [640, 512]   # multi-resolution TTA (512 and 640 both scored ~0.960 with ImageNet normalization)
BATCH_SIZE = 32
TEST_PATH = '../input/ranzcr-clip-catheter-line-classification/test'
#export CUDA_VISIBLE_DEVICES=""
from torch.cuda.amp import autocast, GradScaler

# %%
if torch.cuda.is_available():
    map_location=lambda storage, loc: storage.cuda()
else:
    map_location='cpu'

# %%
if torch.cuda.is_available():
    device= 'cuda'
else:
    device='cpu'
print(device)

# %%
class TestDataset(Dataset):
    def __init__(self, df, transform=None):
        self.df = df
        self.file_names = df['StudyInstanceUID'].values
        self.transform = transform
        
    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        file_name = self.file_names[idx]
        file_path = f'{TEST_PATH}/{file_name}.jpg'
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
        return image

# %%
def get_transforms():
    # Restore the ImageNet normalization that the public resnet200d checkpoint was trained with.
    # Versions v13/v14 (0.96062) used exactly these statistics; every later deviation from them
    # (v16-v21) lowered the leaderboard score.
    return Compose([
        Resize(IMAGE_SIZE, IMAGE_SIZE),
        Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
        ToTensorV2()
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
        output = self.fc(pooled_features)
        return output

# %%
def inference(models, test_loader, device):
    tk0 = tqdm(enumerate(test_loader), total=len(test_loader))
    probs = []
    use_amp = (device == 'cuda')
    for i, (images) in tk0:
        images = images.to(device)
        avg_preds = []
        for model in models:
            view_preds = []
            for size in TTA_SIZES:
                if size != images.shape[-1]:
                    x = F.interpolate(images, size=(size, size), mode='bilinear', align_corners=False)
                else:
                    x = images
                with torch.no_grad():
                    with autocast(enabled=use_amp):
                        y_preds1 = model(x)
                        y_preds2 = model(x.flip(-1))
                view_preds.append(y_preds1.float().sigmoid().to('cpu').numpy())
                view_preds.append(y_preds2.float().sigmoid().to('cpu').numpy())
            avg_preds.append(np.mean(view_preds, axis=0))
        avg_preds = np.mean(avg_preds, axis=0)
        probs.append(avg_preds)
    probs = np.concatenate(probs)
    return probs

# %%
MODEL_DIR = '../input/resnet200d-baseline-benchmark-public'
MODEL_PATH = MODEL_DIR + '/resnet200d_fold4_cv954.pth'
# Ensemble every resnet200d fold checkpoint shipped in the same public dataset (fold averaging);
# fall back to the single proven fold4 checkpoint if no siblings are found.
MODEL_PATHS = sorted(glob.glob(MODEL_DIR + '/resnet200d*.pth'))
if MODEL_PATH not in MODEL_PATHS and os.path.exists(MODEL_PATH):
    MODEL_PATHS.append(MODEL_PATH)
if len(MODEL_PATHS) == 0:
    MODEL_PATHS = [MODEL_PATH]
print('checkpoints:', MODEL_PATHS)

# %%
models = []
for p in MODEL_PATHS:
    model = ResNet200D()
    #model = nn.DataParallel(model)
    state = torch.load(p, map_location=map_location)
    if isinstance(state, dict) and 'model' in state:
        state = state['model']
    missing, unexpected = model.load_state_dict(state, strict=False)
    if len(missing) > 0 or len(unexpected) > 0:
        print(p, 'missing:', len(missing), 'unexpected:', len(unexpected))
    model.eval()
    models.append(model.to(device))
print('ensemble size:', len(models))

# %%
test = pd.read_csv('../input/ranzcr-clip-catheter-line-classification/sample_submission.csv')
test_dataset = TestDataset(test, transform=get_transforms())
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, 
                         num_workers=4 , pin_memory=True)
predictions = inference(models, test_loader, device)


# %%
# AUC is rank-based, so the old *100 / *50 scaling never changed the score; write plain probabilities.
target_cols = test.iloc[:, 1:12].columns.tolist()
test[target_cols] = predictions
test[['StudyInstanceUID'] + target_cols].to_csv('submission.csv', index=False)
test.head()

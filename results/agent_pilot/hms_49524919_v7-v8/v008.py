# %% [markdown]
# ## HMS - Harmful Brain Activity Classification - Inference

# %% [markdown]
# ## 1. Setup

# %%
import os
import yaml
from pathlib import Path
from tqdm import tqdm

import numpy as np
import pandas as pd

import torch
import torch.nn as nn
import torch.nn.functional as F
import timm

import albumentations as A
from albumentations import ImageOnlyTransform
from albumentations.pytorch.transforms import ToTensorV2

# %%
competition_dataset_directory = Path('/kaggle/input/hms-harmful-brain-activity-classification')
external_dataset_directory = Path('/kaggle/input/hms-hbac-dataset')

# %%
eeg_directory = competition_dataset_directory / 'test_eegs'
spectrogram_directory = competition_dataset_directory / 'test_spectrograms'
df = pd.read_csv(competition_dataset_directory / 'test.csv')

print(f'Test Set Shape: {df.shape} - EEG Files: {len(os.listdir(eeg_directory))} - Spectrogram Files: {len(os.listdir(spectrogram_directory))}')

df

# %% [markdown]
# ## Models

# %%
class ClassificationHead(nn.Module):

    def __init__(self, input_dimensions, output_dimensions):

        super(ClassificationHead, self).__init__()

        self.classifier = nn.Linear(input_dimensions, output_dimensions, bias=True)

    def forward(self, x):

        output = self.classifier(x)

        return output


# %%
class EfficientNetClassificationModel(nn.Module):

    def __init__(self, model_name, pretrained, backbone_args, pooling_type, dropout_rate, freeze_parameters, head_args):

        super(EfficientNetClassificationModel, self).__init__()

        self.backbone = timm.create_model(
            model_name=model_name,
            pretrained=pretrained,
            **backbone_args
        )

        if freeze_parameters:
            for parameter in self.backbone.parameters():
                parameter.requires_grad = False

        input_features = self.backbone.get_classifier().in_features

        self.pooling_type = pooling_type
        self.dropout = nn.Dropout(dropout_rate) if dropout_rate > 0 else nn.Identity()
        self.head = ClassificationHead(input_dimensions=input_features, **head_args)

    def forward(self, x):

        x = self.backbone.forward_features(x)

        if self.pooling_type == 'avg':
            x = F.adaptive_avg_pool2d(x, output_size=(1, 1)).view(x.size(0), -1)
        elif self.pooling_type == 'max':
            x = F.adaptive_max_pool2d(x, output_size=(1, 1)).view(x.size(0), -1)
        elif self.pooling_type == 'concat':
            x = torch.cat([
                F.adaptive_avg_pool2d(x, output_size=(1, 1)).view(x.size(0), -1),
                F.adaptive_max_pool2d(x, output_size=(1, 1)).view(x.size(0), -1)
            ], dim=-1)

        x = self.dropout(x)
        output = self.head(x)

        return output


# %%
def load_timm_model(model_directory, model_file_names, device):

    """
    Load model and pretrained weights from the given model directory

    Parameters
    ----------
    model_directory: pathlib.Path
        Path of the model directory

    model_file_names: list
        List of names of the model weights files

    device: torch.device
        Location of the model

    Returns
    -------
    model: dict
        Dictionary of models with pretrained weights loaded

    config: dict
        Dictionary of configurations
    """

    config = yaml.load(open(model_directory / 'config.yaml', 'r'), Loader=yaml.FullLoader)
    config['model']['model_args']['pretrained'] = False

    models = {}

    for model_file_name in model_file_names:
        model = eval(config['model']['model_class'])(**config['model']['model_args'])
        model.load_state_dict(torch.load(model_directory / model_file_name))
        model.to(device)
        model.eval()
        models[model_file_name] = model

    return models, config


# %%
model_directory_names = [
    'efficientnetv2_spectrogram',
    'efficientnetv2tiny_spectrogram_v1.1',
    'efficientnetv2tiny_spectrogram_v1.2',
    'efficientnetv2tiny_spectrogram_v1.3',
]

model_sets = []

for model_directory_name in model_directory_names:
    models, config = load_timm_model(
        model_directory=external_dataset_directory / model_directory_name,
        model_file_names=[
            'model_fold1_best.pt',
            'model_fold2_best.pt',
            'model_fold3_best.pt',
            'model_fold4_best.pt',
            'model_fold5_best.pt',
        ],
        device=torch.device('cuda')
    )
    model_sets.append(models)


# %%
config

# %% [markdown]
# ## Inference

# %%
class InstanceNormalization(ImageOnlyTransform):

    def apply(self, image, eps=1e-6, **kwargs):

        """
        Normalize image by mean and standard deviation of itself

        Parameters
        ----------
        image: numpy.ndarray of shape (height, width, channel)
             Image array

        Returns
        -------
        image: numpy.ndarray of shape (height, width, channel)
            Normalized image array
        """

        mean = np.mean(image)
        std = np.std(image)
        image = (image - mean) / (std + eps)

        return image


# %%
device = torch.device('cuda')
amp = True
tta = False

transforms = A.Compose([
    InstanceNormalization(always_apply=True),
    ToTensorV2(always_apply=True)
])

# %%
test_spectrogram_predictions = []
spectrogram_prediction_cache = {}

for idx, row in tqdm(df.iterrows(), total=df.shape[0]):
    
    if int(row["spectrogram_id"]) in spectrogram_prediction_cache:
        test_spectrogram_predictions.append(spectrogram_prediction_cache[int(row["spectrogram_id"])])
        continue
    
    spectrogram_path = spectrogram_directory / f'{int(row["spectrogram_id"])}.parquet'
    spectrogram = pd.read_parquet(spectrogram_path).iloc[:, 1:]
    spectrogram = spectrogram.ffill().bfill().values
    
    spectrogram = np.clip(spectrogram, np.exp(-4), np.exp(8))
    spectrogram = np.log(spectrogram)
    spectrogram = spectrogram.T[..., None]
    
    inputs = transforms(image=spectrogram)['image'].float()
    inputs = inputs.to(device)
    
    spectrogram_predictions = torch.zeros(1, 6)

    if tta:
        inputs = torch.stack((
            inputs,
            #torch.flip(inputs, dims=(1,)),
            torch.flip(inputs, dims=(2,)),
            #torch.flip(inputs, dims=(1, 2))
        ), dim=0)
    else:
        inputs = torch.unsqueeze(inputs, dim=0)

    for model_idx, models in enumerate(model_sets):
        for model in models.values():
            with torch.no_grad():
                if amp:
                    with torch.autocast(device_type='cuda', dtype=torch.float16):
                        outputs = model(inputs)
                    if not torch.isfinite(outputs).all():
                        outputs = model(inputs)
                else:
                    outputs = model(inputs)

            outputs = outputs.cpu()
            if tta:
                outputs = torch.mean(outputs, dim=0)
            else:
                outputs = torch.squeeze(outputs, dim=0)
            
            spectrogram_predictions += outputs / (len(models) * len(model_sets))
    
    spectrogram_predictions = torch.softmax(spectrogram_predictions, dim=-1).numpy()
    spectrogram_prediction_cache[int(row["spectrogram_id"])] = spectrogram_predictions
    test_spectrogram_predictions.append(spectrogram_predictions)

test_spectrogram_predictions = np.concatenate(test_spectrogram_predictions)

# %% [markdown]
# ## Submission

# %%
target_columns = ['seizure_vote', 'lpd_vote', 'gpd_vote', 'lrda_vote', 'grda_vote', 'other_vote']
df[target_columns] = test_spectrogram_predictions
df

# %%
df_submission = df.loc[:, ['eeg_id'] + target_columns]
df_submission

# %%
df_submission.to_csv('submission.csv', index=False)

# %%


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
import scipy
import cv2

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
'''spectrogram_models, spectrogram_models_config = load_timm_model(
    model_directory=external_dataset_directory / 'spectrogram_subsample_efficientnetv2tiny_v1.3',
    model_file_names=[
        'model_fold1_best.pt',
        'model_fold2_best.pt',
        'model_fold3_best.pt',
        'model_fold4_best.pt',
        'model_fold5_best.pt',
    ],
    device=torch.device('cuda')
)'''

# %% [markdown]
# ## Raw EEG Models

# %% [markdown]
# ### EEGNet

# %%
class ResNet1DBlock(nn.Module):

    def __init__(self, in_channels, out_channels, kernel_size, stride, padding, downsampling):

        super(ResNet1DBlock, self).__init__()

        self.conv1 = nn.Conv1d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, padding=padding, bias=True)
        self.bn1 = nn.BatchNorm1d(num_features=in_channels)
        self.activation = nn.LeakyReLU(inplace=False)
        self.conv2 = nn.Conv1d(in_channels=out_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, padding=padding, bias=True)
        self.bn2 = nn.BatchNorm1d(num_features=out_channels)
        self.pooling = nn.MaxPool1d(kernel_size=2, stride=2, padding=0)
        self.downsampling = downsampling

    def forward(self, x):

        identity = x

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.activation(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.pooling(x)

        identity = self.downsampling(identity)
        outputs = x + identity
        outputs = self.activation(outputs)

        return outputs


class EEGNet(nn.Module):

    def __init__(self, in_channels, kernels, fixed_kernel_size, head_args):

        super(EEGNet, self).__init__()

        self.in_channels = in_channels
        self.kernels = kernels
        self.planes = 128
        self.parallel_conv = nn.ModuleList()

        for i, kernel_size in enumerate(self.kernels):
            sep_conv = nn.Conv1d(in_channels=in_channels, out_channels=self.planes, kernel_size=kernel_size, stride=1, padding=0, bias=False)
            self.parallel_conv.append(sep_conv)

        self.bn1 = nn.BatchNorm1d(num_features=self.planes)
        self.activation = nn.LeakyReLU(inplace=False)
        self.conv1 = nn.Conv1d(in_channels=self.planes, out_channels=self.planes, kernel_size=fixed_kernel_size, stride=2, padding=2, bias=False)
        self.res_blocks = self._make_resnet_layer(kernel_size=fixed_kernel_size, stride=1, padding=fixed_kernel_size // 2)
        self.bn2 = nn.BatchNorm1d(num_features=self.planes)
        self.pooling = nn.AvgPool1d(kernel_size=6, stride=6, padding=2)
        self.head = ClassificationHead(input_dimensions=256, **head_args)

    def _make_resnet_layer(self, kernel_size, stride, blocks=11, padding=0):

        layers = []

        for i in range(blocks):
            downsampling = nn.MaxPool1d(kernel_size=2, stride=2, padding=0)
            res_block = ResNet1DBlock(
                in_channels=self.planes,
                out_channels=self.planes,
                kernel_size=kernel_size,
                stride=stride,
                padding=padding,
                downsampling=downsampling
            )
            layers.append(res_block)

        return nn.Sequential(*layers)

    def forward(self, x):

        out_sep = []

        for i in range(len(self.kernels)):
            sep = self.parallel_conv[i](x)
            out_sep.append(sep)

        x = torch.cat(out_sep, dim=2)
        x = self.bn1(x)
        x = self.activation(x)
        x = self.conv1(x)

        x = self.res_blocks(x)
        x = self.bn2(x)
        x = self.activation(x)
        x = self.pooling(x)

        x = x.reshape(x.shape[0], -1)
        outputs = self.head(x)

        return outputs


# %%
def load_eegnet_model(model_directory, model_file_names, device):

    """
    Load model and pretrained weights from the given model directory for EEGNet model

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

    models = {}

    for model_file_name in model_file_names:
        model = EEGNet(**config['model']['model_args'])
        model.load_state_dict(torch.load(model_directory / model_file_name))
        model.to(device)
        model.eval()
        models[model_file_name] = model

    return models, config


# %%
raw_eeg_1d_eegnet_models, raw_eeg_1d_eegnet_models_config = load_eegnet_model(
    model_directory=external_dataset_directory / 'raw_eeg_1d_eegnet_19x10000_quality_2',
    model_file_names=[
        'model_fold_1_epoch_19_best_sq_2_kl_divergence_0.3802.pt',
        'model_fold_2_epoch_30_best_sq_2_kl_divergence_0.3875.pt',
        'model_fold_3_epoch_6_best_sq_2_kl_divergence_0.3984.pt',
        'model_fold_4_epoch_18_best_sq_2_kl_divergence_0.3984.pt',
        'model_fold_5_epoch_6_best_sq_2_kl_divergence_0.4155.pt'
    ],
    device=torch.device('cuda')
)

# %% [markdown]
# ## Raw EEG Transforms

# %%
class ChannelDifference(ImageOnlyTransform):

    def __init__(self, ekg, always_apply=True, p=1.0):

        super(ChannelDifference, self).__init__(always_apply=always_apply, p=p)

        self.ekg = ekg

    def apply(self, inputs, **kwargs):

        """
        Create difference features

        Parameters
        ----------
        inputs: numpy.ndarray of shape (time, 20)
             Inputs array

        Returns
        -------
        inputs: numpy.ndarray of shape (time, 19)
            Inputs array with difference features
        """

        n_channels = 19 if self.ekg else 18
        inputs_difference = np.zeros((inputs.shape[0], n_channels))

        inputs_difference[:, 0] = inputs[:, 0] - inputs[:, 4]
        inputs_difference[:, 1] = inputs[:, 4] - inputs[:, 5]
        inputs_difference[:, 2] = inputs[:, 5] - inputs[:, 6]
        inputs_difference[:, 3] = inputs[:, 6] - inputs[:, 7]

        inputs_difference[:, 4] = inputs[:, 11] - inputs[:, 15]
        inputs_difference[:, 5] = inputs[:, 15] - inputs[:, 16]
        inputs_difference[:, 6] = inputs[:, 16] - inputs[:, 17]
        inputs_difference[:, 7] = inputs[:, 17] - inputs[:, 18]

        inputs_difference[:, 8] = inputs[:, 0] - inputs[:, 1]
        inputs_difference[:, 9] = inputs[:, 1] - inputs[:, 2]
        inputs_difference[:, 10] = inputs[:, 2] - inputs[:, 3]
        inputs_difference[:, 11] = inputs[:, 3] - inputs[:, 7]

        inputs_difference[:, 12] = inputs[:, 11] - inputs[:, 12]
        inputs_difference[:, 13] = inputs[:, 12] - inputs[:, 13]
        inputs_difference[:, 14] = inputs[:, 13] - inputs[:, 14]
        inputs_difference[:, 15] = inputs[:, 14] - inputs[:, 18]

        inputs_difference[:, 16] = inputs[:, 8] - inputs[:, 9]
        inputs_difference[:, 17] = inputs[:, 9] - inputs[:, 10]

        if self.ekg:
            inputs_difference[:, 18] = inputs[:, 19]

        return inputs_difference


class InstanceNormalization1D(ImageOnlyTransform):

    def __init__(self, per_channel, epsilon=1e-15, always_apply=True, p=1.0):

        super(InstanceNormalization1D, self).__init__(always_apply=always_apply, p=p)

        self.per_channel = per_channel
        self.epsilon = epsilon

    def apply(self, inputs, **kwargs):

        """
        Normalize inputs by mean and standard deviation of itself

        Parameters
        ----------
        inputs: numpy.ndarray of shape (time, channel)
             Inputs array

        Returns
        -------
        inputs: numpy.ndarray of shape (time, channel)
            Normalized inputs array
        """

        if self.per_channel:
            axis = 0
        else:
            axis = (0, 1)

        mean = np.mean(inputs, axis=axis)
        std = np.std(inputs, axis=axis)
        inputs = (inputs - mean) / (std + self.epsilon)

        return inputs


class SignalFilter(ImageOnlyTransform):

    def __init__(self, always_apply=True, p=1.0):

        super(SignalFilter, self).__init__(always_apply=always_apply, p=p)
        
        self.filter = scipy.signal.butter(3, [0.001, 20], btype='bandpass', fs=200, output='sos')

    def apply(self, inputs, **kwargs):

        """
        Filter inputs

        Parameters
        ----------
        inputs: numpy.ndarray of shape (time, channel)
             Inputs array

        Returns
        -------
        inputs: numpy.ndarray of shape (time, channel)
            Filtered inputs array
        """
        
        inputs = scipy.signal.sosfilt(self.filter, inputs, axis=0).astype(np.float32)

        return inputs


class CenterTemporalDropout1D(ImageOnlyTransform):

    def __init__(self, n_time_steps, drop_value=0, always_apply=False, p=0.5):

        super(CenterTemporalDropout1D, self).__init__(always_apply=always_apply, p=p)

        self.n_time_steps = n_time_steps
        self.drop_value = drop_value

    def apply(self, inputs, **kwargs):

        """
        Drop time steps from center 10 seconds randomly

        Parameters
        ----------
        inputs: numpy.ndarray of shape (height, width, channel)
             Inputs array

        Returns
        -------
        inputs: numpy.ndarray of shape (height, width, channel)
            Inputs array with dropped time steps from center 10 seconds
        """

        # Uniformly sample N amount of indices to drop on time axis from center 10 seconds
        center_start = 4000
        center_end = 6000
        drop_idx = np.random.choice(np.arange(center_start, center_end + 1), self.n_time_steps, replace=False)
        inputs[drop_idx, :] = self.drop_value

        return inputs


class NonCenterTemporalDropout1D(ImageOnlyTransform):

    def __init__(self, n_time_steps, drop_value=0, always_apply=False, p=0.5):

        super(NonCenterTemporalDropout1D, self).__init__(always_apply=always_apply, p=p)

        self.n_time_steps = n_time_steps
        self.drop_value = drop_value

    def apply(self, inputs, **kwargs):

        """
        Drop time steps from other than center 10 seconds randomly

        Parameters
        ----------
        inputs: numpy.ndarray of shape (height, width, channel)
             Inputs array

        Returns
        -------
        inputs: numpy.ndarray of shape (height, width, channel)
            Inputs array with dropped time steps except from center 10 seconds
        """

        # Uniformly sample N amount of indices to drop on time axis everywhere except from center 10 seconds
        center_10_seconds_start = 4000
        center_10_seconds_end = 6000
        drop_idx = np.random.choice(
            np.arange(0, center_10_seconds_start).tolist() + np.arange(center_10_seconds_end + 1, inputs.shape[1]).tolist(),
            self.n_time_steps,
            replace=False
        )
        inputs[drop_idx, :] = self.drop_value

        return inputs


class ToTensor1D(ImageOnlyTransform):

    def __init__(self, always_apply=True, p=1.0):

        super(ToTensor1D, self).__init__(always_apply=always_apply, p=p)

    def apply(self, inputs, **kwargs):

        """
        Convert inputs array to a torch tensor and transpose it

        Parameters
        ----------
        inputs: numpy.ndarray of shape (time, channel)
             Inputs array

        Returns
        -------
        inputs: torch.Tensor of shape (channel, time)
            Transposed inputs tensor
        """

        inputs = torch.as_tensor(inputs.T, dtype=torch.float32)

        return inputs


# %%
def get_raw_eeg_1d_transforms(**transform_parameters):

    """
    Get raw EEG 1D transforms for dataset

    Parameters
    ----------
    transform_parameters: dict
        Dictionary of transform parameters

    Returns
    -------
    eeg_transforms: dict
        Transforms for training and inference
    """

    training_transforms = A.Compose([
        ChannelDifference(ekg=True, always_apply=True),
        A.VerticalFlip(p=transform_parameters['vertical_flip_probability']),
        A.HorizontalFlip(p=transform_parameters['horizontal_flip_probability']),
        CenterTemporalDropout1D(
            n_time_steps=transform_parameters['center_temporal_dropout_time_steps'],
            drop_value=0,
            p=transform_parameters['center_temporal_dropout_probability']
        ),
        NonCenterTemporalDropout1D(
            n_time_steps=transform_parameters['non_center_temporal_dropout_time_steps'],
            drop_value=0,
            p=transform_parameters['non_center_temporal_dropout_probability']
        ),
        InstanceNormalization1D(per_channel=True, always_apply=True),
        ToTensor1D(always_apply=True)
    ])

    inference_transforms = A.Compose([
        ChannelDifference(ekg=True, always_apply=True),
        InstanceNormalization1D(per_channel=True, always_apply=True),
        ToTensor1D(always_apply=True)
    ])

    eeg_transforms = {'training': training_transforms, 'inference': inference_transforms}
    return eeg_transforms


# %% [markdown]
# ## Inference

# %%
device = torch.device('cuda')
amp = True

raw_eeg_1d_transforms = get_raw_eeg_1d_transforms(**raw_eeg_1d_eegnet_models_config['transforms'])['inference']
raw_eeg_1d_tta = True
raw_eeg_1d_task_type = 'binary'
# Ensemble in probability space (each TTA view and each fold model converted to a
# normalized distribution first, then averaged) instead of averaging raw logits.
probability_space_ensemble = True
# Floor applied to final probabilities before renormalization to guard KL divergence
# against overconfident mistakes on a handful of samples.
probability_floor = 1e-3


def logits_to_probabilities(logits, task_type):

    """
    Convert model outputs to normalized probability distributions

    Parameters
    ----------
    logits: torch.Tensor of shape (n, 6)
        Raw model outputs

    task_type: str
        'binary' (sigmoid + normalize) or 'multiclass' (softmax)

    Returns
    -------
    probabilities: torch.Tensor of shape (n, 6)
        Probabilities that sum to 1 on the last axis
    """

    logits = logits.float()
    if task_type == 'binary':
        probabilities = torch.sigmoid(logits)
        probabilities = probabilities / probabilities.sum(dim=-1, keepdim=True)
    else:
        probabilities = torch.softmax(logits, dim=-1)

    return probabilities

# %%
test_raw_eeg_1d_predictions = []

for idx, row in df.iterrows():
    
    eeg_path = eeg_directory / f'{int(row["eeg_id"])}.parquet'
    eeg = pd.read_parquet(eeg_path)
    eeg = eeg.interpolate(method='linear', limit_area='inside')
    eeg = eeg.fillna(0).values
        
    raw_eeg_1d_inputs = raw_eeg_1d_transforms(image=eeg)['image'].float()
    raw_eeg_1d_inputs = raw_eeg_1d_inputs.to(device)
    
    raw_eeg_1d_predictions = torch.zeros(1, 6)
    n_models_total = sum(len(models) for models in [raw_eeg_1d_eegnet_models])

    if raw_eeg_1d_tta:
        raw_eeg_1d_inputs = torch.stack((
            raw_eeg_1d_inputs,
            torch.flip(raw_eeg_1d_inputs, dims=(0,)),
            torch.flip(raw_eeg_1d_inputs, dims=(1,)),
            torch.flip(raw_eeg_1d_inputs, dims=(0, 1))
        ), dim=0)
    else:
        raw_eeg_1d_inputs = torch.unsqueeze(raw_eeg_1d_inputs, dim=0)

    for model_idx, models in enumerate([raw_eeg_1d_eegnet_models]):
        for model in models.values():
            with torch.no_grad():
                if amp:
                    with torch.autocast(device_type='cuda', dtype=torch.float16):
                        raw_eeg_1d_outputs = model(raw_eeg_1d_inputs)
                else:
                    raw_eeg_1d_outputs = model(raw_eeg_1d_inputs)

            raw_eeg_1d_outputs = raw_eeg_1d_outputs.cpu().float()

            if probability_space_ensemble:
                # Convert every TTA view to a distribution, then average views and models
                raw_eeg_1d_outputs = logits_to_probabilities(raw_eeg_1d_outputs, raw_eeg_1d_task_type)

            raw_eeg_1d_outputs = torch.mean(raw_eeg_1d_outputs, dim=0, keepdim=True)
            raw_eeg_1d_predictions += raw_eeg_1d_outputs / n_models_total

    if probability_space_ensemble:
        raw_eeg_1d_predictions = raw_eeg_1d_predictions.numpy()
    else:
        raw_eeg_1d_predictions = logits_to_probabilities(raw_eeg_1d_predictions, raw_eeg_1d_task_type).numpy()

    # Floor and renormalize
    raw_eeg_1d_predictions = np.clip(raw_eeg_1d_predictions, probability_floor, 1.0)
    raw_eeg_1d_predictions = raw_eeg_1d_predictions / raw_eeg_1d_predictions.sum(axis=1, keepdims=True)

    test_raw_eeg_1d_predictions.append(raw_eeg_1d_predictions)

test_raw_eeg_1d_predictions = np.concatenate(test_raw_eeg_1d_predictions)
test_raw_eeg_1d_predictions

# %% [markdown]
# ## Post-processing

# %%
def normalize_probabilities(df, columns):

    """
    Normalize probabilities to 1 within given columns

    Parameters
    ----------
    df: pandas.DataFrame
        Dataframe with given columns

    columns: list
        List of column names that have probabilities

    Returns
    -------
    df: pandas.DataFrame
        Dataframe with given columns' sum adjusted to 1
    """

    df_sums = df[columns].sum(axis=1)
    for column in columns:
        df[column] /= df_sums

    return df


# %%
target_columns = ['seizure_vote', 'lpd_vote', 'gpd_vote', 'lrda_vote', 'grda_vote', 'other_vote']
raw_eeg_1d_prediction_columns = [f'{column}_raw_eeg_1d_prediction' for column in target_columns]

df[raw_eeg_1d_prediction_columns] = test_raw_eeg_1d_predictions

#df['seizure_vote_spectrogram_prediction'] *= 1.
#df['lpd_vote_spectrogram_prediction'] *= 1.5
#df['gpd_vote_spectrogram_prediction'] *= 1.5
#df['lrda_vote_spectrogram_prediction'] *= 1.75
#df['grda_vote_spectrogram_prediction'] *= 1.5
#df['other_vote_spectrogram_prediction'] *= 1.

df = normalize_probabilities(df=df, columns=raw_eeg_1d_prediction_columns)
df

# %% [markdown]
# ## Submission

# %%
df_submission = df.loc[:, ['eeg_id']]
df_submission[target_columns] = df[raw_eeg_1d_prediction_columns]
df_submission

# %%
df_submission.to_csv('submission.csv', index=False)

# %%


# %%


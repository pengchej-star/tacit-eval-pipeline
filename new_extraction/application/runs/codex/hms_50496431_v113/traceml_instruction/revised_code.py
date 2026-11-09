# %%
#import

import random
import cv2
import json
import numpy as np
import copy
import pandas as pd
import torch
import gc

import albumentations as A
import os
import librosa
import pickle
import timm
from tqdm import tqdm

import mne

import torch
import torchaudio
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision.models.video.mvit import mvit_v2_s

# %%
import shutil
shutil.copy2("/kaggle/input/torchvideo/r50.py", "r50.py")
shutil.copy2("/kaggle/input/torchvideo/x3d.py", "x3d.py")
from r50 import create_r2plus1d
from x3d import create_x3d

# %%
CFG={
    'batch_size':32,
    'num_worker':4,
    'data':'/kaggle/input/hms-harmful-brain-activity-classification/test.csv',
    'weights_spec':'/kaggle/input/hms-baseline',
    'weights_mix':'/kaggle/input/hms-mix',
    'weights_one_image':'/kaggle/input/hms-oneimage',
    'weights_3d':'/kaggle/input/hms-3d',
    'weights_x3d':'/kaggle/input/hms-x3d',
    'weights_doublehead':'/kaggle/input/hms-double-head',
    'weights_eeg_raw':'/kaggle/input/hms-eeg-raw',
    'flip':True
}

# %%
# Only enumerate checkpoints for the families used in this submission.
# Keep every supplied checkpoint within each family, with equal fold weights.
for key in ('weights_x3d', 'weights_eeg_raw'):
    checkpoint_dir = CFG[key]
    CFG[key] = [os.path.join(checkpoint_dir, name)
                for name in sorted(os.listdir(checkpoint_dir))
                if os.path.isfile(os.path.join(checkpoint_dir, name))]
    if not CFG[key]:
        raise RuntimeError(f"No checkpoints found in {checkpoint_dir}")

random.seed(2024)
np.random.seed(2024)
torch.manual_seed(2024)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(2024)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

CFG

# %%
# #make eeg specs
# import os
# import pickle

# import librosa
# import numpy as np
# import pandas as pd
# import torch
# import torchaudio
# from torch import nn
# from tqdm import tqdm
# data_dir='/kaggle/input/hms-harmful-brain-activity-classification/test_eegs'
# NAMES = ['LL', 'LP', 'RP', 'RR']

# FEATS = [['Fp1', 'F7', 'T3', 'T5', 'O1'],
#          ['Fp1', 'F3', 'C3', 'P3', 'O1'],
#          ['Fp2', 'F8', 'T4', 'T6', 'O2'],
#          ['Fp2', 'F4', 'C4', 'P4', 'O2']]



# class Transform(nn.Module):
#     def __init__(self, ):
#         super().__init__()

#         self.wave_transform = torchaudio.transforms.MelSpectrogram(sample_rate=200,
#                                                           hop_length=10000// 256,
#                                                           n_fft=1024,
#                                                           n_mels=128,
#                                                           f_min=0, f_max=20,
#                                                           win_length=128)

#         # self.am2db= torchaudio.transforms.AmplitudeToDB(stype='power',
#         #                                                 top_db=80)


#     def forward(self, x):
#         bs = x.size(0)


#         image = self.wave_transform(x)
#         # image = self.am2db(image)
#         return image


# transform_func=Transform().to('cuda')
# def spectrogram_from_eeg( parquet_path, display=False):
#     # LOAD MIDDLE 50 SECONDS OF EEG SERIES
#     eeg = pd.read_parquet(parquet_path)
#     middle = (len(eeg) - 10_000) // 2
#     eeg = eeg.iloc[middle:middle + 10_000]

#     # VARIABLE TO HOLD SPECTROGRAM
#     img = np.zeros((128, 256, 4), dtype='float32')

#     signals = []
#     for k in range(4):
#         COLS = FEATS[k]

#         for kk in range(4):

#             # COMPUTE PAIR DIFFERENCES
#             x = eeg[COLS[kk]].values - eeg[COLS[kk + 1]].values

#             # FILL NANS
#             m = np.nanmean(x)
#             if np.isnan(x).mean() < 1:
#                 x = np.nan_to_num(x, nan=m)
#             else:
#                 x[:] = 0


#             x_tensor=torch.from_numpy(x).to('cuda')
#             mel_spec=transform_func(x_tensor)
#             mel_spec=mel_spec.cpu().numpy()
#             # LOG TRANSFORM

#             width = (mel_spec.shape[1] // 32) * 32
#             mel_spec_db = librosa.power_to_db(mel_spec,
#                                               ref=np.max).astype(np.float32)[:, :width]

            
#             img[:, :, k] += mel_spec_db
            
#         # AVERAGE THE 4 MONTAGE DIFFERENCES
#         img[:, :, k] /= 4.0

#     return img


# all_fs=os.listdir(data_dir)
# all_specs={}



# for item in tqdm(all_fs):

#     eeg_id=item.rsplit('.',1)[0]

#     eeg_path = '/kaggle/input/hms-harmful-brain-activity-classification/test_eegs/%s.parquet' % (eeg_id)



#     eeg_spec=spectrogram_from_eeg(eeg_path)

#     all_specs[eeg_id]=eeg_spec




# with open('eeg_specs_dict.pkl', 'wb') as file:
#     pickle.dump(all_specs, file)

# %%
#dataiter
class AlaskaDataIter():
    def __init__(self, df,
                 training_flag=False,shuffle=False,
                 use_spec=False,
                 use_eeg=False,
                 use_mix=False,
                 ll=0,rr=20,
                 flip=False):
        
        self.flip_eeg=flip
        self.ll=ll
        self.rr=rr
        print(self.ll,self.rr)
        self.training_flag = training_flag
        self.shuffle = shuffle

        self.raw_data_set_size = None     ##decided by self.parse_file


        self.df=df
        
        self.train_trans=A.Compose([

                                    A.HorizontalFlip(p=0.5),

                              ])

        TARS = {'Seizure': 0, 'LPD': 1, 'GPD': 2, 'LRDA': 3, 'GRDA': 4, 'Other': 5}
        self.TARS2 = {x: y for y, x in TARS.items()}


        self.eeg_nms=['Fp1', 'F3', 'C3', 'P3', 'F7', 'T3', 'T5', 'O1', 'Fz', 'Cz', 'Pz',
       'Fp2', 'F4', 'C4', 'P4', 'F8', 'T4', 'T6', 'O2', 'EKG']

        self.LL = ['Fp1', 'F7', 'T3', 'T5', 'O1']

        self.RL = ['Fp2', 'F8', 'T4', 'T6', 'O2']

        self.LP = ['Fp1', 'F3', 'C3', 'P3', 'O1']

        self.RP = ['Fp2', 'F4', 'C4', 'P4', 'O2']

        self.mid = ['Fz', 'Cz', 'Pz']
        self.leads_dict = {value: index for index, value in enumerate(self.eeg_nms)}

        self.use_eeg = use_eeg
        self.use_spec = use_spec
        self.use_mix = use_mix
        
        
        
        
    def __getitem__(self, item):

        return self.single_map_func(self.df.iloc[item], self.training_flag)

    def __len__(self):

        return len(self.df)

    def brain_lead(self, waves):
        waves = copy.deepcopy(waves)

        brain_leads = [self.LL, self.RL, self.LP, self.RP]

        leads = []

        for chain in brain_leads:
            for i in range(len(chain) - 1):
                tmp_lead = waves[self.leads_dict[chain[i]]] - waves[self.leads_dict[chain[i + 1]]]
                leads.append(tmp_lead)

        data = np.concatenate([leads], axis=0)
        
        return data
    def mirror_spec(self, data):

        # index_choice = [[0, 1, 3, 2], [0, 1, 2, 3], [1, 0, 2, 3], [1, 0, 3, 2]]
        indx = [1, 0, 3, 2]
        return data[..., indx]

    def mirror_eeg(self, data):

        indx1 = [0, 1, 2, 3, 4, 5, 6, 7]
        indx2 = [11, 12, 13, 14, 15, 16, 17, 18]

        data[indx1, ...], data[indx2, ...] = data[indx2, ...], data[indx1, ...]

        return data
    def get_eeg(self, dp, is_training,flip=False):
        eeg_path = '/kaggle/input/hms-harmful-brain-activity-classification/test_eegs/%s.parquet' % (dp['eeg_id'])
        eeg = pd.read_parquet(eeg_path)

        
        offset = 0
        eeg = eeg.iloc[int(offset * 200):int(offset * 200) + 10000]

        waves = eeg.values

        waves = np.transpose(waves, axes=[1, 0])

        for i in range(waves.shape[0]):
            m = np.nanmean(waves[i])
            if np.isnan(waves[i]).mean() < 1:
                waves[i] = np.nan_to_num(waves[i], nan=m)
            else:
                waves[i] = 0
        
        if flip:
            waves=self.mirror_eeg(waves)
        waves = self.brain_lead(waves)
        waves = np.array(waves, dtype=np.float64)

        waves = np.clip(waves, -1024, 1024)
        

        waves = mne.filter.filter_data(waves, 200, self.ll, self.rr, verbose=False)
        #


        return waves
    def get_spec(self, dp, is_training,flip=False):
        spec_path = '/kaggle/input/hms-harmful-brain-activity-classification/test_spectrograms/%s.parquet' % (dp['spectrogram_id'])
        spec = pd.read_parquet(spec_path)

        spec=spec.values[:,1:]

        images=[]
        r = 0

        for region in range(4):
            img = spec[r:r + 300,
                  region * 100:(region + 1) * 100].T
            img = np.clip(img, np.exp(-4), np.exp(8))
            img = np.log(img)

            # STANDARDIZE PER IMAGE
            # ep = 1e-6
            # m = np.nanmean(img.flatten())
            # s = np.nanstd(img.flatten())
            # img = (img - m) / (s + ep)
            img = np.nan_to_num(img, nan=0.0)

            images.append(img)

        images=np.stack(images,-1)
        
        if flip:
            images = self.mirror_spec(images)
        data = np.transpose(images, [2,0,1])


        return data
    
    def get_mix(self, dp, is_training,flip=False):
        
        eeg_path = '/kaggle/input/hms-harmful-brain-activity-classification/test_eegs/%s.parquet' % (dp['eeg_id'])
        eeg = pd.read_parquet(eeg_path)
        
        offset = 0

        eeg = eeg.iloc[int(offset * 200):int(offset * 200) + 10000]

        waves = eeg.values

        waves = np.transpose(waves, axes=[1, 0])
        for i in range(waves.shape[0]):
            m = np.nanmean(waves[i])
            if np.isnan(waves[i]).mean() < 1:
                waves[i] = np.nan_to_num(waves[i], nan=m)
            else:
                waves[i] = 0

        if flip:
            waves = self.mirror_eeg(waves)
        
        waves = self.brain_lead(waves)
        waves = np.array(waves, dtype=np.float64)

        waves = np.clip(waves, -1024, 1024)

        waves = mne.filter.filter_data(waves, 200, self.ll, self.rr, verbose=False)
        #
        # get spec
        r = 0
        spec_path = '/kaggle/input/hms-harmful-brain-activity-classification/test_spectrograms/%s.parquet' % (dp['spectrogram_id'])
        spec = pd.read_parquet(spec_path)
        spec=spec.values[:,1:]
        

        images = []
        for region in range(4):
            img = spec[r:r + 300, region * 100:(region + 1) * 100].T
            img = np.clip(img, np.exp(-4), np.exp(8))
            img = np.log(img)

            # STANDARDIZE PER IMAGE
            # ep = 1e-6
            # m = np.nanmean(img.flatten())
            # s = np.nanstd(img.flatten())
            # img = (img - m) / (s + ep)
            img = np.nan_to_num(img, nan=0.0)

            images.append(img)

        images = np.stack(images, -1)

        if flip:
            images = self.mirror_spec(images)

        images = np.transpose(images, [2, 0, 1])
        
        
        return waves, images
    
    def single_map_func(self, dp, is_training):
        """Data augmentation function."""
        ####customed here

        
        if self.use_eeg:
            
            data=self.get_eeg(dp,is_training,self.flip_eeg)
        elif self.use_spec:
            data=self.get_spec(dp,is_training,self.flip_eeg)
        elif self.use_mix:
            data,spec =self.get_mix(dp,is_training)
            
            return data.astype(np.float32),spec.astype(np.float32)
        
        return data.astype(np.float32)

# %%



class NetSpec(nn.Module):
    def __init__(self, num_classes=1):
        super().__init__()

        

        self.model = timm.create_model('efficientnet_b5',
                                       pretrained=False,
                                       in_chans=3)

        self.fc = nn.Linear(2048, 6, bias=True)
        # self.wave_encoder = ResNet1D(inp_ch=42, block=ResNetBlock1D, layers=[2, 2, 4, 2], num_classes=1)

        # weight_init(self.fc)
        self.dropout=nn.Dropout(0.5)

        self.avg=nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        # do preprocess
        bs = x.size(0)

        # wave_fm = self.wave_encoder(x)  # 1x250
        # wave_fm = wave_fm.unsqueeze(2)
        #
        x1 = [x[:,  i:i + 1,:, :] for i in range(4)]
        x1 = torch.cat(x1,dim=2)
        x= torch.cat([x1,x1,x1],dim=1)
        

        if CFG['flip']:
            x_flip=torch.flip(x, [3])
            x=torch.cat([x,x_flip],dim=0)

            

        x = self.model.forward_features(x)
        x = self.avg(x)

        if CFG['flip']:
            x = x.view(2*bs, -1)
        else:
            x = x.view(bs, -1)
        x = self.dropout(x)

        x = self.fc(x)
        
        x =torch.softmax(x,-1)
        
        if CFG['flip']:
            ans= (x[:bs,...]+x[bs:,...])/2.
        else:
            ans=x
        return ans




# %%


# %%

class NetMix(nn.Module):
    def __init__(self, num_classes=1):
        super().__init__()

        self.preprocess = Transform()

        self.model = timm.create_model('hrnet_w18',
                                       pretrained=False,
                                       in_chans=3)

        self.fc = nn.Linear(2048, 6, bias=True)
        # self.wave_encoder = ResNet1D(inp_ch=42, block=ResNetBlock1D, layers=[2, 2, 4, 2], num_classes=1)

        # weight_init(self.fc)
        self.dropout=nn.Dropout(0.5)

        self.avg=nn.AdaptiveAvgPool2d(1)


    def forward(self, x):
        # do preprocess
        bs = x.size(0)
        if CFG['flip']:
            x_flip=torch.flip(x, [3])
            x=torch.cat([x,x_flip],dim=0)
            
        x1 = [x[:, i:i + 1, :, :] for i in range(4)]
        x1 = torch.cat(x1, dim=2)

        x2=[x[:, i+4:i + 5, :, :] for i in range(4)]
        x2 = torch.cat(x2, dim=2)

        x= torch.cat([x1,x2],dim=3)

        x = torch.cat([x, x, x], dim=1)
        

            
        x = self.model.forward_features(x)
        x = self.avg(x)
        
        if CFG['flip']:
            x = x.view(2*bs, -1)
        else:
            x = x.view(bs, -1)
        
        x = self.dropout(x)
        x = self.fc(x)

        x =torch.softmax(x,-1)

        if CFG['flip']:
            ans= (x[:bs,...]+x[bs:,...])/2.
        else:
            ans=x
            
        return ans



# %%

class Transform(nn.Module):
    def __init__(self, ):
        super().__init__()

        self.wave_transform = torchaudio.transforms.Spectrogram(n_fft=512, hop_length=50, power=1)

        

    def forward(self, x):
        bs = x.size(0)


        image = self.wave_transform(x)
        image = torch.log10(image)
        image = torch.clip(image, min=0)

        n, c, h, w = image.size()
        image=image[:,:,:int(40/100*h),:]

        image = torch.reshape(image,shape=[n,2,-1,w])


        x1=image[:,0:1,...]
        x2=image[:,1:2,...]

        image=torch.cat([x1,x2],dim=-1)

        image=torch.cat([image,image,image],dim=1)

        return image




class NetOneImage(nn.Module):
    def __init__(self, num_classes=1):
        super().__init__()

        self.preprocess = Transform()

        self.model = timm.create_model('efficientnet_b5',
                                       pretrained=False,
                                       in_chans=3)

        self.fc = nn.Linear(2048, 6, bias=True)
        # self.wave_encoder = ResNet1D(inp_ch=42, block=ResNetBlock1D, layers=[2, 2, 4, 2], num_classes=1)

        # weight_init(self.fc)
        self.dropout=nn.Dropout(0.5)

        self.avg=nn.AdaptiveAvgPool2d(1)


    def forward(self, x):
        # do preprocess
        bs = x.size(0)

        x= self.preprocess(x)
        
        if CFG['flip']:
            x_flip=torch.flip(x, [-1])
            x=torch.cat([x,x_flip],dim=0)
            
            
        x = self.model.forward_features(x)
        x = self.avg(x)
        if CFG['flip']:
            x = x.view(2*bs, -1)
        else:
            x = x.view(bs, -1)
        x = self.dropout(x)

        x = self.fc(x)
        x =torch.softmax(x,-1)
        
        if CFG['flip']:
            ans= (x[:bs,...]+x[bs:,...])/2.
        else:
            ans=x
            
        return ans


# %%

class Transform3d(nn.Module):
    def __init__(self, ):
        super().__init__()

        self.wave_transform = torchaudio.transforms.Spectrogram(n_fft=512,
                                                                
                                                                hop_length=50,
                                                                power=1)

        self.am2db= torchaudio.transforms.AmplitudeToDB(stype='magnitude',top_db=80)

        self.resizer=nn.UpsamplingBilinear2d(size=[160,320])
    def forward(self, x):
        bs = x.size(0)


        image = self.wave_transform(x)
        # image = self.am2db(image)
        image = torch.log10(image)
        image = torch.clip(image, min=0)

        n, c, h, w = image.size()
        image = image[:, :, :int(20 / 100 * h + 30), :]




        return image


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = create_r2plus1d()
        # n_features = self.net._fc.in_features
        # self.net._fc = nn.Linear(in_features=n_features, out_features=6, bias=True)
        
    def forward(self, x):
        out = self.net(x)

        return out


class Net3d(nn.Module):
    def __init__(self, num_classes=1):
        super().__init__()

        self.preprocess = Transform3d()

        self.model = Model()

        self.pool=nn.AdaptiveAvgPool3d(1)
        self.fc = nn.Linear(2048, 6, bias=True)

    def forward(self, x):
        bs = x.size(0)

        x= self.preprocess(x)

        x = torch.unsqueeze(x,dim=1)

        x = torch.cat([x,x,x],dim=1)
        if CFG['flip']:
            x_flip=torch.flip(x, [-1])
            x=torch.cat([x,x_flip],dim=0)
            
        x = self.model(x)

        x = self.pool(x)
        if CFG['flip']:
            x = x.view(2*bs, -1)
        else:
            x = x.view(bs, -1)
            
        
        x= self.fc(x)
        
        x =torch.softmax(x,-1)
        
        if CFG['flip']:
            ans= (x[:bs,...]+x[bs:,...])/2.
        else:
            ans=x
            
        return ans




# %%

class Transformx3d(nn.Module):
    def __init__(self, ):
        super().__init__()

        self.wave_transform = torchaudio.transforms.Spectrogram(n_fft=512,                                      
                                                                hop_length=25,
                                                                power=1)

        self.am2db= torchaudio.transforms.AmplitudeToDB(stype='magnitude',top_db=80)

        self.resizer=nn.UpsamplingBilinear2d(size=[160,320])
    def forward(self, x):
        bs = x.size(0)


        image = self.wave_transform(x)
        # image = self.am2db(image)
        image = torch.log10(image)
        image = torch.clip(image, min=0)

        n, c, h, w = image.size()
        image = image[:, :, :int(40 / 100 * h+10 ), :]



        return image


class Modelx3d(nn.Module):
    def __init__(self):
        super().__init__()
        model_name = "x3d_l"
        self.net = create_x3d(input_clip_length=16,
        input_crop_size=312,
        depth_factor=5.0,)
        
        # self.net.blocks[5]=nn.Identity()
        # self.net.avgpool = nn.Identity()
        self.net.blocks[5].dropout=nn.Identity()
        self.net.blocks[5].proj = nn.Identity()
        self.net.blocks[5].activation = nn.Identity()
        self.net.blocks[5].output_pool = nn.Identity()
    def forward(self, x):

        x = self.net(x)

        return x



class Netx3d(nn.Module):
    def __init__(self, num_classes=1):
        super().__init__()

        self.preprocess = Transformx3d()

        self.model = Modelx3d()

        self.pool=nn.AdaptiveAvgPool3d(1)
        self.fc = nn.Linear(2048, 6, bias=True)

    def forward(self, x):
        bs = x.size(0)

        x= self.preprocess(x)

        x = torch.unsqueeze(x,dim=1)

        x = torch.cat([x,x,x],dim=1)
        if CFG['flip']:
            x_flip=torch.flip(x, [-1])
            x=torch.cat([x,x_flip],dim=0)
            
        x = self.model(x)

#         x = self.pool(x)
        if CFG['flip']:
            x = x.view(2*bs, -1)
        else:
            x = x.view(bs, -1)
            
        
        x= self.fc(x)
        
        x =torch.softmax(x,-1)
        
        if CFG['flip']:
            ans= (x[:bs,...]+x[bs:,...])/2.
        else:
            ans=x
            
        return ans




# %%


class Net1d(nn.Module):
    def __init__(
        self,
    ):
        super(Net1d, self).__init__()





        self.model_doc=timm.create_model('efficientnet_b5',
                                            pretrained=False,
                                            in_chans=3,)

        
        self.neck=nn.Linear(79*2,1,bias=True)
        self.pool=nn.AdaptiveAvgPool2d(1)
        self.fc=nn.Linear(2048,out_features=6,bias=True)


        self.dropout=nn.Dropout(p=0.5)


    def extract_features(self, x):


        bs=x.size(0)
        x=self.model_doc.forward_features(x)

        x=x.view(bs,2048,-1)

        x= self.neck(x)

        return x

    def forward(self, x):
        bs = x.size(0)
        reshaped_tensor = x.view(bs,16,2500, 4)

        reshaped_and_permuted_tensor = reshaped_tensor.permute(0,1,3,2)

        reshaped_and_permuted_tensor= reshaped_and_permuted_tensor.reshape(bs,16*4,2500)

        x=torch.unsqueeze(reshaped_and_permuted_tensor,dim=1)

        x=torch.cat([x,x,x],dim=1)
        bs=x.size(0)


        x = self.extract_features(x)


#         x = self.pool(x)
        x = x.view(bs,-1)

        x =self.dropout(x)
        x = self.fc(x)
        x =torch.softmax(x,-1)
        return x



# %%

class Modeleeg(nn.Module):
    def __init__(self,):
        super(Modeleeg, self).__init__()





        self.model=timm.create_model('efficientnet_b5',
                                            pretrained=False,
                                            in_chans=3,)



        self.pool=nn.AdaptiveAvgPool2d(1)
        self.fc=nn.Linear(2048,out_features=6,bias=True)

    def extract_features(self, x):


        feature1=self.model.forward_features(x)

        return feature1
    
    def forward(self, x):
        bs = x.size(0)
        reshaped_tensor = x.view(bs,16,500, 20)

        reshaped_and_permuted_tensor = reshaped_tensor.permute(0,1,3,2)

        reshaped_and_permuted_tensor= reshaped_and_permuted_tensor.reshape(bs,16*20,500)

        x=torch.unsqueeze(reshaped_and_permuted_tensor,dim=1)

        x=torch.cat([x,x,x],dim=1)
        bs=x.size(0)


        x = self.extract_features(x)


        x = self.pool(x)
        x = x.view(bs,-1)

        return x

class Modelspec(nn.Module):
    def __init__(self, num_classes=1):
        super().__init__()

        model_name = "x3d_l"
        self.net = create_x3d(input_clip_length=16,
        input_crop_size=312,
        depth_factor=5.0,)
        
        # self.net.blocks[5]=nn.Identity()
        # self.net.avgpool = nn.Identity()
        self.net.blocks[5].dropout=nn.Identity()
        self.net.blocks[5].proj = nn.Identity()
        self.net.blocks[5].activation = nn.Identity()
        self.net.blocks[5].output_pool = nn.Identity()
        
        self.avg = nn.AdaptiveAvgPool2d(1)



    def forward(self, x):
        x = torch.unsqueeze(x, dim=1)
        x = torch.cat([x, x, x], dim=1)
        x = self.net(x)
        # do preprocess
        bs = x.size(0)

        x = x.view(bs, -1)

        return x


class Netdoublehead(nn.Module):
    def __init__(self, num_classes=1):
        super().__init__()

        
        self.model_wave = Modeleeg()

        self.model_spec = Modelspec()

        self.pool = nn.AdaptiveAvgPool3d(1)
        self.fc = nn.Linear(2048, 6, bias=True)

        self.droup = nn.Dropout(0.5)




    def forward(self,  eeg, spec):
        # do preprocess
        bs = eeg.size(0)

        x = self.model_wave(eeg)
        y = self.model_spec(spec)
        x = (x + y) / 2

        

        x = self.droup(x)
        x = self.fc(x)
        x =torch.softmax(x,-1)
        
        return x



# %%
def inference_function(test_loader, model, device,double_input=False):
    model.eval()
    
    prediction_dict = {}
    preds = []
    with tqdm(test_loader, unit="test_batch", desc='Inference') as tqdm_test_loader:
        for step, X in enumerate(tqdm_test_loader):
            
            if double_input:
                wave,spec=X
                
                wave = wave.to(device)
                spec = spec.to(device)
                
                
                batch_size = wave.size(0)
                with torch.no_grad():
                    y_preds = model(wave,spec)
                    
            else:
                X = X.to(device)

                batch_size = X.size(0)
                with torch.no_grad():
                    y_preds = model(X)

            preds.append(y_preds.to('cpu').numpy()) 
                
    prediction_dict["predictions"] = np.concatenate(preds) 
    return prediction_dict

# %%
test_df=pd.read_csv(CFG['data'])

test_df.head(5)


# %%
def run_weight_spec():
    print('infer with weights_spec')
    predictions=[]
    for model_weight in CFG['weights_spec']:

        test_dataset = AlaskaDataIter(test_df, training_flag=False, shuffle=False,use_spec=True)
        test_loader = DataLoader(test_dataset,
                         CFG['batch_size'],
                         num_workers=CFG['num_worker'],
                         shuffle=False)

        model = NetSpec()
        state_dict = torch.load(model_weight, map_location=device)

        model.load_state_dict(state_dict,strict=False)
        model.to(device)
        prediction_dict = inference_function(test_loader, model, device)
        predictions.append(prediction_dict["predictions"])

        test_dataset = AlaskaDataIter(test_df, training_flag=False, shuffle=False,use_spec=True,flip=True)
        test_loader = DataLoader(test_dataset,
                         CFG['batch_size'],
                         num_workers=CFG['num_worker'],
                         shuffle=False)

        model = NetSpec()
        state_dict = torch.load(model_weight, map_location=device)

        model.load_state_dict(state_dict,strict=False)
        model.to(device)
        prediction_dict = inference_function(test_loader, model, device)
        predictions.append(prediction_dict["predictions"])

        torch.cuda.empty_cache()
        gc.collect()
    predictions = np.array(predictions)
    predictions = np.mean(predictions, axis=0)
    
    return predictions

# %%
def run_weight_mix():
    predictions=[]
    print('infer with weights_mix')
    for model_weight in CFG['weights_mix']:
        test_dataset = AlaskaDataIter(test_df, training_flag=False, shuffle=False,use_mix=True)
        test_loader = DataLoader(test_dataset,
                         CFG['batch_size'],
                         num_workers=CFG['num_worker'],
                         shuffle=False)

        model = NetMix()
        state_dict = torch.load(model_weight, map_location=device)

        model.load_state_dict(state_dict,strict=False)
        model.to(device)
        prediction_dict = inference_function(test_loader, model, device)
        predictions.append(prediction_dict["predictions"])
        torch.cuda.empty_cache()
        gc.collect()
        
    predictions = np.array(predictions)
    predictions = np.mean(predictions, axis=0)
    
    return predictions

# %%
def run_weight_one_image():
    print('infer with weights_one_image')
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    predictions=[]
    for model_weight in CFG['weights_one_image']:
        test_dataset = AlaskaDataIter(test_df, training_flag=False, shuffle=False,use_eeg=True,ll=0,rr=20)
        test_loader = DataLoader(test_dataset,
                         CFG['batch_size'],
                         num_workers=CFG['num_worker'],
                         shuffle=False)

        model = NetOneImage()
        state_dict = torch.load(model_weight, map_location=device)

        model.load_state_dict(state_dict,strict=True)
        model.to(device)
        prediction_dict = inference_function(test_loader, model, device)
        predictions.append(prediction_dict["predictions"])
        
        test_dataset = AlaskaDataIter(test_df, training_flag=False, shuffle=False,use_eeg=True,flip=True,ll=0,rr=20)
        test_loader = DataLoader(test_dataset,
                         CFG['batch_size'],
                         num_workers=CFG['num_worker'],
                         shuffle=False)

        model = NetOneImage()
        state_dict = torch.load(model_weight, map_location=device)

        model.load_state_dict(state_dict,strict=True)
        model.to(device)
        prediction_dict = inference_function(test_loader, model, device)
        predictions.append(prediction_dict["predictions"])

        torch.cuda.empty_cache()
        gc.collect()
        
        
    predictions = np.array(predictions)
    predictions = np.mean(predictions, axis=0)
    
    return predictions

# %%
def run_weight_3d():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    print('infer with weights_3d')
    predictions=[]
    for model_weight in CFG['weights_3d']:
        test_dataset = AlaskaDataIter(test_df, training_flag=False, shuffle=False,use_eeg=True)
        test_loader = DataLoader(test_dataset,
                         CFG['batch_size'],
                         num_workers=CFG['num_worker'],
                         shuffle=False)

        model = Net3d()
        state_dict = torch.load(model_weight, map_location=device)

        model.load_state_dict(state_dict,strict=False)
        model.to(device)
        prediction_dict = inference_function(test_loader, model, device)
        predictions.append(prediction_dict["predictions"])


        test_dataset = AlaskaDataIter(test_df, training_flag=False, shuffle=False,use_eeg=True,flip=True)
        test_loader = DataLoader(test_dataset,
                         CFG['batch_size'],
                         num_workers=CFG['num_worker'],
                         shuffle=False)

        model = Net3d()
        state_dict = torch.load(model_weight, map_location=device)

        model.load_state_dict(state_dict,strict=False)
        model.to(device)
        prediction_dict = inference_function(test_loader, model, device)
        predictions.append(prediction_dict["predictions"])

        torch.cuda.empty_cache()
        gc.collect()
    predictions = np.array(predictions)
    predictions = np.mean(predictions, axis=0)
    
    return predictions

# %%
def run_eeg_family(model_class, weight_key, batch_size):
    """Average checkpoint probabilities and the original left/right EEG TTA.

    Mirroring the four bipolar chains after the linear filter is equivalent
    to swapping electrode hemispheres before montage construction/filtering.
    Thus each parquet file needs reading/filtering only once per checkpoint.
    X3D retains its existing internal spectrogram time-reversal TTA.
    """
    dataset = AlaskaDataIter(test_df, training_flag=False, shuffle=False,
                             use_eeg=True, ll=0, rr=20)
    loader = DataLoader(dataset, batch_size=batch_size,
                        num_workers=CFG['num_worker'], shuffle=False,
                        pin_memory=(device.type == 'cuda'))
    # Montage order in brain_lead is LL, RL, LP, RP (four leads each).
    mirror = [4, 5, 6, 7, 0, 1, 2, 3, 12, 13, 14, 15, 8, 9, 10, 11]
    total = np.zeros((len(test_df), 6), dtype=np.float64)
    os.makedirs('prediction_cache', exist_ok=True)
    for checkpoint_index, model_weight in enumerate(CFG[weight_key]):
        print(f'Infer {weight_key}: {model_weight}')
        model = model_class()
        # CPU loading avoids keeping a second copy of weights on the GPU.
        state_dict = torch.load(model_weight, map_location='cpu')
        model.load_state_dict(state_dict, strict=True)
        del state_dict
        model.to(device).eval()
        checkpoint_preds = []
        with torch.inference_mode():
            for wave in tqdm(loader, desc=weight_key, unit='batch'):
                wave = wave.to(device, non_blocking=True)
                normal = model(wave)
                mirrored = model(wave[:, mirror, :].contiguous())
                pred = (normal + mirrored) * 0.5
                checkpoint_preds.append(pred.float().cpu().numpy())
        checkpoint_preds = np.concatenate(checkpoint_preds, axis=0)
        if not np.isfinite(checkpoint_preds).all():
            raise ValueError(f'Non-finite predictions from {model_weight}')
        np.save(f'prediction_cache/{weight_key}_{checkpoint_index}.npy',
                checkpoint_preds)
        total += checkpoint_preds
        del model, wave, normal, mirrored, pred, checkpoint_preds
        gc.collect()
        if device.type == 'cuda':
            torch.cuda.empty_cache()
    return total / len(CFG[weight_key])


def run_weight_eeg_raw():
    return run_eeg_family(Net1d, 'weights_eeg_raw', CFG['batch_size'])


# %%
def run_weight_x3d():
    # Internal time-flip TTA doubles the effective X3D batch size.
    return run_eeg_family(Netx3d, 'weights_x3d', max(1, CFG['batch_size'] // 2))


# %%
def run_weight_double_head():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    print('infer with weights_doublehead')
    predictions=[]
    for model_weight in CFG['weights_doublehead']:
        
        test_dataset = AlaskaDataIter(test_df, training_flag=False, shuffle=False,use_mix=True,ll=0,rr=20)
        test_loader = DataLoader(test_dataset,
                         CFG['batch_size']//2,
                         num_workers=CFG['num_worker'],
                         shuffle=False)

        model = Netdoublehead()
        state_dict = torch.load(model_weight, map_location=device)

        model.load_state_dict(state_dict,strict=True)
        model.to(device)
        prediction_dict = inference_function(test_loader, model, device,double_input=True)
        predictions.append(prediction_dict["predictions"])


        test_dataset = AlaskaDataIter(test_df, training_flag=False, shuffle=False,use_mix=True,flip=True,ll=0,rr=20)
        test_loader = DataLoader(test_dataset,
                         CFG['batch_size']//2,
                         num_workers=CFG['num_worker'],
                         shuffle=False)

        model = Netdoublehead()
        state_dict = torch.load(model_weight, map_location=device)

        model.load_state_dict(state_dict,strict=True)
        model.to(device)
        prediction_dict = inference_function(test_loader, model, device,double_input=True)
        predictions.append(prediction_dict["predictions"])

        torch.cuda.empty_cache()
        gc.collect()
    predictions = np.array(predictions)
    predictions = np.mean(predictions, axis=0)
    
    return predictions

# %%


# %%
# The latest double-head rewrite regressed sharply in the supplied history.
# Restore complementary X3D spectrogram and raw-EEG probability ensembles.
# Equal FAMILY weights avoid overweighting a family with more checkpoints.
# Keep the current checkpoint-compatible architectures and 0--20 Hz filter.
x3d_predictions = run_weight_x3d()
raw_predictions = run_weight_eeg_raw()
predictions = 0.5 * x3d_predictions + 0.5 * raw_predictions
np.save('prediction_cache/x3d_family.npy', x3d_predictions)
np.save('prediction_cache/raw_family.npy', raw_predictions)
np.save('prediction_cache/eeg_ids.npy', test_df.eeg_id.to_numpy())

# KL consumes distributions, so enforce finite, strictly positive row sums.
if predictions.shape != (len(test_df), 6):
    raise ValueError(f'Unexpected prediction shape: {predictions.shape}')
if not np.isfinite(predictions).all():
    raise ValueError('Non-finite ensemble predictions')
predictions = np.clip(predictions, 1e-15, 1.0)
predictions /= predictions.sum(axis=1, keepdims=True)

# %%
TARGETS = ['seizure_vote', 'lpd_vote', 'gpd_vote', 'lrda_vote', 'grda_vote', 'other_vote']
sub = pd.DataFrame({'eeg_id': test_df.eeg_id.values})
sub[TARGETS] = predictions
sub.to_csv('submission.csv',index=False)
print(f'Submissionn shape: {sub.shape}')
sub.head()

# %%


# %%


# %%


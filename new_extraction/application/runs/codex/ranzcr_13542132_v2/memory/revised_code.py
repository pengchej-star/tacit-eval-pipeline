# %% [markdown]
# # RANZCR: Xception TPU Prediction
# ![](https://storage.googleapis.com/kaggle-competitions/kaggle/23870/logos/header.png?t=2020-12-01-04-28-05)
# 
# Serious complications can occur as a result of malpositioned lines and tubes in patients. Doctors and nurses frequently use checklists for placement of lifesaving equipment to ensure they follow protocol in managing patients. Yet, these steps can be time consuming and are still prone to human error, especially in stressful situations when hospitals are at capacity.
# 
# Hospital patients can have catheters and lines inserted during the course of their admission and serious complications can arise if they are positioned incorrectly. Nasogastric tube malpositioning into the airways has been reported in up to 3% of cases, with up to 40% of these cases demonstrating complications [1-3]. Airway tube malposition in adult patients intubated outside the operating room is seen in up to 25% of cases [4,5]. The likelihood of complication is directly related to both the experience level and specialty of the proceduralist. Early recognition of malpositioned tubes is the key to preventing risky complications (even death), even more so now that millions of COVID-19 patients are in need of these tubes and lines.
# 
# The gold standard for the confirmation of line and tube positions are chest radiographs. However, a physician or radiologist must manually check these chest x-rays to verify that the lines and tubes are in the optimal position. Not only does this leave room for human error, but delays are also common as radiologists can be busy reporting other scans. Deep learning algorithms may be able to automatically detect malpositioned catheters and lines. Once alerted, clinicians can reposition or remove them to avoid life-threatening complications.
# 
# ## The first part of this notebook: [RANZCR: Xception TPU](https://www.kaggle.com/maksymshkliarevskyi/ranzcr-xception-tpu)

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import models, layers
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.applications import Xception
from tensorflow.keras.optimizers import Adam

# ignoring warnings
import warnings
warnings.simplefilter("ignore")

import os, cv2

# %%
# TPU or GPU detection
# Detect hardware, return appropriate distribution strategy
# try:
#     tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
#     print(f'Running on TPU {tpu.master()}')
# except ValueError:
#     tpu = None

# if tpu:
#     tf.config.experimental_connect_to_cluster(tpu)
#     tf.tpu.experimental.initialize_tpu_system(tpu)
#     strategy = tf.distribute.experimental.TPUStrategy(tpu)
# else:
#     strategy = tf.distribute.get_strategy()

# AUTO = tf.data.experimental.AUTOTUNE
# REPLICAS = strategy.num_replicas_in_sync
# print(f'REPLICAS: {REPLICAS}')

# %% [markdown]
# ## Work directory

# %%
RUN_DIAGNOSTICS = False
WORK_DIR = '../input/ranzcr-clip-catheter-line-classification'
os.listdir(WORK_DIR)

# %% [markdown]
# # Fast look at the data

# %%
print('Train images: %d' %len(os.listdir(os.path.join(WORK_DIR, "train"))))

# %%
# Data
train = pd.read_csv(os.path.join(WORK_DIR, "train.csv"))
train_images = WORK_DIR + "/train/" + train['StudyInstanceUID'] + '.jpg'

ss = pd.read_csv(os.path.join(WORK_DIR, 'sample_submission.csv'))
test_images = WORK_DIR + "/test/" + ss['StudyInstanceUID'] + '.jpg'

label_cols = ss.columns[1:]
labels = train[label_cols].values

train_annot = pd.read_csv(os.path.join(WORK_DIR, "train_annotations.csv"))

print('Labels:\n', '*'*20, '\n', label_cols.values)
print('*'*50)
train.head()

# %%
if RUN_DIAGNOSTICS:
    sns.set_style("whitegrid")
    fig = plt.figure(figsize = (15, 12), dpi = 300)
    plt.suptitle('Labels count', fontfamily = 'serif', size = 15)

    for ind, i in enumerate(label_cols):
        fig.add_subplot(4, 3, ind + 1)

        sns.countplot(train[i], edgecolor = 'black',
                      palette = reversed(sns.color_palette('viridis', 2)))

        plt.xlabel('')
        plt.ylabel('')
        plt.xticks(fontfamily = 'serif', size = 10)
        plt.yticks(fontfamily = 'serif', size = 10)
        plt.title(i, fontfamily = 'serif', size = 10)
    plt.show()

# %%
if RUN_DIAGNOSTICS:
    sample = train.sample(9)
    plt.figure(figsize=(10, 7), dpi = 300)
    for ind, image_id in enumerate(sample.StudyInstanceUID):
        plt.subplot(3, 3, ind + 1)
        image = image_id + '.jpg'
        img = cv2.imread(os.path.join(WORK_DIR, "train", image))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img)
        plt.title('Shape: {}'.format(img.shape[:2]))
        plt.axis("off")
    plt.show()

# %% [markdown]
# # Preparation for prediction

# %%
# Main parameters
BATCH_SIZE = 8 * 1
STEPS_PER_EPOCH = len(train)*0.8 / BATCH_SIZE
VALIDATION_STEPS = len(train)*0.2 / BATCH_SIZE
EPOCHS = 30
TARGET_SIZE = 750

# %%
# https://www.kaggle.com/xhlulu/ranzcr-efficientnet-b3-gpu-starter

def build_decoder(with_labels = True,
                  target_size = (TARGET_SIZE, TARGET_SIZE), 
                  ext = 'jpg'):
    def decode(path):
        file_bytes = tf.io.read_file(path)
        if ext == 'png':
            img = tf.image.decode_png(file_bytes, channels = 3)
        elif ext in ['jpg', 'jpeg']:
            img = tf.image.decode_jpeg(file_bytes, channels = 3)
        else:
            raise ValueError("Image extension not supported")

        img = tf.cast(img, tf.float32) / 255.0
        img = tf.image.resize(img, target_size)

        return img
    
    def decode_with_labels(path, label):
        return decode(path), label
    
    return decode_with_labels if with_labels else decode


def build_augmenter(with_labels = True):
    def augment(img):
        img = tf.image.random_flip_left_right(img)
        img = tf.image.random_flip_up_down(img)
        return img
    
    def augment_with_labels(img, label):
        return augment(img), label
    
    return augment_with_labels if with_labels else augment


def build_dataset(paths, labels = None, bsize = 32, cache = True,
                  decode_fn = None, augment_fn = None,
                  augment = True, repeat = True, shuffle = 1024, 
                  cache_dir = ""):
    if cache_dir != "" and cache is True:
        os.makedirs(cache_dir, exist_ok=True)
    
    if decode_fn is None:
        decode_fn = build_decoder(labels is not None)
    
    if augment_fn is None:
        augment_fn = build_augmenter(labels is not None)
    
    AUTO = tf.data.experimental.AUTOTUNE
    slices = paths if labels is None else (paths, labels)
    
    dset = tf.data.Dataset.from_tensor_slices(slices)
    options = tf.data.Options()
    options.experimental_deterministic = True
    dset = dset.with_options(options)
    dset = dset.map(decode_fn, num_parallel_calls = 2)
    dset = dset.cache(cache_dir) if cache else dset
    dset = dset.map(augment_fn, num_parallel_calls = AUTO) if augment else dset
    dset = dset.repeat() if repeat else dset
    dset = dset.shuffle(shuffle) if shuffle else dset
    dset = dset.batch(bsize).prefetch(1)
    
    return dset

# %%
# Train test split
# (train_img, valid_img, 
#  train_labels, valid_labels) = train_test_split(train_images, labels, 
#                                                 train_size = 0.8, 
#                                                 random_state = 0)

# %%
# Tensorflow datasets
# train_df = build_dataset(
#     train_img, train_labels, bsize = BATCH_SIZE, 
#     cache = True)

# valid_df = build_dataset(
#     valid_img, valid_labels, bsize = BATCH_SIZE, 
#     repeat = False, shuffle = False, augment = False, 
#     cache = True)

test_df = build_dataset(
    test_images, bsize = BATCH_SIZE, repeat = False, 
    shuffle = False, augment = False, cache = False)

test_df

# %%
# def create_model():
#     conv_base = Xception(include_top = False, weights = 'imagenet',
#                          input_shape = (TARGET_SIZE, TARGET_SIZE, 3))
#     model = conv_base.output
#     model = layers.GlobalAveragePooling2D()(model)
#     model = layers.Dense(11, activation = "sigmoid")(model)
#     model = models.Model(conv_base.input, model)

#     model.compile(optimizer = Adam(lr = 0.001),
#                   loss = "binary_crossentropy",
#                   metrics = ["AUC"])
#     return model

# %%
model = models.load_model(
    '../input/ranzcr-xception-tpu-baseline/Xception_750_TPU.h5',
    compile=False,
)
model.summary()

# %%
print('Our Xception CNN has %d layers' %len(model.layers))

# %% [markdown]
# # Visualization of CNN intermediate activations

# %%
def activation_layer_vis(img, activation_layer = 0, layers = 10):
    layer_outputs = [layer.output for layer in model.layers[:layers]]
    activation_model = models.Model(inputs = model.input, outputs = layer_outputs)
    activations = activation_model.predict(img)
    
    rows = int(activations[activation_layer].shape[3] / 3)
    cols = int(activations[activation_layer].shape[3] / rows)
    fig, axes = plt.subplots(rows, cols, figsize = (15, 15 * cols))
    axes = axes.flatten()
    
    for i, ax in zip(range(activations[activation_layer].shape[3]), axes):
        ax.matshow(activations[activation_layer][0, :, :, i], cmap = 'viridis')
        ax.axis('off')
    plt.tight_layout()
    plt.show()

def all_activations_vis(img, layers = 10):
    layer_outputs = [layer.output for layer in model.layers[:layers]]
    activation_model = models.Model(inputs = model.input, outputs = layer_outputs)
    activations = activation_model.predict(img)
    
    layer_names = []
    for layer in model.layers[:layers]: 
        layer_names.append(layer.name) 

    images_per_row = 3
    for layer_name, layer_activation in zip(layer_names, activations): 
        n_features = layer_activation.shape[-1] 

        size = layer_activation.shape[1] 

        n_cols = n_features // images_per_row 
        display_grid = np.zeros((size * n_cols, images_per_row * size)) 

        for col in range(n_cols): 
            for row in range(images_per_row): 
                channel_image = layer_activation[0, :, :, col * images_per_row + row] 
                channel_image -= channel_image.mean() 
                channel_image /= channel_image.std() 
                channel_image *= 64 
                channel_image += 128 
                channel_image = np.clip(channel_image, 0, 255).astype('uint8') 
                display_grid[col * size : (col + 1) * size, 
                             row * size : (row + 1) * size] = channel_image 
        scale = 1. / size 
        plt.figure(figsize=(scale * 5 * display_grid.shape[1], 
                            scale * 5 * display_grid.shape[0])) 
        plt.title(layer_name) 
        plt.grid(False)
        plt.axis('off')
        plt.imshow(display_grid, aspect = 'auto', cmap = 'viridis')

# %% [markdown]
# ### Visualization of the first 3 layers

# %%
img_tensor = build_dataset(
    pd.Series(test_images[0]), bsize = 1,repeat = False, 
    shuffle = False, augment = False, cache = False)

# %%
if RUN_DIAGNOSTICS:
    all_activations_vis(img_tensor, 3)

# %% [markdown]
# # Prediction

# %%
# Two deterministic views retain the full field of view and the checkpoint's
# existing 750-pixel, [0, 1] preprocessing. The provided augmenter already
# includes horizontal reflection. Avoid crops that could remove line tips.
# Run the views separately to retain the baseline's peak inference batch size.
@tf.function(input_signature=[
    tf.TensorSpec([None, TARGET_SIZE, TARGET_SIZE, 3], tf.float32)
])
def predict_view(images):
    return tf.cast(model(images, training=False), tf.float32)


def predict_with_tta(dataset, n_images):
    original = np.empty((n_images, len(label_cols)), dtype=np.float32)
    reflected = np.empty_like(original)
    offset = 0
    for batch_index, images in enumerate(dataset):
        batch_size = int(tf.shape(images)[0].numpy())
        end = offset + batch_size
        if end > n_images:
            raise ValueError("Prediction dataset has more rows than submission")
        original[offset:end] = predict_view(images).numpy()
        reflected[offset:end] = predict_view(
            tf.image.flip_left_right(images)
        ).numpy()
        offset = end
        if batch_index % 100 == 0 or offset == n_images:
            print(f"Predicted {offset}/{n_images} images (two views)")
    if offset != n_images:
        raise ValueError("Prediction dataset has missing rows")
    for values in (original, reflected):
        if not np.isfinite(values).all():
            raise ValueError("Non-finite model predictions")
        if np.any(values < 0.0) or np.any(values > 1.0):
            raise ValueError("Expected sigmoid probabilities from checkpoint")
    return original, reflected


assert len(label_cols) == 11
assert ss['StudyInstanceUID'].is_unique
base_predictions, flip_predictions = predict_with_tta(test_df, len(ss))
# Average probabilities, preserving continuous scores for macro ROC AUC.
# No class-specific tuning is justified without held-out checkpoint predictions.
predictions = 0.5 * base_predictions + 0.5 * flip_predictions
assert predictions.shape == (len(ss), 11)
# Small prediction artifacts allow an exact no-TTA comparison after evaluation.
np.savez_compressed(
    'tta_predictions.npz',
    study_ids=ss['StudyInstanceUID'].to_numpy(dtype=str),
    label_columns=np.asarray(label_cols, dtype=str),
    original=base_predictions,
    horizontal_flip=flip_predictions,
)
ss[label_cols] = predictions
ss.to_csv('submission.csv', index=False)

# %%
ss.head()

# %% [markdown]
# # WORK IN PROGRESS...

# %% [markdown]
# ## The first part of this notebook: [RANZCR: Xception TPU](https://www.kaggle.com/maksymshkliarevskyi/ranzcr-xception-tpu)

# %%


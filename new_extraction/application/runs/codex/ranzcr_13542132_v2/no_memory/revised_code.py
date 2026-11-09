# %% [markdown]
# # RANZCR: Xception TPU Prediction
# Deterministic horizontal-flip test-time augmentation of the supplied checkpoint.

# %%
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import models

# %% [markdown]
# ## Work directory

# %%
WORK_DIR = '../input/ranzcr-clip-catheter-line-classification'
MODEL_PATH = '../input/ranzcr-xception-tpu-baseline/Xception_750_TPU.h5'

# %% [markdown]
# # Submission data

# %%
ss = pd.read_csv(os.path.join(WORK_DIR, 'sample_submission.csv'))
label_cols = list(ss.columns[1:])
test_images = (
    WORK_DIR + '/test/' + ss['StudyInstanceUID'].astype(str) + '.jpg'
).to_numpy(dtype=str)
assert len(label_cols) == 11, 'Expected the eleven competition labels.'
assert ss['StudyInstanceUID'].is_unique, 'Duplicate submission IDs.'
print('Test images:', len(test_images))
print('Labels:', label_cols)

# %% [markdown]
# # Preparation for prediction

# %%
BATCH_SIZE = 8
TARGET_SIZE = 750
AUTO = tf.data.experimental.AUTOTUNE
# Average probabilities from two complete-image views. No crop removes line tips.
ORIGINAL_WEIGHT = 0.5
FLIPPED_WEIGHT = 0.5

# %%
def build_decoder(with_labels=True,
                  target_size=(TARGET_SIZE, TARGET_SIZE), ext='jpg'):
    def decode(path):
        file_bytes = tf.io.read_file(path)
        if ext == 'png':
            img = tf.image.decode_png(file_bytes, channels=3)
        elif ext in ['jpg', 'jpeg']:
            img = tf.image.decode_jpeg(file_bytes, channels=3)
        else:
            raise ValueError('Image extension not supported')
        # Preserve the supplied checkpoint's existing input convention exactly.
        # Do not substitute the generic Xception [-1, 1] preprocessing here.
        img = tf.cast(img, tf.float32) / 255.0
        img = tf.image.resize(img, target_size, method='bilinear')
        return img

    def decode_with_labels(path, label):
        return decode(path), label

    return decode_with_labels if with_labels else decode


def build_dataset(paths, labels=None, bsize=BATCH_SIZE):
    slices = paths if labels is None else (paths, labels)
    dset = tf.data.Dataset.from_tensor_slices(slices)
    options = tf.data.Options()
    options.experimental_deterministic = True
    dset = dset.with_options(options)
    dset = dset.map(build_decoder(labels is not None), num_parallel_calls=AUTO)
    # Retain the last partial batch and the sample_submission row ordering.
    # Only prefetch one batch: the hidden test set is much larger than public test.
    return dset.batch(bsize, drop_remainder=False).prefetch(1)


# %%
test_df = build_dataset(test_images)

# %%
# Inference does not need saved optimizer state or training metric deserialization.
model = models.load_model(MODEL_PATH, compile=False)
assert len(model.input_shape) == 4, 'Expected a single image input.'
assert model.input_shape[-1] == 3
assert model.input_shape[1] in (None, TARGET_SIZE)
assert model.input_shape[2] in (None, TARGET_SIZE)
assert model.output_shape[-1] == len(label_cols)
print('Loaded Xception with %d layers' % len(model.layers))

# %% [markdown]
# # Prediction
# Horizontal reflection keeps all image content while averaging orientation-sensitive
# errors. Vertical reflection changes superior/inferior anatomy and is not used.
# Both views use inference-mode batch normalization and dropout.

# %%
@tf.function(input_signature=[
    tf.TensorSpec(shape=[None, TARGET_SIZE, TARGET_SIZE, 3], dtype=tf.float32)
])
def predict_batch(images):
    return model(images, training=False)


predictions = np.empty((len(ss), len(label_cols)), dtype=np.float32)
row = 0
num_batches = (len(ss) + BATCH_SIZE - 1) // BATCH_SIZE
for batch_index, images in enumerate(test_df):
    # Run the views sequentially to keep the checkpoint's original batch size.
    # Decode each image only once; never cache all 750px images in memory.
    original = np.asarray(predict_batch(images).numpy(), dtype=np.float32)
    reflected = np.asarray(
        predict_batch(tf.image.flip_left_right(images)).numpy(), dtype=np.float32
    )
    batch_predictions = ORIGINAL_WEIGHT * original + FLIPPED_WEIGHT * reflected
    batch_len = len(batch_predictions)
    assert batch_predictions.shape == (batch_len, len(label_cols))
    assert np.isfinite(batch_predictions).all(), 'Non-finite model predictions.'
    assert (batch_predictions >= 0).all() and (batch_predictions <= 1).all(), (
        'The saved checkpoint must output sigmoid probabilities.'
    )
    predictions[row:row + batch_len] = batch_predictions
    row += batch_len
    if (batch_index + 1) % 100 == 0 or batch_index + 1 == num_batches:
        print('Predicted batch %d/%d (%d images)' % (
            batch_index + 1, num_batches, row))

assert row == len(ss), 'Predictions do not cover all submission rows.'
ss.loc[:, label_cols] = predictions
ss.to_csv('submission.csv', index=False)
print('Saved submission.csv:', ss.shape)

# %%
ss.head()

# %% [markdown]
# # RANZCR: Xception TPU Prediction with deterministic test-time augmentation
# Reuse the supplied trained checkpoint. Average predictions across mirrored
# views and a lightly reduced full-image view to reduce sensitivity to framing.

# %%
import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import models

# %% [markdown]
# ## Work directory

# %%
WORK_DIR = '../input/ranzcr-clip-catheter-line-classification'
MODEL_PATH = '../input/ranzcr-xception-tpu-baseline/Xception_750_TPU.h5'
PREDICTION_DIR = 'prediction_cache'
os.makedirs(PREDICTION_DIR, exist_ok=True)

# %% [markdown]
# ## Data and submission order

# %%
ss = pd.read_csv(os.path.join(WORK_DIR, 'sample_submission.csv'))
label_cols = ss.columns[1:].tolist()
assert len(label_cols) == 11, 'Expected the 11 competition targets.'
assert ss['StudyInstanceUID'].is_unique, 'Submission IDs must be unique.'
test_images = (
    WORK_DIR + '/test/' + ss['StudyInstanceUID'].astype(str) + '.jpg'
).to_numpy()
# Never derive the prediction order from directory listings.
ss[['StudyInstanceUID']].to_csv(
    os.path.join(PREDICTION_DIR, 'prediction_ids.csv'), index=False
)

# %% [markdown]
# ## Preparation for prediction

# %%
BATCH_SIZE = 8
TARGET_SIZE = 750
# Most of the weight stays on the original image scale. The smaller view
# retains the entire radiograph; cropping can remove clinically relevant tips.
TTA_VIEWS = [
    ('original', False, 1.00, 0.40),
    ('horizontal_flip', True, 1.00, 0.40),
    ('full_image_small', False, 0.96, 0.10),
    ('full_image_small_flip', True, 0.96, 0.10),
]
assert np.isclose(sum(v[3] for v in TTA_VIEWS), 1.0)

# %%
def build_decoder(target_size=(TARGET_SIZE, TARGET_SIZE)):
    def decode(path):
        img = tf.image.decode_jpeg(tf.io.read_file(path), channels=3)
        # Keep precisely the checkpoint's existing [0, 1] preprocessing.
        # Do not substitute ImageNet Xception preprocess_input here.
        img = tf.cast(img, tf.float32) / 255.0
        img = tf.image.resize(img, target_size)
        img = tf.ensure_shape(img, [target_size[0], target_size[1], 3])
        return img
    return decode


def build_dataset(paths, bsize=BATCH_SIZE):
    options = tf.data.Options()
    options.experimental_deterministic = True
    dset = tf.data.Dataset.from_tensor_slices(paths)
    dset = dset.with_options(options)
    # Bound buffering: the hidden test set is too large for an in-memory cache.
    dset = dset.map(build_decoder(), num_parallel_calls=2)
    return dset.batch(bsize, drop_remainder=False).prefetch(2)


def transform_batch(images, flip=False, scale=1.0):
    if scale != 1.0:
        side = int(round(TARGET_SIZE * scale))
        images = tf.image.resize(images, [side, side])
        before = (TARGET_SIZE - side) // 2
        after = TARGET_SIZE - side - before
        # Reflect padding avoids introducing a strong artificial black border.
        images = tf.pad(
            images, [[0, 0], [before, after], [before, after], [0, 0]],
            mode='REFLECT',
        )
    if flip:
        images = tf.image.flip_left_right(images)
    return images

# %%
test_df = build_dataset(test_images)

# %% [markdown]
# ## Load the existing Xception checkpoint

# %%
# Training optimizer/metric deserialization is unnecessary for inference.
model = models.load_model(MODEL_PATH, compile=False)
assert model.output_shape[-1] == len(label_cols)
for dimension in model.input_shape[1:3]:
    assert dimension in (None, TARGET_SIZE), model.input_shape
model.summary()

# %% [markdown]
# ## Prediction ensemble
# No validation scores are estimated on the checkpoint's training data:
# its original training/validation patient split is not supplied. TTA weights
# are fixed in advance, rather than fitted to potentially leaked predictions.

# %%
n_test = len(ss)
assert n_test > 0
view_predictions = {
    name: np.empty((n_test, len(label_cols)), dtype=np.float32)
    for name, _, _, _ in TTA_VIEWS
}

# Decode each image once; evaluate one transformed batch at a time. This keeps
# accelerator memory close to the baseline instead of concatenating TTA views.
@tf.function
def predict_batch(images):
    return model(images, training=False)

position = 0
for batch_number, images in enumerate(test_df):
    batch_size = int(tf.shape(images)[0].numpy())
    end = position + batch_size
    for name, flip, scale, _ in TTA_VIEWS:
        batch_prediction = predict_batch(
            transform_batch(images, flip=flip, scale=scale)
        ).numpy()
        if batch_prediction.shape != (batch_size, len(label_cols)):
            raise ValueError('Unexpected prediction shape: %s' % (batch_prediction.shape,))
        if not np.isfinite(batch_prediction).all():
            raise ValueError('Non-finite predictions in view ' + name)
        view_predictions[name][position:end] = batch_prediction
    position = end
    if batch_number % 100 == 0 or position == n_test:
        print('Predicted %d / %d radiographs' % (position, n_test))
assert position == n_test

# Cache each member, including the exact unaugmented baseline, for inspection
# and future blending without repeating expensive image inference.
predictions = np.zeros((n_test, len(label_cols)), dtype=np.float64)
for name, _, _, weight in TTA_VIEWS:
    member = view_predictions[name]
    np.save(os.path.join(PREDICTION_DIR, name + '.npy'), member)
    predictions += weight * member

with open(os.path.join(PREDICTION_DIR, 'metadata.json'), 'w') as f:
    json.dump({
        'model_path': MODEL_PATH,
        'label_columns': label_cols,
        'target_size': TARGET_SIZE,
        'views': [
            {'name': name, 'horizontal_flip': flip, 'scale': scale, 'weight': weight}
            for name, flip, scale, weight in TTA_VIEWS
        ],
    }, f, indent=2)

# %% [markdown]
# ## Submission

# %%
assert predictions.shape == (len(ss), 11)
assert np.isfinite(predictions).all()
assert ((predictions >= 0.0) & (predictions <= 1.0)).all(), 'Expected sigmoid probabilities.'
ss.loc[:, label_cols] = predictions
ss.to_csv('submission.csv', index=False)
print('Saved submission.csv:', ss.shape)
print(ss.head())

# Reuse encoders with unknown-category handling  `T.2.2.4`   2 edits, 0 experts
1 scored cases, median improvement +0.00603, 1 improved


- expert 7823861 (nan) · google · v8→v10   Fit the encoder on training data only. At test time, call transform (not fit_transform) on the test data. Ensure the output array has exactly as many rows as the test set. Set the encoder to handle unknown categories gracefully (e.g., ignore or map to a default) so unseen test categories do not caus
    evidence: ✓ Test categories include unseen levels or the inference code fits a new encoder. | ✓ The variable feeding a downstream stage references the wrong version of the data (e.g., raw vs. preprocessed, or vice versa). | ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✗ The prediction API call used at inference time does not match the model object's actual method signature or name. | ✓ A new feature branch receives implausible shapes or values.
    leaderboard score n/a → 0.41495
- expert 7823861 (nan) · google · v10→v15   Use two layers of defense: configure the encoder to ignore unknown categories (producing a zero-vector), and also remap unknown values to the most frequent or most representative training category before encoding. This avoids both crashes and degenerate feature vectors.
    evidence: ✓ Test categories include unseen levels or the inference code fits a new encoder. | ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✓ The variable feeding a downstream stage references the wrong version of the data (e.g., raw vs. preprocessed, or vice versa).
    leaderboard score 0.41495 → 0.42097 (+0.00603)
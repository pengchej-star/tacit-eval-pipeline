# Match image normalization to training  `T.3.1.12`   5 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.01220, 2 improved


- expert 15082684 · ranzcr · v16→v18   Audit every preprocessing step—resolution, cropping, normalization mean/std, interpolation mode—and ensure inference exactly mirrors training. Prioritize resolution and normalization statistics, as these are the most common sources of silent mismatch.
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail. | ✓ Image input statistics differ from the checkpoint’s training preprocessing.
    leaderboard score 0.95870 → 0.96509 (higher is better; improved by 0.00639)
- expert 15082684 · ranzcr · v17→v18   Compute the channel-wise mean and standard deviation on the training set and use those values for normalization at both training and inference. For single-channel images replicated to three channels, use the same statistic for all channels. Verify the statistics match between training and inference 
    evidence: ✗ The inference image size differs from training or may discard task-relevant detail. | ✓ Image input statistics differ from the checkpoint’s training preprocessing.
    leaderboard score n/a → 0.96509 (higher is better)
- expert 15173072 · ranzcr · v15→v21   Default to the canonical normalization statistics for the pretraining dataset (e.g., the dataset-wide mean/std the model was trained with). Deviating from these values almost always hurts because the model's learned features expect a specific input distribution. If the exact training stats are unkno
    evidence: ✓ Image input statistics differ from the checkpoint’s training preprocessing. | ✗ The inference image size differs from training or may discard task-relevant detail.
    leaderboard score n/a → 0.95243 (higher is better)
- expert 15173072 · ranzcr · v21→v28   Always use the exact normalization mean and standard deviation that the pretrained backbone was originally trained with. Do not guess or hand-tune these values; mismatched normalization silently degrades predictions even when the model otherwise loads correctly.
    evidence: ✓ Image input statistics differ from the checkpoint’s training preprocessing.
    leaderboard score 0.95243 → 0.96462 (higher is better; improved by 0.01220)
- expert 13521245 · ranzcr · v1→v2   Ensure the input preprocessing (especially image resolution and normalization) exactly matches what the checkpoint was trained with. A mismatch between the model's expected input size and the actual test-image size can depress the score far more than the choice of augmentation or caching strategy. V
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail. | ✓ Image input statistics differ from the checkpoint’s training preprocessing.
    leaderboard score n/a → 0.80492 (higher is better)
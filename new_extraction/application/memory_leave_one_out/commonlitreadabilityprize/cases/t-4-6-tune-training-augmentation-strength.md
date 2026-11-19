# Tune training augmentation strength  `T.4.6`   3 edits, 0 experts
2 scored cases, median improvement +0.00797, 2 improved


- expert 49576186 (Expert) · hms · v157→v163   Add random zeroing of contiguous time-frequency regions in the spectrogram (applied stochastically per sample during training only). Test across multiple runs. If the score does not improve after several attempts, the augmentation is not beneficial for this input representation and should be reverte
    evidence: ✓ The dataset is limited and label-preserving transformations represent variation expected at test time. | ✗ Repeated augmentation-strength changes have already failed to improve the fixed baseline. | ✓ Training improves while validation degrades as model complexity or feature count grows.
    leaderboard score 0.27394 → 0.27691 (+0.00298)
- expert 13542132 (Master) · ranzcr · v2→v3   Add a simple brightness or contrast perturbation as the first augmentation. Use a small fixed offset or random range. Evaluate on the leaderboard; brightness-type augmentations can yield surprisingly large gains on radiograph tasks because they help the model generalize across exposure variations.
    evidence: ✓ The dataset is limited and label-preserving transformations represent variation expected at test time. | ✗ Repeated augmentation-strength changes have already failed to improve the fixed baseline.
    leaderboard score 0.94363 → 0.95160 (+0.00797)
- expert 13542132 (Master) · ranzcr · v9→v13   Start with very mild augmentation (small brightness perturbation only). When adding geometric transforms (rotation) or stronger color jitter, keep magnitudes small (a few percent variation) and test each addition individually. If the score drops, revert immediately rather than trying to compensate w
    evidence: ✓ The dataset is limited and label-preserving transformations represent variation expected at test time. | ✓ Repeated augmentation-strength changes have already failed to improve the fixed baseline.
    leaderboard score n/a → 0.94397
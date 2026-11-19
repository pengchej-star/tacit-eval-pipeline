# Use mild image augmentation  `T.5.4.3.2`   2 edits, 0 experts
1 scored cases, median improvement +0.00797, 1 improved


- expert 13542132 (Master) · ranzcr · v2→v3   Add a simple brightness or contrast perturbation as the first augmentation. Use a small fixed offset or random range. Evaluate on the leaderboard; brightness-type augmentations can yield surprisingly large gains on radiograph tasks because they help the model generalize across exposure variations.
    evidence: ✓ Small visual intensity or geometric changes preserve the label. | ✗ The task relies on exact orientation or a small localized event. | ✗ Previous stronger augmentation experiments (rotation, color jitter, contrast, saturation) degraded or failed to improve scores compared to the mild baseline.
    leaderboard score 0.94363 → 0.95160 (+0.00797)
- expert 13542132 (Master) · ranzcr · v9→v13   Start with very mild augmentation (small brightness perturbation only). When adding geometric transforms (rotation) or stronger color jitter, keep magnitudes small (a few percent variation) and test each addition individually. If the score drops, revert immediately rather than trying to compensate w
    evidence: ✓ Small visual intensity or geometric changes preserve the label. | ✓ The task relies on exact orientation or a small localized event. | ✓ Previous stronger augmentation experiments (rotation, color jitter, contrast, saturation) degraded or failed to improve scores compared to the mild baseline.
    leaderboard score n/a → 0.94397
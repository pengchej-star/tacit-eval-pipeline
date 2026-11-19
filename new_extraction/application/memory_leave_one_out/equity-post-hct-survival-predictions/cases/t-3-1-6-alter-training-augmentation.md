# Alter training augmentation  `T.3.1.6`   5 edits, 0 experts
3 scored cases, median improvement +0.00797, 3 improved


- expert 17616127 (Contributor) · commonlitreadabilityprize · v49→v50   Swap in the alternative fold predictions and evaluate on the leaderboard. If the score degrades further, abandon that augmentation variant and return to the previously best-performing ensemble composition rather than continuing to explore weaker components.
    evidence: ✓ Training overfits and label-preserving perturbations are supported by the input semantics. | ✓ Previous augmentation attempts beyond the current minimal setup degraded performance.
    leaderboard score 0.47952 → 0.49902 (+0.01950)
- expert 49576186 (Expert) · hms · v157→v163   Add random zeroing of contiguous time-frequency regions in the spectrogram (applied stochastically per sample during training only). Test across multiple runs. If the score does not improve after several attempts, the augmentation is not beneficial for this input representation and should be reverte
    evidence: ✓ Training overfits and label-preserving perturbations are supported by the input semantics. | ✓ Previous augmentation attempts beyond the current minimal setup degraded performance. | ✓ Rare labels or the test-like subgroup receive little influence under the current loss.
    leaderboard score 0.27394 → 0.27691 (+0.00298)
- expert 13542132 (Master) · ranzcr · v2→v3   Add a simple brightness or contrast perturbation as the first augmentation. Use a small fixed offset or random range. Evaluate on the leaderboard; brightness-type augmentations can yield surprisingly large gains on radiograph tasks because they help the model generalize across exposure variations.
    evidence: ✓ Training overfits and label-preserving perturbations are supported by the input semantics. | ✗ Previous augmentation attempts beyond the current minimal setup degraded performance.
    leaderboard score 0.94363 → 0.95160 (+0.00797)
- expert 13542132 (Master) · ranzcr · v9→v13   If several small augmentation parameter sweeps (magnitude, probability, adding/removing transforms) each fail to improve over the baseline, stop iterating on augmentation alone. The lever is likely exhausted; switch to a different lever such as the loss function, learning rate schedule, or model arc
    evidence: ✓ Training overfits and label-preserving perturbations are supported by the input semantics. | ✓ Previous augmentation attempts beyond the current minimal setup degraded performance.
    leaderboard score n/a → 0.94397
- expert 13542132 (Master) · ranzcr · v9→v13   Start with very mild augmentation (small brightness perturbation only). When adding geometric transforms (rotation) or stronger color jitter, keep magnitudes small (a few percent variation) and test each addition individually. If the score drops, revert immediately rather than trying to compensate w
    evidence: ✓ Training overfits and label-preserving perturbations are supported by the input semantics. | ✓ Previous augmentation attempts beyond the current minimal setup degraded performance.
    leaderboard score n/a → 0.94397
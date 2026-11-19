# Augment labeled examples  `T.3.1.3`   11 edits, 0 experts
9 scored cases (improvement signed by each competition's direction), median -0.00298, 2 improved


- expert 17616127 · commonlitreadabilityprize · v49→v50   Swap in the alternative fold predictions and evaluate on the leaderboard. If the score degrades further, abandon that augmentation variant and return to the previously best-performing ensemble composition rather than continuing to explore weaker components.
    evidence: ✓ The training set is small or imbalanced and plausible label-preserving transformations exist. | ✓ Unlabeled in-domain data and a sufficiently reliable teacher are available. | ✓ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.47952 → 0.49902 (lower is better; worse by 0.01950)
- expert 49576186 · hms · v52→v55   Avoid bundling many changes in a single iteration: if the combined result regresses, it is impossible to identify which change caused the harm. Instead, add one change at a time, verify each on the leaderboard or a reliable local validation, and only keep changes that individually help or are neutra
    evidence: ✓ The training set is small or imbalanced and plausible label-preserving transformations exist. | ✓ Rare classes or relevant subgroups contribute too little to the current objective. | ✗ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.37019 → 0.45357 (lower is better; worse by 0.08339)
- expert 49576186 · hms · v58→v60   Extend mixup to blend three samples with a dominant weight on the primary sample (e.g., 0.8) and split the remainder randomly between two other samples. Ensure NaN values in inputs are zeroed before mixing. Evaluate in isolation or with minimal other changes to attribute any score change correctly.
    evidence: ✓ The training set is small or imbalanced and plausible label-preserving transformations exist.
    leaderboard score n/a → 0.41959 (lower is better)
- expert 49576186 · hms · v157→v163   Add random zeroing of contiguous time-frequency regions in the spectrogram (applied stochastically per sample during training only). Test across multiple runs. If the score does not improve after several attempts, the augmentation is not beneficial for this input representation and should be reverte
    evidence: ✓ The training set is small or imbalanced and plausible label-preserving transformations exist. | ✗ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.27394 → 0.27691 (lower is better; worse by 0.00298)
- expert 49576186 · hms · v183→v185   Test augmentation and schedule changes in a separate submission rather than bundling them with the architectural change. If the score regresses even slightly, revert and test each modification independently to isolate which helps and which hurts.
    evidence: ✓ The training set is small or imbalanced and plausible label-preserving transformations exist. | ✗ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.25555 → 0.25639 (lower is better; worse by 0.00084)
- expert 59253662 · learning · v29→v31   Test synthetic oversampling (e.g., interpolation-based minority augmentation) on a holdout before submitting. Expect it to hurt when the metric rewards calibrated predictions rather than balanced accuracy, and when the test distribution is itself imbalanced. If the score drops, revert immediately an
    evidence: ✓ Rare classes or relevant subgroups contribute too little to the current objective. | ✓ The training set is small or imbalanced and plausible label-preserving transformations exist. | ✓ A minority subgroup matches the expected test population and is currently underrepresented. | ✗ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.81830 → 0.81098 (higher is better; worse by 0.00732)
- expert 58130512 · learning · v81→v86   Generate synthetic samples by finding nearest neighbors within each label class (using an approximate nearest-neighbor index for speed) and interpolating their feature vectors. Append these to training folds. Monitor both validation and leaderboard scores carefully: mixup-style augmentation in featu
    evidence: ✓ The training set is small or imbalanced and plausible label-preserving transformations exist. | ✓ A minority subgroup matches the expected test population and is currently underrepresented. | ✗ A prior augmentation trial degraded validation without improving minority-group errors. | ✓ Rare classes or relevant subgroups contribute too little to the current objective.
    leaderboard score 0.82250 → 0.82322 (higher is better; improved by 0.00073)
- expert 58130512 · learning · v86→v87   Remove the augmentation entirely and compare the score. If performance is similar or only marginally worse, the augmentation is not contributing meaningful signal and should be dropped to simplify the pipeline and reduce confounding when tuning other levers.
    evidence: ✓ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.82322 → 0.82230 (higher is better; worse by 0.00092)
- expert 13542132 · ranzcr · v2→v3   Add a simple brightness or contrast perturbation as the first augmentation. Use a small fixed offset or random range. Evaluate on the leaderboard; brightness-type augmentations can yield surprisingly large gains on radiograph tasks because they help the model generalize across exposure variations.
    evidence: ✓ The training set is small or imbalanced and plausible label-preserving transformations exist. | ✗ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.94363 → 0.95160 (higher is better; improved by 0.00797)
- expert 13542132 · ranzcr · v3→v7   When sweeping small hyperparameter changes (split ratio, augmentation strength), compare the observed delta against the run-to-run noise. If the changes produce score movements within the noise band, stop pursuing that lever and move to a qualitatively different approach (e.g., model architecture, r
    evidence: ✓ The training set is small or imbalanced and plausible label-preserving transformations exist. | ✗ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.95160 → 0.94700 (higher is better; worse by 0.00459)
- expert 13542132 · ranzcr · v9→v13   Start with very mild augmentation (small brightness perturbation only). When adding geometric transforms (rotation) or stronger color jitter, keep magnitudes small (a few percent variation) and test each addition individually. If the score drops, revert immediately rather than trying to compensate w
    evidence: ✓ The training set is small or imbalanced and plausible label-preserving transformations exist. | ✓ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score n/a → 0.94397 (higher is better)
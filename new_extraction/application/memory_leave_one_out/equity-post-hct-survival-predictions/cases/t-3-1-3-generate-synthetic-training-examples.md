# Generate synthetic training examples  `T.3.1.3`   4 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median -0.00092, 1 improved


- expert 49576186 · hms · v58→v60   Extend mixup to blend three samples with a dominant weight on the primary sample (e.g., 0.8) and split the remainder randomly between two other samples. Ensure NaN values in inputs are zeroed before mixing. Evaluate in isolation or with minimal other changes to attribute any score change correctly.
    evidence: ✓ Minority examples are sparse but interpolation is meaningful in the current feature space. | ✓ Training overfits and label-preserving perturbations are supported by the input semantics. | ✗ Previous augmentation attempts beyond the current minimal setup degraded performance.
    leaderboard score n/a → 0.41959 (lower is better)
- expert 59253662 · learning · v29→v31   Test synthetic oversampling (e.g., interpolation-based minority augmentation) on a holdout before submitting. Expect it to hurt when the metric rewards calibrated predictions rather than balanced accuracy, and when the test distribution is itself imbalanced. If the score drops, revert immediately an
    evidence: ✓ Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source. | ✓ Rare labels or the test-like subgroup receive little influence under the current loss. | ✗ Minority examples are sparse but interpolation is meaningful in the current feature space. | ✗ Previous augmentation attempts beyond the current minimal setup degraded performance.
    leaderboard score 0.81830 → 0.81098 (higher is better; worse by 0.00732)
- expert 58130512 · learning · v81→v86   Generate synthetic samples by finding nearest neighbors within each label class (using an approximate nearest-neighbor index for speed) and interpolating their feature vectors. Append these to training folds. Monitor both validation and leaderboard scores carefully: mixup-style augmentation in featu
    evidence: ✓ Rare labels or the test-like subgroup receive little influence under the current loss. | ✓ Minority examples are sparse but interpolation is meaningful in the current feature space. | ✗ Previous augmentation attempts beyond the current minimal setup degraded performance. | ✓ Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source.
    leaderboard score 0.82250 → 0.82322 (higher is better; improved by 0.00073)
- expert 58130512 · learning · v86→v87   Remove the augmentation entirely and compare the score. If performance is similar or only marginally worse, the augmentation is not contributing meaningful signal and should be dropped to simplify the pipeline and reduce confounding when tuning other levers.
    evidence: ✓ Previous augmentation attempts beyond the current minimal setup degraded performance.
    leaderboard score 0.82322 → 0.82230 (higher is better; worse by 0.00092)
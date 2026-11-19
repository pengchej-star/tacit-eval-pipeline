# Standardize prediction scales  `T.6.3.2`   3 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00023, 1 improved


- expert 75584724 · equity · v8→v11   Test with and without standardization of the meta-features (fit scaler on out-of-fold predictions, apply to test). Compare leaderboard or validation scores for both settings. If the difference is negligible or negative, keep raw predictions—ranking-based metrics are invariant to monotone transforms 
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✓ A fitted linear combiner receives predictors with very different variance or heavy tails. | ✗ Models expose both logits and probabilities and the metric evaluates distributions.
    leaderboard score n/a → 0.69408 (higher is better)
- expert 75584724 · equity · v12→v13   Try a median-and-IQR-based scaler (robust to outliers) instead of a mean-and-variance scaler for normalizing individual model predictions before weight optimization. Compare leaderboard or validation scores to confirm the benefit.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✓ A fitted linear combiner receives predictors with very different variance or heavy tails.
    leaderboard score 0.69376 → 0.69399 (higher is better; improved by 0.00023)
- expert 55621328 · learning · v131→v134   If rounding thresholds are already optimized on the same fold predictions used to fit the scaler, adding a distribution-matching normalization step is redundant and can hurt. Test this only when there is evidence of a genuine distribution shift between OOF and test predictions, and verify on a held-
    evidence: ✓ Absolute magnitudes are required by a downstream additive correction. | ✓ The metric depends on ordering and member score scales or calibration differ. | ✓ A fitted linear combiner receives predictors with very different variance or heavy tails.
    leaderboard score n/a → 0.80343 (higher is better)
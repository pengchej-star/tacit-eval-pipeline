# Reshape scores before averaging  `T.6.3.3`   3 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00037, 2 improved


- expert 15164527 · ranzcr · v4→v5   Apply a concave power transform (exponent < 1, e.g., square root) to each model's predicted probabilities before the weighted blend. This spreads predictions away from 0/1, which can improve discrimination under AUC. Submit and compare; the gain is typically small, so verify it is consistent and not
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✓ Bounded component probabilities are highly concentrated before averaging. | ✗ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score 0.96642 → 0.96679 (higher is better; improved by 0.00037)
- expert 15164527 · ranzcr · v6→v13   Try a concave power transform (exponent between 0.3 and 0.7) on each model's predictions before weighted averaging. If it helps, consider switching to rank-based averaging instead, which achieves a similar effect without needing to choose the exponent.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✓ Bounded component probabilities are highly concentrated before averaging. | ✗ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score 0.96755 → 0.96772 (higher is better; improved by 0.00018)
- expert 15203842 · ranzcr · v12→v13   Try a power-mean blend: raise each model's predictions to a fractional exponent (e.g., 0.5, i.e., square root) before averaging. This compresses high probabilities less and can better separate classes. Compare the leaderboard score against the simple average to decide whether to keep it.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ.
    leaderboard score n/a → 0.96772 (higher is better)
# Test nonlinear pooling  `T.6.3.6`   3 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00037, 2 improved


- expert 15164527 · ranzcr · v4→v5   Apply a concave power transform (exponent < 1, e.g., square root) to each model's predicted probabilities before the weighted blend. This spreads predictions away from 0/1, which can improve discrimination under AUC. Submit and compare; the gain is typically small, so verify it is consistent and not
    evidence: ✓ The metric is ranking-based and member prediction scales or calibrations differ. | ✓ Probability tails or output scale differences dominate an arithmetic blend. | ✓ The only evaluation feedback is a small public subset and many weights have already been tried.
    leaderboard score 0.96642 → 0.96679 (higher is better; improved by 0.00037)
- expert 15164527 · ranzcr · v6→v13   Try a concave power transform (exponent between 0.3 and 0.7) on each model's predictions before weighted averaging. If it helps, consider switching to rank-based averaging instead, which achieves a similar effect without needing to choose the exponent.
    evidence: ✓ The metric is ranking-based and member prediction scales or calibrations differ. | ✓ Probability tails or output scale differences dominate an arithmetic blend. | ✓ The only evaluation feedback is a small public subset and many weights have already been tried.
    leaderboard score 0.96755 → 0.96772 (higher is better; improved by 0.00018)
- expert 15203842 · ranzcr · v12→v13   Try a power-mean blend: raise each model's predictions to a fractional exponent (e.g., 0.5, i.e., square root) before averaging. This compresses high probabilities less and can better separate classes. Compare the leaderboard score against the simple average to decide whether to keep it.
    evidence: ✓ Members differ in quality or residual patterns and the current blend has not been retuned after a component change. | ✓ The metric is ranking-based and member prediction scales or calibrations differ. | ✓ The only evaluation feedback is a small public subset and many weights have already been tried.
    leaderboard score n/a → 0.96772 (higher is better)
# Construct targets within evaluation groups  `T.5.2.2`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00067, 2 improved


- expert 77450317 · equity · v9→v10   Compute the target transform separately within each subgroup used by the equity metric, then recombine. This ensures each subgroup's target reflects its own event distribution, improving calibration where the metric measures it. Verify with the stratified metric that both mean and variance component
    evidence: ✓ The outcome is censored and ordinary regression targets do not express the observed event information. | ✓ The metric scores predefined groups and their outcome distributions differ substantially. | ✓ The group-conditioning implementation correctly identifies and matches group labels in the data (e.g., no mismatch between string labels and encoded values).
    leaderboard score 0.69562 → 0.69576 (higher is better; improved by 0.00014)
- expert 77129691 · equity · v14→v16   Compute the target transformation (e.g., survival curve estimate or cumulative hazard) separately within each group defined by the fairness variable, then concatenate. This calibrates each group's targets to its own baseline, improving both per-group accuracy and cross-group equity.
    evidence: ✓ The outcome is censored and ordinary regression targets do not express the observed event information. | ✓ The metric scores predefined groups and their outcome distributions differ substantially. | ✓ The group-conditioning implementation correctly identifies and matches group labels in the data (e.g., no mismatch between string labels and encoded values).
    leaderboard score 0.69390 → 0.69457 (higher is better; improved by 0.00067)
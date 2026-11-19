# Simplify numerical preprocessing  `T.3.4.3`   3 edits, 0 experts
1 scored cases, median improvement +0.00012, 1 improved


- expert 27836972 (Expert) · amex · v21→v25   Round continuous features to a small number of decimal places, replace the originals, and evaluate on the leaderboard or validation set. Expect only a marginal gain; treat it as a low-effort addition rather than a major lever.
    evidence: ✗ Scaling, rounding or sparse-column filtering has no demonstrated benefit for the active tree model. | ✓ The active estimator supports NaNs and prior imputation erased useful missingness patterns. | ✗ The active neural or other estimator fails on NaNs or unseen categorical values.
    leaderboard score n/a → 0.79366
- expert 27799930 (Contributor) · amex · v71→v72   Identify columns with high missing-value rates and explicitly drop them before aggregation and training. Verify on validation that dropping them does not hurt the metric. This complements importance-based selection by targeting a different failure mode (sparse signal).
    evidence: ✓ The active estimator supports NaNs and prior imputation erased useful missingness patterns. | ✗ The active neural or other estimator fails on NaNs or unseen categorical values. | ✓ Scaling, rounding or sparse-column filtering has no demonstrated benefit for the active tree model. | ✓ Missingness is concentrated in specific columns with extreme NA rates that differ substantially from the rest of the feature set.
    leaderboard score n/a → n/a
- expert 73937748 (Master) · equity · v12→v13   Try disabling standard scaling of numeric features when the pipeline uses only tree-based models. If the score stays the same or improves, remove scaling permanently to simplify the pipeline.
    evidence: ✓ Scaling, rounding or sparse-column filtering has no demonstrated benefit for the active tree model.
    leaderboard score 0.68793 → 0.68805 (+0.00012)
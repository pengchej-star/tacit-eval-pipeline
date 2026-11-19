# Construct subgroup-aware targets  `T.3.2.2`   2 edits, 0 experts
2 scored cases, median improvement +0.00067, 2 improved


- expert 77450317 (Grandmaster) · equity · v9→v10   Compute the target transform separately within each subgroup used by the equity metric, then recombine. This ensures each subgroup's target reflects its own event distribution, improving calibration where the metric measures it. Verify with the stratified metric that both mean and variance component
    evidence: ✓ Some observed times are censored rather than completed events. | ✓ The score explicitly aggregates performance across groups with different outcome distributions. | ✗ Labels occupy an ordered finite scale while the current learner treats them as unconstrained real values.
    leaderboard score 0.69562 → 0.69576 (+0.00014)
- expert 77129691 (Master) · equity · v14→v16   Compute the target transformation (e.g., survival curve estimate or cumulative hazard) separately within each group defined by the fairness variable, then concatenate. This calibrates each group's targets to its own baseline, improving both per-group accuracy and cross-group equity.
    evidence: ✓ Some observed times are censored rather than completed events. | ✓ The score explicitly aggregates performance across groups with different outcome distributions. | ✓ The existing target transform includes tunable scaling or centering constants. | ✗ Labels occupy an ordered finite scale while the current learner treats them as unconstrained real values.
    leaderboard score 0.69390 → 0.69457 (+0.00067)
# Choose an ordinal prediction formulation  `T.3.2.3`   2 edits, 0 experts
2 scored cases, median improvement +0.00101, 1 improved


- expert 55621328 (Master) · learning · v30→v33   Implement a classification head that outputs softmax probabilities over ordinal classes and takes argmax. Compare its leaderboard score against the regression + optimized-rounding baseline. If classification underperforms, retain the regression approach—threshold optimization on continuous outputs o
    evidence: ✗ Some observed times are censored rather than completed events. | ✗ The score explicitly aggregates performance across groups with different outcome distributions. | ✓ Labels occupy an ordered finite scale while the current learner treats them as unconstrained real values. | ✓ The existing target transform includes tunable scaling or centering constants.
    leaderboard score 0.80353 → 0.79406 (-0.00947)
- expert 55621328 (Master) · learning · v102→v103   Train or obtain checkpoints using an ordinal prediction formulation and swap them into the inference pipeline. Compare leaderboard scores directly; if the ordinal variant matches or exceeds regression, iterate on checkpoint selection and blend weights within that formulation.
    evidence: ✗ Some observed times are censored rather than completed events. | ✓ The score explicitly aggregates performance across groups with different outcome distributions. | ✓ Labels occupy an ordered finite scale while the current learner treats them as unconstrained real values. | ✓ The existing target transform includes tunable scaling or centering constants.
    leaderboard score 0.82366 → 0.82467 (+0.00101)
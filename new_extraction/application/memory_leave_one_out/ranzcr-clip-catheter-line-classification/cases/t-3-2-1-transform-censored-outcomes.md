# Transform censored outcomes  `T.3.2.1`   3 edits, 0 experts
1 scored cases, median improvement -0.00716, 0 improved


- expert 75145694 (Expert) · equity · v1→v2   Use a non-parametric survival estimator (e.g., Kaplan-Meier) to compute survival probabilities at each patient's event time, then use these probabilities as the regression target. This handles censoring naturally and produces a continuous target whose ranking aligns with the concordance metric.
    evidence: ✓ Some observed times are censored rather than completed events. | ✓ The score explicitly aggregates performance across groups with different outcome distributions. | ✗ The existing target transform includes tunable scaling or centering constants.
    leaderboard score 0.68795 → n/a
- expert 73671444 (Grandmaster) · equity · v22→v24   Train separate models on each target transformation and evaluate each in isolation on the leaderboard or a reliable local CV. Even though all monotonic transforms preserve order in theory, regularization and splits differ in practice, so empirical comparison is necessary. Pick the best-performing ta
    evidence: ✓ Some observed times are censored rather than completed events. | ✓ The score explicitly aggregates performance across groups with different outcome distributions. | ✓ The existing target transform includes tunable scaling or centering constants. | ✗ Labels occupy an ordered finite scale while the current learner treats them as unconstrained real values.
    leaderboard score 0.69141 → 0.68425 (-0.00716)
- expert 77276039 (Expert) · equity · v10→v12   Use a Kaplan–Meier estimator to map each patient's (time, event) pair to a survival probability, then train tree-based regressors on this continuous target with cross-validation. Collect out-of-fold predictions and test-set averages, and add them as a new diverse member in a rank-averaged ensemble.
    evidence: ✓ Some observed times are censored rather than completed events. | ✓ The score explicitly aggregates performance across groups with different outcome distributions. | ✗ Labels occupy an ordered finite scale while the current learner treats them as unconstrained real values.
    leaderboard score 0.69330 → n/a
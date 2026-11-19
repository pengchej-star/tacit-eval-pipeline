# Transform the censored outcome  `T.5.2.1`   5 edits, 0 experts
3 scored cases, median improvement +0.00024, 2 improved


- expert 77129691 (Master) · equity · v9→v10   Probe the parameter in small increments (e.g., steps of ~0.1) with single-variable submissions. Track the leaderboard response to map the sensitivity curve and find the local optimum. If partial recovery is seen, continue probing in the improving direction.
    evidence: ✓ The outcome is censored and ordinary regression targets do not express the observed event information. | ✓ The metric scores predefined groups and their outcome distributions differ substantially.
    leaderboard score 0.69004 → 0.69054 (+0.00051)
- expert 77129691 (Master) · equity · v16→v18   Re-tune the hyperparameter by making small incremental changes in one direction, submitting each to the leaderboard. If consecutive steps both improve the score but with diminishing returns, continue until the gain becomes negligible or reverses, then stop near the last improving value.
    evidence: ✓ The outcome is censored and ordinary regression targets do not express the observed event information. | ✓ The metric scores predefined groups and their outcome distributions differ substantially. | ✓ The group-conditioning implementation correctly identifies and matches group labels in the data (e.g., no mismatch between string labels and encoded values).
    leaderboard score 0.69457 → 0.69481 (+0.00024)
- expert 73671444 (Grandmaster) · equity · v22→v24   Train separate models on each target transformation and evaluate each in isolation on the leaderboard or a reliable local CV. Even though all monotonic transforms preserve order in theory, regularization and splits differ in practice, so empirical comparison is necessary. Pick the best-performing ta
    evidence: ✓ The outcome is censored and ordinary regression targets do not express the observed event information. | ✓ The metric scores predefined groups and their outcome distributions differ substantially.
    leaderboard score 0.69141 → 0.68425 (-0.00716)
- expert 75145694 (Expert) · equity · v1→v2   Use a non-parametric survival estimator (e.g., Kaplan-Meier) to compute survival probabilities at each patient's event time, then use these probabilities as the regression target. This handles censoring naturally and produces a continuous target whose ranking aligns with the concordance metric.
    evidence: ✓ The outcome is censored and ordinary regression targets do not express the observed event information. | ✓ The metric scores predefined groups and their outcome distributions differ substantially.
    leaderboard score 0.68795 → n/a
- expert 77276039 (Expert) · equity · v10→v12   Use a Kaplan–Meier estimator to map each patient's (time, event) pair to a survival probability, then train tree-based regressors on this continuous target with cross-validation. Collect out-of-fold predictions and test-set averages, and add them as a new diverse member in a rank-averaged ensemble.
    evidence: ✓ The outcome is censored and ordinary regression targets do not express the observed event information. | ✓ The metric scores predefined groups and their outcome distributions differ substantially.
    leaderboard score 0.69330 → n/a
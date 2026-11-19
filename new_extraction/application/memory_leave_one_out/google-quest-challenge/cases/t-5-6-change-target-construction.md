# Change target construction  `T.5.6`   11 edits, 0 experts
8 scored cases, median improvement +0.00024, 7 improved


- expert 77450317 (Grandmaster) · equity · v9→v10   Compute the target transform separately within each subgroup used by the equity metric, then recombine. This ensures each subgroup's target reflects its own event distribution, improving calibration where the metric measures it. Verify with the stratified metric that both mean and variance component
    evidence: ✓ The raw target encodes censoring, group effects, or offsets poorly represented by the current objective.
    leaderboard score 0.69562 → 0.69576 (+0.00014)
- expert 77129691 (Master) · equity · v9→v10   Probe the parameter in small increments (e.g., steps of ~0.1) with single-variable submissions. Track the leaderboard response to map the sensitivity curve and find the local optimum. If partial recovery is seen, continue probing in the improving direction.
    evidence: ✓ The raw target encodes censoring, group effects, or offsets poorly represented by the current objective.
    leaderboard score 0.69004 → 0.69054 (+0.00051)
- expert 77129691 (Master) · equity · v14→v16   Compute the target transformation (e.g., survival curve estimate or cumulative hazard) separately within each group defined by the fairness variable, then concatenate. This calibrates each group's targets to its own baseline, improving both per-group accuracy and cross-group equity.
    evidence: ✓ The raw target encodes censoring, group effects, or offsets poorly represented by the current objective.
    leaderboard score 0.69390 → 0.69457 (+0.00067)
- expert 77129691 (Master) · equity · v16→v18   Re-tune the hyperparameter by making small incremental changes in one direction, submitting each to the leaderboard. If consecutive steps both improve the score but with diminishing returns, continue until the gain becomes negligible or reverses, then stop near the last improving value.
    evidence: ✓ The raw target encodes censoring, group effects, or offsets poorly represented by the current objective.
    leaderboard score 0.69457 → 0.69481 (+0.00024)
- expert 73671444 (Grandmaster) · equity · v22→v24   Train separate models on each target transformation and evaluate each in isolation on the leaderboard or a reliable local CV. Even though all monotonic transforms preserve order in theory, regularization and splits differ in practice, so empirical comparison is necessary. Pick the best-performing ta
    evidence: ✓ The raw target encodes censoring, group effects, or offsets poorly represented by the current objective.
    leaderboard score 0.69141 → 0.68425 (-0.00716)
- expert 75145694 (Expert) · equity · v1→v2   Use a non-parametric survival estimator (e.g., Kaplan-Meier) to compute survival probabilities at each patient's event time, then use these probabilities as the regression target. This handles censoring naturally and produces a continuous target whose ranking aligns with the concordance metric.
    evidence: ✓ The raw target encodes censoring, group effects, or offsets poorly represented by the current objective.
    leaderboard score 0.68795 → n/a
- expert 77276039 (Expert) · equity · v10→v12   Use a Kaplan–Meier estimator to map each patient's (time, event) pair to a survival probability, then train tree-based regressors on this continuous target with cross-validation. Collect out-of-fold predictions and test-set averages, and add them as a new diverse member in a rank-averaged ensemble.
    evidence: ✓ The raw target encodes censoring, group effects, or offsets poorly represented by the current objective. | ✓ A component is fitted ad hoc without the fold discipline used by the rest of the ensemble.
    leaderboard score 0.69330 → n/a
- expert 73937748 (Master) · equity · v13→v15   Before fitting any auxiliary model used to create target labels, explicitly drop identifier and index columns. After writing the fix, verify it is effective by checking that the variable actually used downstream is the cleaned one, not the original dataframe. A quick sanity check: print the column l
    evidence: ✓ The raw target encodes censoring, group effects, or offsets poorly represented by the current objective.
    leaderboard score 0.68805 → 0.68814 (+0.00009)
- expert 73937748 (Master) · equity · v51→v52   Design a new target transformation (e.g., an exponential or power transform of ranks) that preserves ordering but reshapes the target distribution, train the same model families on this new target, and include their predictions in the ensemble blend. Verify that the blended validation metric improve
    evidence: ✓ The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors. | ✓ The raw target encodes censoring, group effects, or offsets poorly represented by the current objective.
    leaderboard score 0.69100 → 0.69155 (+0.00055)
- expert 58130512 (Master) · learning · v100→v102   Compute the constants once from the full training set (or an oversampled version reflecting the target distribution) and keep them fixed across all folds. This reduces fold-to-fold variance in the learned models and produces a more stable ensemble.
    evidence: ✓ The raw target encodes censoring, group effects, or offsets poorly represented by the current objective. | ✓ Training stops before convergence or continues after validation deterioration. | ✓ The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors. | ✓ A component is fitted ad hoc without the fold discipline used by the rest of the ensemble.
    leaderboard score 0.82301 → 0.82313 (+0.00012)
- expert 58130512 (Master) · learning · v103→v105   Try per-fold target centering (subtract each fold's training mean, then average the fold means to reconstruct the global offset at inference). Compare validation metrics against the fixed global shift. If per-fold centering shows no improvement or adds instability, revert to the simpler fixed shift 
    evidence: ✓ The raw target encodes censoring, group effects, or offsets poorly represented by the current objective.
    leaderboard score 0.82432 → n/a
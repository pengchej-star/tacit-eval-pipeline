# Transform the learning target  `T.4.1`   12 edits, 0 experts
8 scored cases, median improvement +0.00024, 7 improved


- expert 77450317 (Grandmaster) · equity · v9→v10   Compute the target transform separately within each subgroup used by the equity metric, then recombine. This ensures each subgroup's target reflects its own event distribution, improving calibration where the metric measures it. Verify with the stratified metric that both mean and variance component
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression.
    leaderboard score 0.69562 → 0.69576 (+0.00014)
- expert 77129691 (Master) · equity · v9→v10   Probe the parameter in small increments (e.g., steps of ~0.1) with single-variable submissions. Track the leaderboard response to map the sensitivity curve and find the local optimum. If partial recovery is seen, continue probing in the improving direction.
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✗ Repeated augmentation-strength changes have already failed to improve the fixed baseline.
    leaderboard score 0.69004 → 0.69054 (+0.00051)
- expert 77129691 (Master) · equity · v14→v16   Compute the target transformation (e.g., survival curve estimate or cumulative hazard) separately within each group defined by the fairness variable, then concatenate. This calibrates each group's targets to its own baseline, improving both per-group accuracy and cross-group equity.
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression.
    leaderboard score 0.69390 → 0.69457 (+0.00067)
- expert 77129691 (Master) · equity · v16→v18   Re-tune the hyperparameter by making small incremental changes in one direction, submitting each to the leaderboard. If consecutive steps both improve the score but with diminishing returns, continue until the gain becomes negligible or reverses, then stop near the last improving value.
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✗ Repeated augmentation-strength changes have already failed to improve the fixed baseline.
    leaderboard score 0.69457 → 0.69481 (+0.00024)
- expert 73671444 (Grandmaster) · equity · v22→v24   Train separate models on each target transformation and evaluate each in isolation on the leaderboard or a reliable local CV. Even though all monotonic transforms preserve order in theory, regularization and splits differ in practice, so empirical comparison is necessary. Pick the best-performing ta
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✗ Repeated augmentation-strength changes have already failed to improve the fixed baseline.
    leaderboard score 0.69141 → 0.68425 (-0.00716)
- expert 75924487 (Master) · equity · v5→v6   Train the same model type multiple times, each with a different target transformation, generate out-of-fold and test predictions from each, and add all as candidate columns for a stacking or blending ensembler. This increases diversity cheaply because only the label encoding changes, not the feature
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression.
    leaderboard score n/a → 0.69331
- expert 75145694 (Expert) · equity · v1→v2   Use a non-parametric survival estimator (e.g., Kaplan-Meier) to compute survival probabilities at each patient's event time, then use these probabilities as the regression target. This handles censoring naturally and produces a continuous target whose ranking aligns with the concordance metric.
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✓ The loss and output activation optimize a different target structure from the task metric.
    leaderboard score 0.68795 → n/a
- expert 75145694 (Expert) · equity · v3→v4   Create multiple regression targets from the same survival data using distinct statistical transforms of the censored outcome. Train separate base models on each target variant and blend their predictions. Even small per-model gains compound when the transforms are sufficiently decorrelated.
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✗ Repeated augmentation-strength changes have already failed to improve the fixed baseline.
    leaderboard score 0.68865 → 0.68888 (+0.00022)
- expert 75145694 (Expert) · equity · v28→v29   Create experiment-specific feature pipelines so each member model gets tailored features. Compute multiple survival-derived labels (e.g., cumulative hazard and survival probability transforms) as alternative regression targets. Standardize numeric features per-experiment. Expect small but consistent
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✓ The loss and output activation optimize a different target structure from the task metric. | ✗ Repeated augmentation-strength changes have already failed to improve the fixed baseline.
    leaderboard score 0.69133 → 0.69139 (+0.00006)
- expert 77276039 (Expert) · equity · v10→v12   Use a Kaplan–Meier estimator to map each patient's (time, event) pair to a survival probability, then train tree-based regressors on this continuous target with cross-validation. Collect out-of-fold predictions and test-set averages, and add them as a new diverse member in a rank-averaged ensemble.
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✗ Repeated augmentation-strength changes have already failed to improve the fixed baseline.
    leaderboard score 0.69330 → n/a
- expert 73937748 (Master) · equity · v51→v52   Design a new target transformation (e.g., an exponential or power transform of ranks) that preserves ordering but reshapes the target distribution, train the same model families on this new target, and include their predictions in the ensemble blend. Verify that the blended validation metric improve
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✓ The loss and output activation optimize a different target structure from the task metric.
    leaderboard score 0.69100 → 0.69155 (+0.00055)
- expert 58130512 (Master) · learning · v103→v105   Try per-fold target centering (subtract each fold's training mean, then average the fold means to reconstruct the global offset at inference). Compare validation metrics against the fixed global shift. If per-fold centering shows no improvement or adds instability, revert to the simpler fixed shift 
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✓ The loss and output activation optimize a different target structure from the task metric.
    leaderboard score 0.82432 → n/a
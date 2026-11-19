# Tune regularization  `T.5.2`   10 edits, 0 experts
6 scored cases (improvement signed by each competition's direction), median +0.00117, 4 improved


- expert 27389424 · amex · v32→v36   Sweep the L2 regularization parameter in roughly exponential steps (e.g., doubling or more each time). If increasing regularization does not improve validation, revert to a moderate value and instead adjust the minimum samples per leaf downward to restore model expressiveness. Combine both levers ra
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score n/a → n/a (higher is better)
- expert 27389424 · amex · v32→v36   Sweep one regularization axis at a time in coarse exponential steps. When increasing regularization along one axis fails to help across several trials, revert it to a moderate value and compensate by relaxing a different regularization axis (e.g., reduce minimum leaf size). This avoids a full grid s
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score n/a → n/a (higher is better)
- expert 27389424 · amex · v63→v64   Enable column subsampling and row subsampling (e.g., both around 0.3) so each tree sees a random subset of features and rows. Also increase early-stopping patience proportionally so the model can still find its best iteration under the added noise.
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability. | ✓ Training stops before convergence or continues after validation deterioration.
    leaderboard score 0.78859 → 0.79155 (higher is better; improved by 0.00296)
- expert 27389424 · amex · v78→v82   Fix the first parameter near its optimum, activate the second regularization control, and re-sweep the first parameter to capture any interaction. Compare local validation against the single-control best. If no improvement is observed across the sweep, revert the second control and keep the simpler 
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score n/a → n/a (higher is better)
- expert 27389424 · amex · v96→v131   Expect diminishing returns: regularization strength tuning on gradient-boosted trees typically yields only marginal gains after tree depth, learning rate, and iteration count are set. Limit the sweep to a coarse log-scale grid (e.g., 5–7 values spanning 4 orders of magnitude) for each penalty type, 
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability. | ✗ Tree models show underfitting or overfitting associated with depth or leaf count. | ✗ Training stops before convergence or continues after validation deterioration. | ✗ The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors. | ✓ The current boosting procedure has plateaued or its interface blocks required training controls.
    leaderboard score n/a → n/a (higher is better)
- expert 59253662 · learning · v37→v39   Do not change multiple things at once (new features and hyperparameter adjustments) in a single submission. When a large batch of new features is added, keep the previously validated hyperparameters fixed first to isolate the effect of the features. If the combined change hurts, you cannot tell whic
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability. | ✗ The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors.
    leaderboard score 0.82433 → 0.81519 (higher is better; worse by 0.00914)
- expert 55987255 · learning · v9→v10   Try substantially increasing L1 regularization (e.g., doubling or tripling it) to encourage sparsity over noisy features, while simultaneously reducing L2 regularization and modestly increasing the number of trees to compensate for the stronger sparsity penalty. Evaluate each combination on the lead
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability. | ✗ A lower learning rate was introduced without increasing the iteration budget.
    leaderboard score 0.81798 → 0.81914 (higher is better; improved by 0.00117)
- expert 55591012 · learning · v10→v12   Avoid jumping regularization coefficients by orders of magnitude in a single step (e.g., 0.1 → 100). Such extreme changes often over-regularize and degrade the score. Instead, sweep multiplicatively in smaller factors (e.g., ×2 or ×5), evaluate each, and stop when the validation metric stops improvi
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score 0.81126 → 0.80877 (higher is better; worse by 0.00249)
- expert 55591012 · learning · v34→v39   After trying small increments in both directions and seeing no clear improvement, make a larger jump (e.g., double the value) to escape the local region. Submit each change individually to isolate its effect. If the larger jump improves, continue exploring in that direction.
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score 0.81994 → 0.81998 (higher is better; improved by 0.00004)
- expert 13702907 · ranzcr · v15→v16   Simultaneously reduce the dropout rate (e.g., roughly halve it) and swap in a checkpoint trained with different or longer training. Changing two correlated levers together is acceptable when each alone is cheap to test and the plateau is persistent.
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score 0.94937 → 0.95396 (higher is better; improved by 0.00460)
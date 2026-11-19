# Tune regularization and subsampling  `T.4.3.2`   12 edits, 0 experts
5 scored cases (improvement signed by each competition's direction), median +0.00030, 4 improved


- expert 27389424 · amex · v32→v36   Sweep the L2 regularization parameter in roughly exponential steps (e.g., doubling or more each time). If increasing regularization does not improve validation, revert to a moderate value and instead adjust the minimum samples per leaf downward to restore model expressiveness. Combine both levers ra
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set. | ✗ Loss is unstable or learning is too slow at the current step size.
    leaderboard score n/a → n/a (higher is better)
- expert 27389424 · amex · v63→v64   Enable column subsampling and row subsampling (e.g., both around 0.3) so each tree sees a random subset of features and rows. Also increase early-stopping patience proportionally so the model can still find its best iteration under the added noise.
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set.
    leaderboard score 0.78859 → 0.79155 (higher is better; improved by 0.00296)
- expert 27389424 · amex · v78→v82   Fix the first parameter near its optimum, activate the second regularization control, and re-sweep the first parameter to capture any interaction. Compare local validation against the single-control best. If no improvement is observed across the sweep, revert the second control and keep the simpler 
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set. | ✗ Loss is unstable or learning is too slow at the current step size. | ✓ Training fits well but validation worsens as depth or leaf count increases. | ✗ Training hits its round limit or stops while the monitored metric is still improving.
    leaderboard score n/a → n/a (higher is better)
- expert 27389424 · amex · v96→v131   Expect diminishing returns: regularization strength tuning on gradient-boosted trees typically yields only marginal gains after tree depth, learning rate, and iteration count are set. Limit the sweep to a coarse log-scale grid (e.g., 5–7 values spanning 4 orders of magnitude) for each penalty type, 
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set. | ✗ Training hits its round limit or stops while the monitored metric is still improving. | ✗ Loss is unstable or learning is too slow at the current step size.
    leaderboard score n/a → n/a (higher is better)
- expert 27799930 · amex · v3→v11   Try two complementary strategies and compare on the validation metric: (1) reduce the learning rate and increase subsampling to reduce variance, or (2) keep a moderate learning rate but add explicit regularization (L2, minimum leaf weight, pruning threshold) and enable early stopping with a held-out
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set. | ✓ Loss is unstable or learning is too slow at the current step size. | ✗ Several compatible snapshots already exist but have not been compared under one inference configuration. | ✓ Training hits its round limit or stops while the monitored metric is still improving.
    leaderboard score n/a → n/a (higher is better)
- expert 7613444 · google · v5→v6   Add dropout layers to each branch's classification head between the pooled representation and the output layer. Expect a small but consistent improvement; verify on the held-out metric before combining with other changes.
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set. | ✗ Training hits its round limit or stops while the monitored metric is still improving.
    leaderboard score 0.39802 → 0.39832 (higher is better; improved by 0.00030)
- expert 7670859 · google · v5→v9   Recognize that if multiple small tweaks to dropout, head complexity, and training-set filtering all yield the same score, the bottleneck is likely structural (e.g., ensembling, post-processing, or representation quality) rather than in minor regularization details. Pivot to a qualitatively different
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set.
    leaderboard score n/a → 0.38252 (higher is better)
- expert 7253130 · google · v3→v5   Re-tune the learning rate and dropout in small sequential steps, changing one at a time and submitting after each change to isolate effects. Start by lowering the learning rate (the loss surface changed) and reducing dropout, then adjust dropout back up if the lower rate already stabilizes training.
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set. | ✓ Loss is unstable or learning is too slow at the current step size.
    leaderboard score n/a → 0.36997 (higher is better)
- expert 7253130 · google · v5→v8   Treat the failed sweep as evidence that the bottleneck is not optimization speed but model capacity or stability. Add architectural components to the head (e.g., normalization layers, additional dense layers) to stabilize training, then re-tune the learning rate at a moderate value. This two-phase a
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set. | ✓ Loss is unstable or learning is too slow at the current step size.
    leaderboard score 0.36997 → n/a (higher is better)
- expert 55987255 · learning · v9→v10   Try substantially increasing L1 regularization (e.g., doubling or tripling it) to encourage sparsity over noisy features, while simultaneously reducing L2 regularization and modestly increasing the number of trees to compensate for the stronger sparsity penalty. Evaluate each combination on the lead
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set. | ✓ Training hits its round limit or stops while the monitored metric is still improving.
    leaderboard score 0.81798 → 0.81914 (higher is better; improved by 0.00117)
- expert 55591012 · learning · v10→v12   Avoid jumping regularization coefficients by orders of magnitude in a single step (e.g., 0.1 → 100). Such extreme changes often over-regularize and degrade the score. Instead, sweep multiplicatively in smaller factors (e.g., ×2 or ×5), evaluate each, and stop when the validation metric stops improvi
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set.
    leaderboard score 0.81126 → 0.80877 (higher is better; worse by 0.00249)
- expert 55591012 · learning · v34→v39   After trying small increments in both directions and seeing no clear improvement, make a larger jump (e.g., double the value) to escape the local region. Submit each change individually to isolate its effect. If the larger jump improves, continue exploring in that direction.
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set.
    leaderboard score 0.81994 → 0.81998 (higher is better; improved by 0.00004)
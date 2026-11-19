# Tune tree regularization  `T.6.1.2`   8 edits, 0 experts
3 scored cases, median improvement +0.00004, 2 improved


- expert 27389424 (Grandmaster) · amex · v32→v36   Sweep the L2 regularization parameter in roughly exponential steps (e.g., doubling or more each time). If increasing regularization does not improve validation, revert to a moderate value and instead adjust the minimum samples per leaf downward to restore model expressiveness. Combine both levers ra
    evidence: ✓ Training fit is strong but validation worsens as complexity grows.
    leaderboard score n/a → n/a
- expert 27389424 (Grandmaster) · amex · v32→v36   Sweep one regularization axis at a time in coarse exponential steps. When increasing regularization along one axis fails to help across several trials, revert it to a moderate value and compensate by relaxing a different regularization axis (e.g., reduce minimum leaf size). This avoids a full grid s
    evidence: ✓ Training fit is strong but validation worsens as complexity grows.
    leaderboard score n/a → n/a
- expert 27389424 (Grandmaster) · amex · v78→v82   Fix the first parameter near its optimum, activate the second regularization control, and re-sweep the first parameter to capture any interaction. Compare local validation against the single-control best. If no improvement is observed across the sweep, revert the second control and keep the simpler 
    evidence: ✓ Training fit is strong but validation worsens as complexity grows. | ✓ Training error remains high with shallow or small trees.
    leaderboard score n/a → n/a
- expert 58130512 (Master) · learning · v7→v9   First verify whether the new features themselves are the problem by removing them and checking whether the original score is restored, before spending iterations on regularization tuning. Regularization adjustments rarely compensate for features that add noise; removing the offending features is a f
    evidence: ✓ Training fit is strong but validation worsens as complexity grows. | ✓ Trees repeatedly use the same dominant rows or feature groups.
    leaderboard score n/a → 0.81420
- expert 60197293 (Expert) · learning · v45→v55   Vary one lever at a time while holding the other fixed, then submit or validate the best single-lever setting before combining changes. When a change worsens the score, revert it before trying the next lever. Avoid submitting configurations that bundle multiple untested changes, because a regression
    evidence: ✓ Training fit is strong but validation worsens as complexity grows.
    leaderboard score 0.81867 → n/a
- expert 55987255 (Master) · learning · v9→v10   Try substantially increasing L1 regularization (e.g., doubling or tripling it) to encourage sparsity over noisy features, while simultaneously reducing L2 regularization and modestly increasing the number of trees to compensate for the stronger sparsity penalty. Evaluate each combination on the lead
    evidence: ✓ Training fit is strong but validation worsens as complexity grows.
    leaderboard score 0.81798 → 0.81914 (+0.00117)
- expert 55591012 (Grandmaster) · learning · v10→v12   Avoid jumping regularization coefficients by orders of magnitude in a single step (e.g., 0.1 → 100). Such extreme changes often over-regularize and degrade the score. Instead, sweep multiplicatively in smaller factors (e.g., ×2 or ×5), evaluate each, and stop when the validation metric stops improvi
    evidence: ✓ Training fit is strong but validation worsens as complexity grows.
    leaderboard score 0.81126 → 0.80877 (-0.00249)
- expert 55591012 (Grandmaster) · learning · v34→v39   After trying small increments in both directions and seeing no clear improvement, make a larger jump (e.g., double the value) to escape the local region. Submit each change individually to isolate its effect. If the larger jump improves, continue exploring in that direction.
    evidence: ✓ Training fit is strong but validation worsens as complexity grows. | ✓ Trees repeatedly use the same dominant rows or feature groups.
    leaderboard score 0.81994 → 0.81998 (+0.00004)
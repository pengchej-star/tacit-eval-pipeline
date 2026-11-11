# Tune target scaling or centering  `T.3.2.4`   3 edits, 0 experts
2 scored cases, median improvement +0.00051, 2 improved


- expert 77129691 (Master) · equity · v9→v10   Probe the parameter in small increments (e.g., steps of ~0.1) with single-variable submissions. Track the leaderboard response to map the sensitivity curve and find the local optimum. If partial recovery is seen, continue probing in the improving direction.
    evidence: ✓ Some observed times are censored rather than completed events. | ✓ The score explicitly aggregates performance across groups with different outcome distributions. | ✗ Labels occupy an ordered finite scale while the current learner treats them as unconstrained real values. | ✓ The existing target transform includes tunable scaling or centering constants.
    leaderboard score 0.69004 → 0.69054 (+0.00051)
- expert 77129691 (Master) · equity · v16→v18   Re-tune the hyperparameter by making small incremental changes in one direction, submitting each to the leaderboard. If consecutive steps both improve the score but with diminishing returns, continue until the gain becomes negligible or reverses, then stop near the last improving value.
    evidence: ✓ Some observed times are censored rather than completed events. | ✓ The score explicitly aggregates performance across groups with different outcome distributions. | ✗ Labels occupy an ordered finite scale while the current learner treats them as unconstrained real values. | ✓ The existing target transform includes tunable scaling or centering constants.
    leaderboard score 0.69457 → 0.69481 (+0.00024)
- expert 58130512 (Master) · learning · v103→v105   Try per-fold target centering (subtract each fold's training mean, then average the fold means to reconstruct the global offset at inference). Compare validation metrics against the fixed global shift. If per-fold centering shows no improvement or adds instability, revert to the simpler fixed shift 
    evidence: ✗ Some observed times are censored rather than completed events. | ✓ The score explicitly aggregates performance across groups with different outcome distributions. | ✓ Labels occupy an ordered finite scale while the current learner treats them as unconstrained real values. | ✓ The existing target transform includes tunable scaling or centering constants.
    leaderboard score 0.82432 → n/a
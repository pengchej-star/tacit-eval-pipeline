# Tune boosting rate and rounds  `T.6.1.4`   6 edits, 0 experts
2 scored cases, median improvement +0.00201, 1 improved


- expert 27389424 (Grandmaster) · amex · v64→v66   When reducing the learning rate by a factor of k, increase the maximum number of boosting rounds by at least the same factor k (and increase early-stopping patience similarly). If the budget cannot be scaled proportionally due to time or resource constraints, keep the higher learning rate.
    evidence: ✓ A reduced learning rate exhausts the iteration budget before convergence. | ✗ Trees repeatedly use the same dominant rows or feature groups.
    leaderboard score 0.79155 → 0.79083 (-0.00072)
- expert 27389424 (Grandmaster) · amex · v66→v70   When using early stopping, test learning rates across at least one order of magnitude. If a lower rate degrades the score, it likely means the model is stopping before it has converged. Increase the rate (or increase patience/max iterations) and verify with a leaderboard or validation check.
    evidence: ✓ A reduced learning rate exhausts the iteration budget before convergence.
    leaderboard score 0.79083 → 0.79285 (+0.00201)
- expert 28984551 (Contributor) · amex · v1→v2   Increase the learning rate by a moderate factor (e.g., 3–4×) and proportionally decrease the number of boosting rounds so the total effective learning stays similar. Simultaneously allow slightly more complex trees (increase leaf count modestly) to compensate for fewer rounds. Verify on the leaderbo
    evidence: ✓ A reduced learning rate exhausts the iteration budget before convergence.
    leaderboard score n/a → 0.79600
- expert 27799930 (Contributor) · amex · v13→v16   First set the number of rounds much higher than needed (e.g., 10–20× the current value) and rely on early stopping to find the effective count. Then halve the learning rate and proportionally adjust the round budget; the early-stopping callback will still protect against overfitting while the smalle
    evidence: ✓ A reduced learning rate exhausts the iteration budget before convergence.
    leaderboard score n/a → n/a
- expert 27799930 (Contributor) · amex · v75→v79   When enabling a dropout booster, start by reducing the learning rate substantially (e.g., by a factor of 3–4×) relative to the value tuned for the standard booster, then sweep upward in small increments, evaluating the validation metric at each step, before committing to a submission.
    evidence: ✓ A reduced learning rate exhausts the iteration budget before convergence.
    leaderboard score n/a → n/a
- expert 27825577 (Expert) · amex · v5→v11   Sweep the learning rate across a wide range (e.g., 0.01 to 0.2) while co-adjusting tree depth. Very low rates may underfit if early stopping triggers too soon; very high rates may overfit. After bracketing, narrow in on the best region. Pair lower learning rates with shallower trees and longer early
    evidence: ✗ A reduced learning rate exhausts the iteration budget before convergence. | ✓ Training fit is strong but validation worsens as complexity grows.
    leaderboard score n/a → 0.79425
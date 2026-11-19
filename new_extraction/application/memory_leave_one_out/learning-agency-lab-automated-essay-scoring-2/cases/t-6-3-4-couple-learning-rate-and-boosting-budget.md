# Couple learning rate and boosting budget  `T.6.3.4`   6 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00201, 2 improved


- expert 27389424 · amex · v64→v66   When reducing the learning rate by a factor of k, increase the maximum number of boosting rounds by at least the same factor k (and increase early-stopping patience similarly). If the budget cannot be scaled proportionally due to time or resource constraints, keep the higher learning rate.
    evidence: ✗ Every tree sees all rows and columns and the model overfits after feature selection. | ✓ Lower learning rates reach the round cap or trigger stopping before sustained convergence. | ✗ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble.
    leaderboard score 0.79155 → 0.79083 (higher is better; worse by 0.00072)
- expert 27389424 · amex · v66→v70   When using early stopping, test learning rates across at least one order of magnitude. If a lower rate degrades the score, it likely means the model is stopping before it has converged. Increase the rate (or increase patience/max iterations) and verify with a leaderboard or validation check.
    evidence: ✓ Lower learning rates reach the round cap or trigger stopping before sustained convergence. | ✗ Every tree sees all rows and columns and the model overfits after feature selection. | ✗ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble.
    leaderboard score 0.79083 → 0.79285 (higher is better; improved by 0.00201)
- expert 28984551 · amex · v1→v2   Increase the learning rate by a moderate factor (e.g., 3–4×) and proportionally decrease the number of boosting rounds so the total effective learning stays similar. Simultaneously allow slightly more complex trees (increase leaf count modestly) to compensate for fewer rounds. Verify on the leaderbo
    evidence: ✓ Lower learning rates reach the round cap or trigger stopping before sustained convergence. | ✗ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble.
    leaderboard score n/a → 0.79600 (higher is better)
- expert 27799930 · amex · v13→v16   First set the number of rounds much higher than needed (e.g., 10–20× the current value) and rely on early stopping to find the effective count. Then halve the learning rate and proportionally adjust the round budget; the early-stopping callback will still protect against overfitting while the smalle
    evidence: ✗ Every tree sees all rows and columns and the model overfits after feature selection. | ✓ Lower learning rates reach the round cap or trigger stopping before sustained convergence. | ✗ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble.
    leaderboard score n/a → n/a (higher is better)
- expert 27799930 · amex · v75→v79   When enabling a dropout booster, start by reducing the learning rate substantially (e.g., by a factor of 3–4×) relative to the value tuned for the standard booster, then sweep upward in small increments, evaluating the validation metric at each step, before committing to a submission.
    evidence: ✓ Lower learning rates reach the round cap or trigger stopping before sustained convergence.
    leaderboard score n/a → n/a (higher is better)
- expert 13542132 · ranzcr · v13→v14   Increase the learning rate (e.g., double it) to compensate for the smaller effective gradients, and raise regularization strength proportionally to prevent the larger step size from overfitting. Treat the loss change as requiring a coordinated update of at least learning rate and regularization, not
    evidence: ✗ Training fit is poor under shallow trees or prior depth changes show a clear capacity effect. | ✗ Training improves while validation stagnates under the current tree capacity. | ✗ Every tree sees all rows and columns and the model overfits after feature selection. | ✗ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble.
    leaderboard score 0.94397 → 0.95109 (higher is better; improved by 0.00713)
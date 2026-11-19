# Use a smoother stopping proxy  `T.1.2.2`   2 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median -0.00115, 0 improved


- expert 28093671 · amex · v34→v37   When expanding features, switch the evaluation metric to a standard smooth proxy (e.g., AUC or log-loss) for more stable early stopping. Increase the learning rate moderately to speed up convergence, set a generous boosting-round budget, and rely on early stopping to find the right number of rounds.
    evidence: ✓ Early-stopping patience (early_stopping_rounds) is too short for the noise level of the current selection metric, risking premature stopping before the true best iteration. | ✓ The task metric fluctuates sharply between nearby iterations while a smooth proxy tracks generalization better.
    leaderboard score n/a → 0.79304 (higher is better)
- expert 27656049 · amex · v16→v18   Try the custom metric as the eval function in one experiment and compare against the standard surrogate loss. If the score drops, revert to the surrogate loss for early stopping; the smooth loss often selects a better stopping point even when the final evaluation uses a different metric.
    evidence: ✓ The current stopping metric differs from the scored objective and selects worse checkpoints in prior comparisons. | ✓ The task metric fluctuates sharply between nearby iterations while a smooth proxy tracks generalization better.
    leaderboard score 0.79171 → 0.79056 (higher is better; worse by 0.00115)
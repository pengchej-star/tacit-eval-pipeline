# Use a stable proxy for stopping  `T.2.3.2`   1 edits, 0 experts

- expert 28093671 (Contributor) · amex · v34→v37   When expanding features, switch the evaluation metric to a standard smooth proxy (e.g., AUC or log-loss) for more stable early stopping. Increase the learning rate moderately to speed up convergence, set a generous boosting-round budget, and rely on early stopping to find the right number of rounds.
    evidence: ✓ The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing. | ✓ The task metric fluctuates sharply between adjacent iterations while a smooth proxy is stable.
    leaderboard score n/a → 0.79304
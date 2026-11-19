# Refit on more labeled data  `T.3.1.4`   3 edits, 0 experts
1 scored cases, median improvement +0.00076, 1 improved


- expert 29588171 (Master) · amex · v24→v34   When a model's blend weight is very small and early stopping is not used, train on the full labeled set to maximize the quality of its small contribution. Reserve a validation split only when the model's weight is large enough that overfitting would materially hurt the blend.
    evidence: ✓ The configuration is fixed and a retained holdout is no longer needed for fitting decisions. | ✗ The proposed membership change risks reducing the training set size enough to cause underfitting. | ✓ The effect of the most recent training-membership change has not yet been scored, so its impact is unknown.
    leaderboard score n/a → 0.79980
- expert 7670859 (Contributor) · google · v27→v31   Use the fixed holdout only for local debugging and hyperparameter selection. For the final submission, disable the holdout and train on all available data using k-fold cross-validation, so every example contributes to the model. Compare leaderboard scores with and without the holdout to confirm the 
    evidence: ✓ The configuration is fixed and a retained holdout is no longer needed for fitting decisions. | ✓ The proposed membership change risks reducing the training set size enough to cause underfitting. | ✓ The effect of the most recent training-membership change has not yet been scored, so its impact is unknown.
    leaderboard score 0.39282 → 0.39358 (+0.00076)
- expert 7670859 (Contributor) · google · v23→v27   Keep a single code path with a simple toggle (e.g., commenting out or a boolean flag) that controls whether a holdout split is applied. Use the holdout mode to validate feature changes, then disable it to train on the full dataset before submitting.
    evidence: ✓ The configuration is fixed and a retained holdout is no longer needed for fitting decisions. | ✗ The proposed membership change risks reducing the training set size enough to cause underfitting. | ✓ The effect of the most recent training-membership change has not yet been scored, so its impact is unknown.
    leaderboard score n/a → 0.39282
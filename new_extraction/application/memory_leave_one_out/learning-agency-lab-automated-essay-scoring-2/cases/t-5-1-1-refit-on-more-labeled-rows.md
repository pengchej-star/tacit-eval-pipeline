# Refit on more labeled rows  `T.5.1.1`   4 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00076, 1 improved


- expert 29588171 · amex · v24→v34   When a model's blend weight is very small and early stopping is not used, train on the full labeled set to maximize the quality of its small contribution. Reserve a validation split only when the model's weight is large enough that overfitting would materially hurt the blend.
    evidence: ✓ A substantial labeled holdout remains unused after the configuration has already been selected. | ✗ Previous filtering or data-selection changes regressed the score, suggesting the current selection should be reverted or refined rather than extended.
    leaderboard score n/a → 0.79980 (higher is better)
- expert 29588171 · amex · v37→v40   Try a small holdout (e.g., 10%) versus a large one (e.g., 40%). If the leaderboard score improves with the smaller holdout, keep it: the extra training data outweighs the value of a more precise local validation estimate when the model is only a minor blend component.
    evidence: ✓ A substantial labeled holdout remains unused after the configuration has already been selected. | ✓ Previous filtering or data-selection changes regressed the score, suggesting the current selection should be reverted or refined rather than extended.
    leaderboard score 0.79961 → 0.79943 (higher is better; worse by 0.00018)
- expert 7670859 · google · v23→v27   Keep a single code path with a simple toggle (e.g., commenting out or a boolean flag) that controls whether a holdout split is applied. Use the holdout mode to validate feature changes, then disable it to train on the full dataset before submitting.
    evidence: ✓ A substantial labeled holdout remains unused after the configuration has already been selected. | ✓ The competition metric is rank-based or otherwise insensitive to the class-weight direction being explored.
    leaderboard score n/a → 0.39282 (higher is better)
- expert 7670859 · google · v27→v31   Use the fixed holdout only for local debugging and hyperparameter selection. For the final submission, disable the holdout and train on all available data using k-fold cross-validation, so every example contributes to the model. Compare leaderboard scores with and without the holdout to confirm the 
    evidence: ✓ A substantial labeled holdout remains unused after the configuration has already been selected. | ✓ Previous filtering or data-selection changes regressed the score, suggesting the current selection should be reverted or refined rather than extended. | ✗ The competition metric is rank-based or otherwise insensitive to the class-weight direction being explored.
    leaderboard score 0.39282 → 0.39358 (higher is better; improved by 0.00076)
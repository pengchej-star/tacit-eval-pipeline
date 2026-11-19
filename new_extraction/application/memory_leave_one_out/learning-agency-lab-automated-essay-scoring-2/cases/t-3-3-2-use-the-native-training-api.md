# Use the native training API  `T.3.3.2`   1 edits, 0 experts
1 scored cases, median improvement -0.00014, 0 improved


- expert 29588171 (Master) · amex · v9→v10   Switch to the native training API with a held-out validation set and early stopping. Compare the leaderboard score at the same blend weight. If the score does not improve, the gain from API-level control is negligible and effort is better spent elsewhere (e.g., features or hyperparameters).
    evidence: ✗ The configured accelerator or dataframe backend does not support a required operation. | ✓ The current wrapper cannot expose the needed custom metric or iteration control. | ✗ The estimator wrapper already supports the required stopping and probability outputs.
    leaderboard score 0.79988 → 0.79973 (-0.00014)
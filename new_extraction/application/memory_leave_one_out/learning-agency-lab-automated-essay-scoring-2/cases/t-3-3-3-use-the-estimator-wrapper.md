# Use the estimator wrapper  `T.3.3.3`   1 edits, 0 experts

- expert 27656049 (Expert) · amex · v6→v7   Use the scikit-learn-compatible estimator class. It handles dataset wrapping internally, provides a predict_proba method for direct probability output, and accepts early-stopping callbacks in the fit call, reducing boilerplate and integration friction.
    evidence: ✗ The configured accelerator or dataframe backend does not support a required operation. | ✓ The estimator wrapper already supports the required stopping and probability outputs.
    leaderboard score n/a → n/a
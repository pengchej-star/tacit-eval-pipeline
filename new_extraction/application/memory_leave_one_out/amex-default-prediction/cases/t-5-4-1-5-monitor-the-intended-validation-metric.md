# Monitor the intended validation metric  `T.5.4.1.5`   3 edits, 0 experts

- expert 55431616 · learning · v22→v23   Explicitly set the early-stopping callback to reference the custom metric by name, enable the maximize flag, and turn on best-model saving so the checkpoint corresponds to the peak of the custom metric rather than the last iteration or the minimum of a loss.
    evidence: ✓ The stopping callback monitors training data, the wrong metric direction, or the wrong validation set. | ✓ The proposed edit changes only one hyperparameter at a time, consistent with controlled experimentation.
    leaderboard score n/a → n/a (higher is better)
- expert 60197293 · learning · v55→v56   Explicitly specify the name or index of the validation evaluation set in the early-stopping callback configuration. Also suppress verbose per-iteration logging to keep output manageable during hyperparameter sweeps.
    evidence: ✓ The stopping callback monitors training data, the wrong metric direction, or the wrong validation set. | ✗ The proposed edit changes only one hyperparameter at a time, consistent with controlled experimentation.
    leaderboard score n/a → n/a (higher is better)
- expert 60197293 · learning · v99→v101   Test early stopping in a validation-only run. If removing early stopping and instead reducing the regularization penalty yields a better validation or leaderboard score, prefer the fixed-iteration approach with lighter regularization. Avoid changing both early stopping and regularization simultaneou
    evidence: ✓ Validation is still improving at the final epoch or worsens well before it. | ✓ The stopping callback monitors training data, the wrong metric direction, or the wrong validation set. | ✓ The proposed edit changes only one hyperparameter at a time, consistent with controlled experimentation.
    leaderboard score n/a → 0.82142 (higher is better)
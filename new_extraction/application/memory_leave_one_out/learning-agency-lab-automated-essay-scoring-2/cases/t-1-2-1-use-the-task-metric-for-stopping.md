# Use the task metric for stopping  `T.1.2.1`   5 edits, 0 experts

- expert 27389424 · amex · v48→v49   Write a custom evaluation function in the format required by the training library's callback/feval interface, returning the competition metric computed on the validation fold. Pass it as the eval metric with early stopping. After switching to the custom metric, re-tune other hyperparameters (e.g., f
    evidence: ✓ The current stopping metric differs from the scored objective and selects worse checkpoints in prior comparisons. | ✓ Callback values or shapes disagree with an independent calculation.
    leaderboard score n/a → n/a (higher is better)
- expert 27389424 · amex · v54→v55   Switch from the high-level wrapper to the native training API so a custom evaluation function matching the competition metric can be passed as the early-stopping criterion. Verify that predictions are extracted consistently (e.g., raw scores vs. probabilities) after the API change.
    evidence: ✓ The current stopping metric differs from the scored objective and selects worse checkpoints in prior comparisons. | ✓ Callback values or shapes disagree with an independent calculation.
    leaderboard score n/a → n/a (higher is better)
- expert 27825577 · amex · v4→v5   Implement the true evaluation metric as a custom callback/eval function and pass it to the training loop. When switching to a custom metric, substantially increase the early-stopping patience (e.g., 5× the previous value) because the custom metric may be noisier or converge differently than the defa
    evidence: ✓ The current stopping metric differs from the scored objective and selects worse checkpoints in prior comparisons. | ✓ Early-stopping patience (early_stopping_rounds) is too short for the noise level of the current selection metric, risking premature stopping before the true best iteration.
    leaderboard score n/a → n/a (higher is better)
- expert 27825577 · amex · v20→v25   Implement the custom metric as a standalone Python function that takes true labels and predictions, returns (metric_name, value). Pass it to the training API's custom-metric argument. Because wiring errors (wrong function name, wrong reference) are common, verify by running a short training loop and
    evidence: ✓ The current stopping metric differs from the scored objective and selects worse checkpoints in prior comparisons. | ✓ Callback values or shapes disagree with an independent calculation.
    leaderboard score n/a → n/a (higher is better)
- expert 28093671 · amex · v10→v11   Implement the competition's custom metric as a callback or custom evaluation function passed to the training API, so early stopping and model selection optimize for the true objective. At the same time, tune tree depth, row/column subsampling, and data-loading strategy to keep iteration fast.
    evidence: ✓ The current stopping metric differs from the scored objective and selects worse checkpoints in prior comparisons.
    leaderboard score n/a → n/a (higher is better)
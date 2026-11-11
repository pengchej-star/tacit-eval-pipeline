# Use the task metric  `T.2.3.1`   12 edits, 0 experts
1 scored cases, median improvement -0.00115, 0 improved


- expert 27389424 (Grandmaster) · amex · v48→v49   Write a custom evaluation function in the format required by the training library's callback/feval interface, returning the competition metric computed on the validation fold. Pass it as the eval metric with early stopping. After switching to the custom metric, re-tune other hyperparameters (e.g., f
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction. | ✗ The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing.
    leaderboard score n/a → n/a
- expert 27389424 (Grandmaster) · amex · v54→v55   Switch from the high-level wrapper to the native training API so a custom evaluation function matching the competition metric can be passed as the early-stopping criterion. Verify that predictions are extracted consistently (e.g., raw scores vs. probabilities) after the API change.
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction. | ✗ The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing.
    leaderboard score n/a → n/a
- expert 27389424 (Grandmaster) · amex · v82→v85   Enable a fast debug mode to run the pipeline quickly, inspect the metric function call for correctness (especially that both labels and predictions are passed), fix any argument errors, and serialize per-fold predictions and indices to disk so they can be independently verified offline.
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction. | ✗ The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing.
    leaderboard score n/a → n/a
- expert 27502740 (Grandmaster) · amex · v3→v4   At the entry of any custom metric function, flatten the prediction array (e.g., ravel) so it is always 1-D, regardless of the shape the framework supplies. This prevents shape-mismatch errors in downstream sorting and arithmetic.
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction.
    leaderboard score n/a → n/a
- expert 27502740 (Grandmaster) · amex · v7→v8   At the top of any custom metric function, unconditionally flatten or squeeze the prediction array to 1-D (e.g., ravel). This defensive step costs nothing and prevents recurring shape-mismatch bugs whenever the metric is reused with a different model or framework.
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction. | ✗ The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing.
    leaderboard score n/a → 0.79461
- expert 27825577 (Expert) · amex · v4→v5   Implement the true evaluation metric as a custom callback/eval function and pass it to the training loop. When switching to a custom metric, substantially increase the early-stopping patience (e.g., 5× the previous value) because the custom metric may be noisier or converge differently than the defa
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction. | ✗ The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing.
    leaderboard score n/a → n/a
- expert 27825577 (Expert) · amex · v20→v25   Implement the custom metric as a standalone Python function that takes true labels and predictions, returns (metric_name, value). Pass it to the training API's custom-metric argument. Because wiring errors (wrong function name, wrong reference) are common, verify by running a short training loop and
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction. | ✓ The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v10→v11   Implement the competition's custom metric as a callback or custom evaluation function passed to the training API, so early stopping and model selection optimize for the true objective. At the same time, tune tree depth, row/column subsampling, and data-loading strategy to keep iteration fast.
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction. | ✓ The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing.
    leaderboard score n/a → n/a
- expert 27656049 (Expert) · amex · v16→v18   Try the custom metric as the eval function in one experiment and compare against the standard surrogate loss. If the score drops, revert to the surrogate loss for early stopping; the smooth loss often selects a better stopping point even when the final evaluation uses a different metric.
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction. | ✓ The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing. | ✓ The task metric fluctuates sharply between adjacent iterations while a smooth proxy is stable.
    leaderboard score 0.79171 → 0.79056 (-0.00115)
- expert 55431616 (Grandmaster) · learning · v22→v23   Explicitly set the early-stopping callback to reference the custom metric by name, enable the maximize flag, and turn on best-model saving so the checkpoint corresponds to the peak of the custom metric rather than the last iteration or the minimum of a loss.
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction. | ✗ The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing.
    leaderboard score n/a → n/a
- expert 60197293 (Expert) · learning · v7→v8   Write one metric function that inspects the type of its input (e.g., the dataset object) to detect which library is calling it, then branches to extract labels and return the result tuple in the format that library expects. Verify by running training with early stopping for both models.
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction. | ✗ The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing.
    leaderboard score n/a → 0.81867
- expert 60197293 (Expert) · learning · v55→v56   Explicitly specify the name or index of the validation evaluation set in the early-stopping callback configuration. Also suppress verbose per-iteration logging to keep output manageable during hyperparameter sweeps.
    evidence: ✓ The current callback differs from the official scoring function or uses the wrong direction.
    leaderboard score n/a → n/a
# Choose the early-stopping metric  `T.4.2.4`   7 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median -0.00115, 0 improved


- expert 27389424 · amex · v48→v49   Write a custom evaluation function in the format required by the training library's callback/feval interface, returning the competition metric computed on the validation fold. Pass it as the eval metric with early stopping. After switching to the custom metric, re-tune other hyperparameters (e.g., f
    evidence: ✓ The best epoch or iteration under the current stopping metric is not best under the target metric. | ✓ The current API obscures required probability output or evaluation controls.
    leaderboard score n/a → n/a (higher is better)
- expert 27389424 · amex · v54→v55   Switch from the high-level wrapper to the native training API so a custom evaluation function matching the competition metric can be passed as the early-stopping criterion. Verify that predictions are extracted consistently (e.g., raw scores vs. probabilities) after the API change.
    evidence: ✓ The best epoch or iteration under the current stopping metric is not best under the target metric. | ✓ The current API obscures required probability output or evaluation controls.
    leaderboard score n/a → n/a (higher is better)
- expert 27825577 · amex · v4→v5   Implement the true evaluation metric as a custom callback/eval function and pass it to the training loop. When switching to a custom metric, substantially increase the early-stopping patience (e.g., 5× the previous value) because the custom metric may be noisier or converge differently than the defa
    evidence: ✓ The current loss optimizes a surrogate that poorly tracks the held-out metric. | ✓ The best epoch or iteration under the current stopping metric is not best under the target metric. | ✓ The current API obscures required probability output or evaluation controls.
    leaderboard score n/a → n/a (higher is better)
- expert 27825577 · amex · v20→v25   Implement the custom metric as a standalone Python function that takes true labels and predictions, returns (metric_name, value). Pass it to the training API's custom-metric argument. Because wiring errors (wrong function name, wrong reference) are common, verify by running a short training loop and
    evidence: ✓ The best epoch or iteration under the current stopping metric is not best under the target metric. | ✓ The current API obscures required probability output or evaluation controls. | ✓ The current loss optimizes a surrogate that poorly tracks the held-out metric.
    leaderboard score n/a → n/a (higher is better)
- expert 28093671 · amex · v10→v11   Implement the competition's custom metric as a callback or custom evaluation function passed to the training API, so early stopping and model selection optimize for the true objective. At the same time, tune tree depth, row/column subsampling, and data-loading strategy to keep iteration fast.
    evidence: ✓ The best epoch or iteration under the current stopping metric is not best under the target metric. | ✓ The current API obscures required probability output or evaluation controls. | ✗ A known best value for the target-transform parameter exists from prior experiments and can serve as the baseline for further sweeps.
    leaderboard score n/a → n/a (higher is better)
- expert 28093671 · amex · v34→v37   When expanding features, switch the evaluation metric to a standard smooth proxy (e.g., AUC or log-loss) for more stable early stopping. Increase the learning rate moderately to speed up convergence, set a generous boosting-round budget, and rely on early stopping to find the right number of rounds.
    evidence: ✓ The best epoch or iteration under the current stopping metric is not best under the target metric.
    leaderboard score n/a → 0.79304 (higher is better)
- expert 27656049 · amex · v16→v18   Try the custom metric as the eval function in one experiment and compare against the standard surrogate loss. If the score drops, revert to the surrogate loss for early stopping; the smooth loss often selects a better stopping point even when the final evaluation uses a different metric.
    evidence: ✓ The best epoch or iteration under the current stopping metric is not best under the target metric. | ✗ Outcomes contain censoring or the metric evaluates risk ranking within known subgroups. | ✓ The current loss optimizes a surrogate that poorly tracks the held-out metric. | ✗ The current API obscures required probability output or evaluation controls. | ✓ A known best value for the target-transform parameter exists from prior experiments and can serve as the baseline for further sweeps.
    leaderboard score 0.79171 → 0.79056 (higher is better; worse by 0.00115)
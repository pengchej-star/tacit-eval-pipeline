# Use the target metric for model selection  `T.2.2.2`   13 edits, 0 experts
5 scored cases (improvement signed by each competition's direction), median -0.00015, 2 improved


- expert 27389424 · amex · v48→v49   Write a custom evaluation function in the format required by the training library's callback/feval interface, returning the competition metric computed on the validation fold. Pass it as the eval metric with early stopping. After switching to the custom metric, re-tune other hyperparameters (e.g., f
    evidence: ✓ Training selects checkpoints using a different objective direction or output convention from the task metric.
    leaderboard score n/a → n/a (higher is better)
- expert 27389424 · amex · v54→v55   Switch from the high-level wrapper to the native training API so a custom evaluation function matching the competition metric can be passed as the early-stopping criterion. Verify that predictions are extracted consistently (e.g., raw scores vs. probabilities) after the API change.
    evidence: ✓ Training selects checkpoints using a different objective direction or output convention from the task metric.
    leaderboard score n/a → n/a (higher is better)
- expert 27389424 · amex · v82→v85   Enable a fast debug mode to run the pipeline quickly, inspect the metric function call for correctness (especially that both labels and predictions are passed), fix any argument errors, and serialize per-fold predictions and indices to disk so they can be independently verified offline.
    evidence: ✓ Training selects checkpoints using a different objective direction or output convention from the task metric.
    leaderboard score n/a → n/a (higher is better)
- expert 27825577 · amex · v4→v5   Implement the true evaluation metric as a custom callback/eval function and pass it to the training loop. When switching to a custom metric, substantially increase the early-stopping patience (e.g., 5× the previous value) because the custom metric may be noisier or converge differently than the defa
    evidence: ✓ Training selects checkpoints using a different objective direction or output convention from the task metric.
    leaderboard score n/a → n/a (higher is better)
- expert 27825577 · amex · v20→v25   Implement the custom metric as a standalone Python function that takes true labels and predictions, returns (metric_name, value). Pass it to the training API's custom-metric argument. Because wiring errors (wrong function name, wrong reference) are common, verify by running a short training loop and
    evidence: ✓ Training selects checkpoints using a different objective direction or output convention from the task metric.
    leaderboard score n/a → n/a (higher is better)
- expert 28093671 · amex · v10→v11   Implement the competition's custom metric as a callback or custom evaluation function passed to the training API, so early stopping and model selection optimize for the true objective. At the same time, tune tree depth, row/column subsampling, and data-loading strategy to keep iteration fast.
    evidence: ✓ Training selects checkpoints using a different objective direction or output convention from the task metric.
    leaderboard score n/a → n/a (higher is better)
- expert 27656049 · amex · v16→v18   Try the custom metric as the eval function in one experiment and compare against the standard surrogate loss. If the score drops, revert to the surrogate loss for early stopping; the smooth loss often selects a better stopping point even when the final evaluation uses a different metric.
    evidence: ✓ Training selects checkpoints using a different objective direction or output convention from the task metric. | ✗ The task metric is too expensive to compute, limiting the number of evaluation trials or CV folds that can be run. | ✓ The exact task metric is unstable across epochs while a smooth surrogate tracks held-out generalization better.
    leaderboard score 0.79171 → 0.79056 (higher is better; worse by 0.00115)
- expert 73937748 · equity · v61→v62   Rewrite the metric computation using a JIT compiler with optimized data structures (e.g., a binary tree for rank queries). Verify that the new implementation produces numerically equivalent results on a held-out fold before replacing the original. Expect possible tiny score differences from floating
    evidence: ✓ The task metric is too expensive to compute, limiting the number of evaluation trials or CV folds that can be run.
    leaderboard score 0.69321 → 0.69306 (higher is better; worse by 0.00015)
- expert 55431616 · learning · v22→v23   Explicitly set the early-stopping callback to reference the custom metric by name, enable the maximize flag, and turn on best-model saving so the checkpoint corresponds to the peak of the custom metric rather than the last iteration or the minimum of a loss.
    evidence: ✓ Training selects checkpoints using a different objective direction or output convention from the task metric.
    leaderboard score n/a → n/a (higher is better)
- expert 60197293 · learning · v55→v56   Explicitly specify the name or index of the validation evaluation set in the early-stopping callback configuration. Also suppress verbose per-iteration logging to keep output manageable during hyperparameter sweeps.
    evidence: ✓ Training selects checkpoints using a different objective direction or output convention from the task metric.
    leaderboard score n/a → n/a (higher is better)
- expert 15082684 · ranzcr · v3→v14   Submit a handful of checkpoints spanning different runs and epochs to calibrate the CV-to-LB correlation. Be aware that the checkpoint with the highest validation score may not win on the public test set due to distribution shift or overfitting to the validation fold. If the first checkpoint already
    evidence: ✓ The exact task metric is unstable across epochs while a smooth surrogate tracks held-out generalization better.
    leaderboard score 0.96040 → 0.95388 (higher is better; worse by 0.00652)
- expert 15082684 · ranzcr · v14→v16   Track both validation and leaderboard scores across all submissions. When a checkpoint with notably higher validation still underperforms on the leaderboard, suspect a mismatch in preprocessing, augmentation, or data distribution rather than continuing to select checkpoints by validation alone. Inve
    evidence: ✓ Inference-time transforms (resolution, normalization, augmentation) differ from those used during training, causing a train/eval mismatch. | ✓ The exact task metric is unstable across epochs while a smooth surrogate tracks held-out generalization better. | ✗ The model's blend weight is small enough that individual overfitting has negligible impact on the ensemble prediction.
    leaderboard score 0.95388 → 0.95870 (higher is better; improved by 0.00482)
- expert 15082684 · ranzcr · v24→v29   Submit a small number of checkpoints spanning the range of validation scores to verify monotonic alignment between validation and test metrics. If two checkpoints with the same validation score from independent runs yield nearly identical test scores, treat validation as a reliable proxy and reduce 
    evidence: ✓ The exact task metric is unstable across epochs while a smooth surrogate tracks held-out generalization better.
    leaderboard score 0.96249 → 0.96901 (higher is better; improved by 0.00652)
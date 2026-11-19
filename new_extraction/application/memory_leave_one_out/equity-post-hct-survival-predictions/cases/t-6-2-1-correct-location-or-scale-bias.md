# Correct location or scale bias  `T.6.2.1`   9 edits, 0 experts
4 scored cases (improvement signed by each competition's direction), median -0.00218, 1 improved


- expert 18523075 · commonlitreadabilityprize · v16→v17   Try a dampened mean-shift correction (e.g., divide the offset by the number of ensemble components or a similar factor) rather than the full offset. If the dampened version still does not beat the uncorrected baseline on validation or leaderboard, remove the calibration entirely.
    evidence: ✓ Validation residuals show a systematic location or scale error. | ✗ Probability vectors are valid but classwise calibration is consistently biased. | ✓ The proposed correction risks overfitting to training-distribution statistics given the size or noise level of the test set.
    leaderboard score n/a → 0.45522 (lower is better)
- expert 17371717 · commonlitreadabilityprize · v24→v29   Select a reference example with minimal label uncertainty. At inference, run it through the same model and subtract its output from every other prediction. This removes additive bias that varies across folds or checkpoints, improving ensemble consistency. Ensure the reference tokens stay on the corr
    evidence: ✓ A zero-variance or otherwise stable reference sample exists that can anchor the bias correction. | ✓ Validation residuals show a systematic location or scale error. | ✗ Probability vectors are valid but classwise calibration is consistently biased. | ✓ The proposed correction risks overfitting to training-distribution statistics given the size or noise level of the test set.
    leaderboard score 0.46940 → 0.46114 (lower is better; improved by 0.00826)
- expert 6803050 · google · v2→v9   For a purely rank-based metric, submit the raw (unclipped, unscaled) predictions first as a baseline, since monotonic transforms cannot change ranks. Only add clipping or rescaling if the submission format requires bounded values or if post-processing (e.g., rounding to discrete levels) is applied a
    evidence: ✓ Raw model outputs may exceed the valid target range or hit exact boundaries. | ✗ Validation residuals show a systematic location or scale error.
    leaderboard score n/a → n/a (higher is better)
- expert 6803050 · google · v9→v10   Apply per-column min-max normalization so each column's predictions span [0,1]. This is a safe first baseline: it satisfies format constraints and preserves within-column ranks perfectly, which is all a rank-correlation metric needs.
    evidence: ✗ The proposed correction risks overfitting to training-distribution statistics given the size or noise level of the test set. | ✓ Raw model outputs may exceed the valid target range or hit exact boundaries.
    leaderboard score n/a → -0.00372 (higher is better)
- expert 6803050 · google · v24→v26   Avoid inserting additional normalization between the raw predictions and a quantile/rank-based calibration step, because altering the relative scale can shift values across quantile boundaries and destroy rank order. If tried, verify immediately and revert if the score drops.
    evidence: ✓ Raw model outputs may exceed the valid target range or hit exact boundaries. | ✓ The proposed correction risks overfitting to training-distribution statistics given the size or noise level of the test set.
    leaderboard score 0.37058 → 0.25892 (higher is better; worse by 0.11166)
- expert 6803050 · google · v26→v27   Remove the unnecessary normalization. Rank-based post-processing (quantile mapping) depends on the ordering of predictions, not their scale, so any rescaling that distorts relative ordering (e.g., adding constants, dividing by a per-fold max) can only hurt. Feed raw averaged outputs directly into th
    evidence: ✓ Validation residuals show a systematic location or scale error. | ✓ Raw model outputs may exceed the valid target range or hit exact boundaries.
    leaderboard score 0.25892 → n/a (higher is better)
- expert 55621328 · learning · v90→v91   After summing the sigmoid outputs, add the minimum label value as an offset so the predicted range matches the target range. Verify this alignment before applying any rounding or threshold optimization, as a mismatch will silently degrade the metric.
    evidence: ✓ Validation residuals show a systematic location or scale error. | ✗ The proposed correction risks overfitting to training-distribution statistics given the size or noise level of the test set. | ✓ Raw model outputs may exceed the valid target range or hit exact boundaries.
    leaderboard score n/a → n/a (higher is better)
- expert 55987255 · learning · v93→v95   Isolate the offset's effect by first removing it and fixing the bookkeeping so raw predictions are stored correctly, then re-introduce only the offset in a separate run. Compare leaderboard scores to determine whether the offset helps. If the score drops with the offset, remove it permanently.
    evidence: ✓ Validation residuals show a systematic location or scale error. | ✓ Raw model outputs may exceed the valid target range or hit exact boundaries. | ✓ The proposed correction risks overfitting to training-distribution statistics given the size or noise level of the test set.
    leaderboard score 0.81675 → 0.81457 (higher is better; worse by 0.00218)
- expert 15173072 · ranzcr · v14→v20   Once the correct order of magnitude for prediction scaling is found (evidenced by a large score jump), further fine-tuning the multiplier yields diminishing or negative returns for a rank-based metric like AUC, because AUC depends on ranking, not absolute values. Lock in the working scale factor and
    evidence: ✓ Raw model outputs may exceed the valid target range or hit exact boundaries. | ✓ Validation residuals show a systematic location or scale error.
    leaderboard score 0.96062 → 0.95319 (higher is better; worse by 0.00742)
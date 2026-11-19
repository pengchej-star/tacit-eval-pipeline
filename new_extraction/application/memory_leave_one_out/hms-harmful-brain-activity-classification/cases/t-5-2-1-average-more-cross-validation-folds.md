# Average more cross-validation folds  `T.5.2.1`   26 edits, 0 experts
19 scored cases (improvement signed by each competition's direction), median +0.00076, 15 improved


- expert 28984551 · amex · v4→v6   When exploring, change only one lever at a time—model type OR fold count OR learning rate—so that the effect of each can be isolated. If multiple changes are made simultaneously and the result is ambiguous, revert to the last known best and vary one factor to establish its individual contribution.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.78926 → 0.78979 (higher is better; improved by 0.00053)
- expert 27799930 · amex · v16→v24   Persist each fold model to disk immediately after training. At inference time, load every fold model, generate predicted probabilities on the same test features, and average the probabilities across all folds. Merge the averaged predictions with the submission template and write the output file.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score n/a → 0.78812 (higher is better)
- expert 27799930 · amex · v53→v55   Try a small range of fold counts (e.g., 5, 7, 10) and compare public leaderboard or held-out scores. Prefer the higher fold count if it scores better, since each fold model sees more data and the averaged prediction is smoother.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score n/a → 0.79342 (higher is better)
- expert 27799930 · amex · v67→v69   Try a small range of fold counts (e.g., 5–10) and compare leaderboard or validation scores. A moderate fold count that keeps each fold's training set large enough while providing sufficient ensemble members often works best. If reducing folds hurts, revert promptly rather than continuing to tune oth
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage. | ✓ Predictions vary across trained seeds beyond the expected evaluation noise. | ✗ Dropout is active or intentionally proposed at inference and creates nontrivial prediction variance.
    leaderboard score n/a → 0.79475 (higher is better)
- expert 27799930 · amex · v73→v74   Treat the number of folds and seeds as low-cost hyperparameters to search over. Increase one at a time, verify on the leaderboard or a stable local metric, and keep the configuration that improves the score. If adding a seed or fold does not help, revert. Avoid assuming more is always better.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage. | ✓ Predictions vary across trained seeds beyond the expected evaluation noise.
    leaderboard score n/a → n/a (higher is better)
- expert 17616127 · commonlitreadabilityprize · v38→v43   Add folds one at a time and measure the target metric after each addition. Track the marginal improvement per fold. Stop when the gain drops below a small threshold relative to earlier gains (e.g., an order of magnitude smaller than the first fold's contribution), as further additions are unlikely t
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.46554 → 0.45414 (lower is better; improved by 0.01140)
- expert 17616127 · commonlitreadabilityprize · v75→v78   Try adding more folds from each model family one group at a time and submit. If the metric does not improve (or worsens), the original smaller blend likely already captured the diversity benefit; additional folds add redundancy rather than complementary signal. Stop expanding when two consecutive ad
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage. | ✓ Several stopping-rule or training-stage snapshots have complementary errors.
    leaderboard score 0.45173 → 0.45174 (lower is better; worse by 0.00000)
- expert 17616127 · commonlitreadabilityprize · v80→v81   Test a single-fold weighted combination against the multi-fold average. Expect the multi-fold average to win because averaging across folds reduces variance, especially when the test set is small and noisy. Revert if the single-fold approach scores worse.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.45266 → 0.45684 (lower is better; worse by 0.00419)
- expert 17616127 · commonlitreadabilityprize · v140→v141   Default to returning the averaged prediction across folds for the final submission unless there is a downstream blending step that specifically benefits from per-fold granularity. The averaged output is more robust and avoids accidental mishandling of per-fold arrays.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score n/a → 0.44790 (lower is better)
- expert 73937748 · equity · v46→v48   Always divide the accumulated test predictions by the number of folds to produce a proper average. Verify this by checking that the scale of out-of-fold and test predictions is comparable. A mismatch in aggregation logic is a common silent bug that degrades ensemble scores.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.69140 → 0.69172 (higher is better; improved by 0.00032)
- expert 7613444 · google · v11→v12   Ensure every trained fold model is loaded and included in the test-time average. Verify that checkpoint file paths match the actual saved names (e.g., via a print/log statement). Going from a partial to a full fold ensemble typically yields a small but consistent gain because averaging more diverse 
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.39956 → 0.40047 (higher is better; improved by 0.00091)
- expert 6803050 · google · v18→v19   Load each fold's checkpoint independently, run full inference on the test set with each, then average the resulting prediction arrays element-wise. This simple mean ensemble reduces variance from individual fold training randomness.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score -0.00372 → -0.00372 (higher is better; unchanged by 0.00000)
- expert 6803050 · google · v21→v23   Ablate by submitting a single fold's predictions alone, then compare against the full ensemble. This isolates the ensemble's contribution. If the gap is large, keep the ensemble; the magnitude also indicates how much variance reduction matters for the metric.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.36763 → 0.38182 (higher is better; improved by 0.01419)
- expert 7253130 · google · v11→v12   Increase the number of CV folds (e.g., by 50%) so that more independently trained models contribute to the averaged prediction. This reduces variance at the cost of longer training time. Verify the improvement on the leaderboard; if the gain is meaningful, keep the higher fold count.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.37532 → 0.38610 (higher is better; improved by 0.01078)
- expert 60264017 · learning · v13→v14   Build an inference routine that loads every available checkpoint, runs each on the test data, and averages their outputs. Optionally fit a scaler (e.g., min-max) on out-of-fold predictions to align the averaged output's range with the target distribution before feeding it into the downstream ensembl
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.82848 → n/a (higher is better)
- expert 55621328 · learning · v12→v14   Load all fold checkpoints and average their predictions before applying any post-processing (e.g., threshold rounding). This reduces variance and typically improves ranking metrics without retraining. Prefer the model size that already performed best on the leaderboard.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.80219 → 0.80527 (higher is better; improved by 0.00308)
- expert 55621328 · learning · v53→v55   Test multi-fold averaging against the single best fold on the leaderboard. If multi-fold scores lower, revert to the single best fold and only use multi-fold when each fold's individual score is competitive. Do not assume more folds always help.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.81104 → 0.81742 (higher is better; improved by 0.00638)
- expert 55621328 · learning · v78→v80   Try replacing the single-fold checkpoint with a multi-fold ensemble (all folds averaged) from the same or a related experiment, adjusting blend weights accordingly. Multi-fold averaging typically reduces variance and outperforms any single fold. If a pseudo-labeled single checkpoint does not beat th
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.82461 → 0.82504 (higher is better; improved by 0.00043)
- expert 58130512 · learning · v87→v91   Compare a nested CV (fewer outer folds × inner folds) against a flat CV with a larger number of folds. If the ensemble benefits from having many diverse models and the metric doesn't improve with nested validation, prefer the simpler flat scheme with many folds. Verify by submitting both configurati
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.82230 → 0.82432 (higher is better; improved by 0.00202)
- expert 58130512 · learning · v91→v96   Run a small grid of changes—fold count, ensemble weighting vs. simple averaging, embedding dimensionality, feature-selection cutoff, and tree depth—each submitted independently. If every variant scores worse than the baseline, accept that these levers are exhausted at the current configuration and r
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.82432 → 0.81933 (higher is better; worse by 0.00498)
- expert 60197293 · learning · v29→v35   Try increasing the fold count substantially (e.g., 5→30). If the score does not improve or degrades, the validation sets are likely too small for reliable early stopping or the additional folds add noise. Revert to a moderate count (e.g., 10) that keeps validation sets large enough for stable early-
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score n/a → 0.81788 (higher is better)
- expert 55591012 · learning · v9→v10   Increase the fold count substantially (e.g., triple it) so each fold trains on a larger share of data and OOF predictions become more stable. Expect a small but real gain on metrics sensitive to prediction calibration, at the cost of proportionally longer training time.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.81083 → 0.81126 (higher is better; improved by 0.00043)
- expert 55591012 · learning · v48→v50   Average the predictions (softmax or logits) of all available transformer checkpoints before blending with the tree models. This reduces variance of the neural component and typically yields a small but consistent metric gain without any retraining.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.82007 → 0.82075 (higher is better; improved by 0.00068)
- expert 15082684 · ranzcr · v18→v22   Average predictions across fold checkpoints at inference. Ensure the model architecture flag and head configuration exactly match what was used during training of those checkpoints; a mismatch silently degrades results. Verify by comparing the ensemble score against the single-checkpoint baseline.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.96509 → 0.96591 (higher is better; improved by 0.00082)
- expert 15372370 · ranzcr · v6→v7   Switch to simple (equal-weight) averaging of predictions across all folds of a single cross-validation run. Fold-averaging is more stable because the models share the same architecture and training recipe, reducing the risk of miscalibrated blend weights.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage. | ✓ The task is invariant to candidate transformations and predictions vary across those views.
    leaderboard score 0.96670 → 0.96804 (higher is better; improved by 0.00135)
- expert 15164527 · ranzcr · v5→v6   For each model in the ensemble, run inference with every fold's checkpoint and average their predictions before blending across models. This reduces variance in each model's contribution and typically yields a small but consistent metric gain.
    evidence: ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.96679 → 0.96755 (higher is better; improved by 0.00076)
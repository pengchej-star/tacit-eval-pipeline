# Select and average fold checkpoints  `T.7.3.1`   43 edits, 0 experts
33 scored cases, median improvement -0.00004, 15 improved


- expert 27799930 (Contributor) · amex · v16→v24   Persist each fold model to disk immediately after training. At inference time, load every fold model, generate predicted probabilities on the same test features, and average the probabilities across all folds. Merge the averaged predictions with the submission template and write the output file.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✗ The model has usable stochastic layers and repeated inference is intended to sample them. | ✗ Stochastic layers are active at inference without a validated repeated-pass strategy. | ✗ Several compatible training snapshots of one model are available for weight averaging.
    leaderboard score n/a → 0.78812
- expert 27799930 (Contributor) · amex · v53→v55   Try a small range of fold counts (e.g., 5, 7, 10) and compare public leaderboard or held-out scores. Prefer the higher fold count if it scores better, since each fold model sees more data and the averaged prediction is smoother.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✗ The model has usable stochastic layers and repeated inference is intended to sample them. | ✗ Stochastic layers are active at inference without a validated repeated-pass strategy. | ✗ Several compatible training snapshots of one model are available for weight averaging.
    leaderboard score n/a → 0.79342
- expert 27799930 (Contributor) · amex · v67→v69   Try a small range of fold counts (e.g., 5–10) and compare leaderboard or validation scores. A moderate fold count that keeps each fold's training set large enough while providing sufficient ensemble members often works best. If reducing folds hurts, revert promptly rather than continuing to tune oth
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Independent training seeds produce materially different errors. | ✗ The model has usable stochastic layers and repeated inference is intended to sample them. | ✗ Stochastic layers are active at inference without a validated repeated-pass strategy.
    leaderboard score n/a → 0.79475
- expert 27799930 (Contributor) · amex · v73→v74   Treat the number of folds and seeds as low-cost hyperparameters to search over. Increase one at a time, verify on the leaderboard or a stable local metric, and keep the configuration that improves the score. If adding a seed or fold does not help, revert. Avoid assuming more is always better.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Independent training seeds produce materially different errors. | ✗ The model has usable stochastic layers and repeated inference is intended to sample them. | ✗ Stochastic layers are active at inference without a validated repeated-pass strategy.
    leaderboard score n/a → n/a
- expert 27656049 (Expert) · amex · v7→v8   Switch to stratified k-fold CV (e.g., 10 folds) to preserve class proportions in each fold. Train one model per fold and average their predicted probabilities on the test set. When increasing the number of folds, consider reducing per-model capacity (fewer boosting rounds or leaves) to keep total tr
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score n/a → 0.78584
- expert 17616127 (Contributor) · commonlitreadabilityprize · v38→v43   Add folds one at a time and measure the target metric after each addition. Track the marginal improvement per fold. Stop when the gain drops below a small threshold relative to earlier gains (e.g., an order of magnitude smaller than the first fold's contribution), as further additions are unlikely t
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.46554 → 0.45414 (-0.01140)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v80→v81   Test a single-fold weighted combination against the multi-fold average. Expect the multi-fold average to win because averaging across folds reduces variance, especially when the test set is small and noisy. Revert if the single-fold approach scores worse.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.45266 → 0.45684 (+0.00419)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v92→v98   Treat fold inclusion as a discrete search variable: toggle each fold in/out, evaluate on the held-out metric, and keep the subset that scores best. Start by removing any fold that causes errors or is suspected weak, then try adding it back to confirm the effect.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.45486 → 0.45076 (-0.00410)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v140→v141   Default to returning the averaged prediction across folds for the final submission unless there is a downstream blending step that specifically benefits from per-fold granularity. The averaged output is more robust and avoids accidental mishandling of per-fold arrays.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score n/a → 0.44790
- expert 18426209 (Expert) · commonlitreadabilityprize · v8→v9   Replace automatic checkpoint discovery with an explicit list of checkpoint paths. Annotate each with its known validation score. This makes the ensemble deterministic and allows selective exclusion of weak folds. Verify the effect by submitting and comparing against the previous score.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.45918 → 0.45856 (-0.00062)
- expert 18350823 (Expert) · commonlitreadabilityprize · v2→v4   Before increasing the number of folds in the ensemble, verify that a trained checkpoint exists for every fold index and that each fold's random seed and data split are correctly assigned. Test the expanded ensemble and revert if the score worsens, as the issue is likely infrastructure (missing or mi
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Stochastic layers are active at inference without a validated repeated-pass strategy.
    leaderboard score 0.46275 → 0.46448 (+0.00173)
- expert 17371717 (Master) · commonlitreadabilityprize · v29→v30   Compare the ensemble of all fold checkpoints against the single best fold checkpoint. Expect the multi-fold ensemble to be substantially better due to variance reduction; revert to the ensemble if the single checkpoint degrades the score.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Independent training seeds produce materially different errors. | ✓ Several compatible training snapshots of one model are available for weight averaging.
    leaderboard score 0.46114 → 0.47074 (+0.00960)
- expert 7573212 (Contributor) · google · v5→v7   Be cautious: dropping folds from a K-fold ensemble usually hurts because it reduces the effective training data and increases variance. If no local validation metric guides fold weighting, prefer equal-weight averaging. Leaderboard probing of fold subsets is unreliable due to noise and risks overfit
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✗ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.38598 → 0.37898 (-0.00700)
- expert 6803050 (Master) · google · v21→v23   Ablate by submitting a single fold's predictions alone, then compare against the full ensemble. This isolates the ensemble's contribution. If the gap is large, keep the ensemble; the magnitude also indicates how much variance reduction matters for the metric.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.36763 → 0.38182 (+0.01419)
- expert 73671444 (Grandmaster) · equity · v1→v3   Probe by submitting predictions from (a) only fold models, (b) only full-data models, and (c) all models combined. If the score differences are negligible (on the order of noise), conclude that checkpoint selection is not a productive lever and move on to other changes such as model architecture or 
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.66986 → 0.66983 (-0.00004)
- expert 77347591 (Expert) · equity · v5→v7   Increase the number of CV folds (e.g., double them) to reduce variance in OOF predictions, and simultaneously increase early-stopping patience substantially (e.g., more than double) so models train closer to their optimum before stopping. Combine this with hyperparameter re-tuning since the changed 
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✗ The model has usable stochastic layers and repeated inference is intended to sample them. | ✗ Stochastic layers are active at inference without a validated repeated-pass strategy.
    leaderboard score 0.69346 → n/a
- expert 73937748 (Master) · equity · v5→v6   Halve the number of CV folds (e.g., 10 → 5) and measure the leaderboard or holdout impact. If the drop is small (on the order of noise), keep the lower fold count to accelerate experimentation, expecting that later improvements will more than compensate. Revert to more folds for a final submission i
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✗ The model has usable stochastic layers and repeated inference is intended to sample them. | ✗ Stochastic layers are active at inference without a validated repeated-pass strategy.
    leaderboard score 0.68705 → 0.68648 (-0.00057)
- expert 73937748 (Master) · equity · v46→v48   Always divide the accumulated test predictions by the number of folds to produce a proper average. Verify this by checking that the scale of out-of-fold and test predictions is comparable. A mismatch in aggregation logic is a common silent bug that degrades ensemble scores.
    evidence: none recorded
    leaderboard score 0.69140 → 0.69172 (+0.00032)
- expert 7613444 (Contributor) · google · v11→v12   Ensure every trained fold model is loaded and included in the test-time average. Verify that checkpoint file paths match the actual saved names (e.g., via a print/log statement). Going from a partial to a full fold ensemble typically yields a small but consistent gain because averaging more diverse 
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.39956 → 0.40047 (+0.00091)
- expert 6803050 (Master) · google · v18→v19   Load each fold's checkpoint independently, run full inference on the test set with each, then average the resulting prediction arrays element-wise. This simple mean ensemble reduces variance from individual fold training randomness.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score -0.00372 → -0.00372 (+0.00000)
- expert 7253130 (Contributor) · google · v11→v12   Increase the number of CV folds (e.g., by 50%) so that more independently trained models contribute to the averaged prediction. This reduces variance at the cost of longer training time. Verify the improvement on the leaderboard; if the gain is meaningful, keep the higher fold count.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.37532 → 0.38610 (+0.01078)
- expert 7606235 (Master) · google · v15→v23   Test small ensembles (2–3 checkpoints) against the best single checkpoint on the leaderboard. If the ensemble consistently scores below the best single checkpoint, the weaker folds are adding noise that hurts ranking quality. In that case, keep the single best checkpoint rather than averaging, or tr
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence. | ✓ Several compatible training snapshots of one model are available for weight averaging.
    leaderboard score 0.38524 → 0.38785 (+0.00261)
- expert 49576186 (Expert) · hms · v105→v107   Remove dead code and unused dependencies to reduce noise, add robustness measures like early stopping and averaging predictions across cross-validation folds, and re-submit. Fold averaging smooths out variance and can partially compensate for a suboptimal single-fold configuration.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.28170 → 0.27969 (-0.00201)
- expert 50376011 (Grandmaster) · hms · v31→v37   Build a loop that loads each fold's saved weights into the same architecture, runs inference on the test set, and averages (or weighted-averages) the resulting predictions across all folds before producing the final submission. This reduces variance from any single fold's idiosyncrasies.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Several compatible training snapshots of one model are available for weight averaging. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.39254 → 0.35548 (-0.03706)
- expert 50376011 (Grandmaster) · hms · v55→v57   Remove the explicit fold restriction and let the inference script average over all available fold checkpoints. If the first submission shows a small regression, re-run before concluding the change is harmful, since leaderboard noise can mask small improvements.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.34467 → 0.34376 (-0.00091)
- expert 50376011 (Grandmaster) · hms · v93→v94   Systematically increase the number of ensemble members (e.g., from 1 to 6 folds) with uniform weights. When the metric rewards calibration (e.g., KL divergence), averaging over more diverse folds tends to yield a substantial improvement. After finding the gain, verify by comparing back to fewer memb
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.33490 → 0.31316 (-0.02174)
- expert 50376011 (Grandmaster) · hms · v126→v142   Sweep individual checkpoints first to rank them by solo performance, then try small ensembles of the top-performing members. Re-submit the same configuration multiple times to estimate submission variance before concluding one config beats another. Only trust improvements that exceed the observed no
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.27192 → 0.26480 (-0.00712)
- expert 50376011 (Grandmaster) · hms · v190→v191   Incrementally add more fold checkpoints to the ensemble (e.g., double the count). If the metric improves, keep the larger set. Then try swapping individual members one at a time to fine-tune composition. Stop expanding when adding more members no longer helps or degrades the score.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.24878 → 0.23917 (-0.00961)
- expert 50376011 (Grandmaster) · hms · v213→v218   Incrementally increase the number of fold predictions averaged at inference and monitor the evaluation metric. Averaging more folds typically reduces prediction variance and improves calibration. Continue adding folds as long as the metric improves and inference time/memory permits.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.25121 → 0.24408 (-0.00712)
- expert 50376011 (Grandmaster) · hms · v237→v251   Incrementally add checkpoints to the ensemble, submitting after each addition. When the improvement from adding one more member falls within the noise floor, stop. If runtime is the binding constraint, reduce per-sample processing cost (e.g., smaller batch counts or fewer augmentation passes) to fit
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.23496 → n/a
- expert 50376011 (Grandmaster) · hms · v252→v254   Add checkpoints incrementally, submitting after each addition. Track the marginal improvement per added member. Continue adding until the marginal gain becomes negligible or turns negative, then stop at the best count.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.22970 → 0.22640 (-0.00331)
- expert 55621328 (Master) · learning · v93→v94   Isolate and evaluate individual alternative folds. If they score substantially lower than the best fold, the performance gap confirms that the best fold is unusually well-aligned with the test distribution, and the ensemble is diluted by weaker folds. Keep the best single fold rather than averaging.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.82276 → 0.81721 (-0.00555)
- expert 55621328 (Master) · learning · v12→v14   Load all fold checkpoints and average their predictions before applying any post-processing (e.g., threshold rounding). This reduces variance and typically improves ranking metrics without retraining. Prefer the model size that already performed best on the leaderboard.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.80219 → 0.80527 (+0.00308)
- expert 55621328 (Master) · learning · v53→v55   Test multi-fold averaging against the single best fold on the leaderboard. If multi-fold scores lower, revert to the single best fold and only use multi-fold when each fold's individual score is competitive. Do not assume more folds always help.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Independent training seeds produce materially different errors. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.81104 → 0.81742 (+0.00638)
- expert 55621328 (Master) · learning · v78→v80   Try replacing the single-fold checkpoint with a multi-fold ensemble (all folds averaged) from the same or a related experiment, adjusting blend weights accordingly. Multi-fold averaging typically reduces variance and outperforms any single fold. If a pseudo-labeled single checkpoint does not beat th
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.82461 → 0.82504 (+0.00043)
- expert 55621328 (Master) · learning · v92→v94   Test the multi-fold ensemble against the single best fold on the leaderboard. If the multi-fold average scores lower, the individual fold may have been better calibrated to the test distribution; revert to the single fold. Also test individual alternative folds to check whether the gain was fold-spe
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.82736 → 0.81721 (-0.01015)
- expert 58130512 (Master) · learning · v87→v91   Compare a nested CV (fewer outer folds × inner folds) against a flat CV with a larger number of folds. If the ensemble benefits from having many diverse models and the metric doesn't improve with nested validation, prefer the simpler flat scheme with many folds. Verify by submitting both configurati
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.82230 → 0.82432 (+0.00202)
- expert 60197293 (Expert) · learning · v29→v35   Try increasing the fold count substantially (e.g., 5→30). If the score does not improve or degrades, the validation sets are likely too small for reliable early stopping or the additional folds add noise. Revert to a moderate count (e.g., 10) that keeps validation sets large enough for stable early-
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✗ The model has usable stochastic layers and repeated inference is intended to sample them. | ✗ Stochastic layers are active at inference without a validated repeated-pass strategy.
    leaderboard score n/a → 0.81788
- expert 55987255 (Master) · learning · v37→v38   Before removing debug shortcuts, recognize that a single-fold prediction can sometimes outscore a full cross-validation ensemble if the single fold's data distribution better matches the test set or if averaging introduces noise from weaker folds. Compare per-fold OOF scores to diagnose whether spec
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.81943 → 0.81711 (-0.00232)
- expert 55591012 (Grandmaster) · learning · v9→v10   Increase the fold count substantially (e.g., triple it) so each fold trains on a larger share of data and OOF predictions become more stable. Expect a small but real gain on metrics sensitive to prediction calibration, at the cost of proportionally longer training time.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.81083 → 0.81126 (+0.00043)
- expert 55591012 (Grandmaster) · learning · v37→v39   Test a modest increase in fold count (e.g., +30–50%) and compare leaderboard or holdout scores. If the score drops, revert. Avoid changing fold count simultaneously with other hyperparameters so the effect is identifiable. Prefer the fold count that balances per-fold training set size with ensemble 
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Several compatible training snapshots of one model are available for weight averaging.
    leaderboard score 0.81990 → 0.81998 (+0.00008)
- expert 55591012 (Grandmaster) · learning · v48→v50   Average the predictions (softmax or logits) of all available transformer checkpoints before blending with the tree models. This reduces variance of the neural component and typically yields a small but consistent metric gain without any retraining.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.82007 → 0.82075 (+0.00068)
- expert 50496431 (Grandmaster) · hms · v1→v5   Loop over all fold checkpoint files, load each model's weights, run inference on the test set collecting predictions per fold, then average the per-fold prediction arrays element-wise. Ensure the dataset class returns only inputs (no labels) during inference and that the data loader yields the expec
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score n/a → 0.42903
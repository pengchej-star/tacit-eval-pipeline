# Select and average fold checkpoints  `T.6.2.1`   41 edits, 0 experts
35 scored cases, median improvement -0.00004, 17 improved


- expert 27799930 (Contributor) · amex · v16→v24   Persist each fold model to disk immediately after training. At inference time, load every fold model, generate predicted probabilities on the same test features, and average the probabilities across all folds. Merge the averaged predictions with the submission template and write the output file.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Dropout or other random inference operations are active or being proposed. | ✓ Repeated forward passes with the same weights and inputs are numerically identical. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score n/a → 0.78812
- expert 27799930 (Contributor) · amex · v67→v69   Try a small range of fold counts (e.g., 5–10) and compare leaderboard or validation scores. A moderate fold count that keeps each fold's training set large enough while providing sufficient ensemble members often works best. If reducing folds hurts, revert promptly rather than continuing to tune oth
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score n/a → 0.79475
- expert 27656049 (Expert) · amex · v7→v8   Switch to stratified k-fold CV (e.g., 10 folds) to preserve class proportions in each fold. Train one model per fold and average their predicted probabilities on the test set. When increasing the number of folds, consider reducing per-model capacity (fewer boosting rounds or leaves) to keep total tr
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score n/a → 0.78584
- expert 17616127 (Contributor) · commonlitreadabilityprize · v38→v43   Add folds one at a time and measure the target metric after each addition. Track the marginal improvement per fold. Stop when the gain drops below a small threshold relative to earlier gains (e.g., an order of magnitude smaller than the first fold's contribution), as further additions are unlikely t
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.46554 → 0.45414 (-0.01140)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v75→v78   Try adding more folds from each model family one group at a time and submit. If the metric does not improve (or worsens), the original smaller blend likely already captured the diversity benefit; additional folds add redundancy rather than complementary signal. Stop expanding when two consecutive ad
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.45173 → 0.45174 (+0.00000)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v80→v81   Test a single-fold weighted combination against the multi-fold average. Expect the multi-fold average to win because averaging across folds reduces variance, especially when the test set is small and noisy. Revert if the single-fold approach scores worse.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.45266 → 0.45684 (+0.00419)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v81→v85   For each fold, compute a weighted combination of the different models' predictions for that fold, then average the fold-level blended predictions with equal weight (1/number-of-folds). This preserves fold-specific signal diversity and can outperform a single global weighted average.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.45684 → 0.45142 (-0.00542)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v92→v98   Treat fold inclusion as a discrete search variable: toggle each fold in/out, evaluate on the held-out metric, and keep the subset that scores best. Start by removing any fold that causes errors or is suspected weak, then try adding it back to confirm the effect.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.45486 → 0.45076 (-0.00410)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v140→v141   Default to returning the averaged prediction across folds for the final submission unless there is a downstream blending step that specifically benefits from per-fold granularity. The averaged output is more robust and avoids accidental mishandling of per-fold arrays.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score n/a → 0.44790
- expert 18426209 (Expert) · commonlitreadabilityprize · v8→v9   Replace automatic checkpoint discovery with an explicit list of checkpoint paths. Annotate each with its known validation score. This makes the ensemble deterministic and allows selective exclusion of weak folds. Verify the effect by submitting and comparing against the previous score.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.45918 → 0.45856 (-0.00062)
- expert 18350823 (Expert) · commonlitreadabilityprize · v2→v4   Before increasing the number of folds in the ensemble, verify that a trained checkpoint exists for every fold index and that each fold's random seed and data split are correctly assigned. Test the expanded ensemble and revert if the score worsens, as the issue is likely infrastructure (missing or mi
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✓ Dropout or other random inference operations are active or being proposed. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.46275 → 0.46448 (+0.00173)
- expert 17371717 (Master) · commonlitreadabilityprize · v29→v30   Compare the ensemble of all fold checkpoints against the single best fold checkpoint. Expect the multi-fold ensemble to be substantially better due to variance reduction; revert to the ensemble if the single checkpoint degrades the score.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.46114 → 0.47074 (+0.00960)
- expert 73671444 (Grandmaster) · equity · v1→v3   Probe by submitting predictions from (a) only fold models, (b) only full-data models, and (c) all models combined. If the score differences are negligible (on the order of noise), conclude that checkpoint selection is not a productive lever and move on to other changes such as model architecture or 
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.66986 → 0.66983 (-0.00004)
- expert 73937748 (Master) · equity · v46→v48   Always divide the accumulated test predictions by the number of folds to produce a proper average. Verify this by checking that the scale of out-of-fold and test predictions is comparable. A mismatch in aggregation logic is a common silent bug that degrades ensemble scores.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.69140 → 0.69172 (+0.00032)
- expert 53424936 (Master) · hms · v5→v8   Add the new branch's checkpoints incrementally to the equal-weight ensemble average, submitting after each addition. This isolates the contribution of each new member and confirms diminishing-returns behavior. Continue adding folds until all available checkpoints are included or gains plateau.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.22872 → 0.22803 (-0.00069)
- expert 50376011 (Grandmaster) · hms · v31→v37   Build a loop that loads each fold's saved weights into the same architecture, runs inference on the test set, and averages (or weighted-averages) the resulting predictions across all folds before producing the final submission. This reduces variance from any single fold's idiosyncrasies.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts. | ✗ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.39254 → 0.35548 (-0.03706)
- expert 50376011 (Grandmaster) · hms · v55→v57   Remove the explicit fold restriction and let the inference script average over all available fold checkpoints. If the first submission shows a small regression, re-run before concluding the change is harmful, since leaderboard noise can mask small improvements.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.34467 → 0.34376 (-0.00091)
- expert 50376011 (Grandmaster) · hms · v93→v94   Systematically increase the number of ensemble members (e.g., from 1 to 6 folds) with uniform weights. When the metric rewards calibration (e.g., KL divergence), averaging over more diverse folds tends to yield a substantial improvement. After finding the gain, verify by comparing back to fewer memb
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.33490 → 0.31316 (-0.02174)
- expert 50376011 (Grandmaster) · hms · v126→v142   Sweep individual checkpoints first to rank them by solo performance, then try small ensembles of the top-performing members. Re-submit the same configuration multiple times to estimate submission variance before concluding one config beats another. Only trust improvements that exceed the observed no
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts. | ✗ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.27192 → 0.26480 (-0.00712)
- expert 50376011 (Grandmaster) · hms · v184→v188   Test each candidate checkpoint individually and in small combinations, submitting multiple times for the same config when feasible. Prefer combinations that consistently score well across runs over single-run winners. Start with the best individual members, then add members incrementally; if adding 
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Repeated forward passes with the same weights and inputs are numerically identical. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.24841 → 0.24815 (-0.00026)
- expert 50376011 (Grandmaster) · hms · v190→v191   Incrementally add more fold checkpoints to the ensemble (e.g., double the count). If the metric improves, keep the larger set. Then try swapping individual members one at a time to fine-tune composition. Stop expanding when adding more members no longer helps or degrades the score.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Repeated forward passes with the same weights and inputs are numerically identical. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.24878 → 0.23917 (-0.00961)
- expert 50376011 (Grandmaster) · hms · v192→v199   Run a systematic single-checkpoint sweep: submit each fold checkpoint alone, record its standalone score, then rank them. Use these rankings to select the top-performing members for the final ensemble and drop weak ones. Expect that no single checkpoint will beat a well-chosen ensemble, but the swee
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts. | ✓ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.23903 → 0.24449 (+0.00546)
- expert 50376011 (Grandmaster) · hms · v213→v218   Incrementally increase the number of fold predictions averaged at inference and monitor the evaluation metric. Averaging more folds typically reduces prediction variance and improves calibration. Continue adding folds as long as the metric improves and inference time/memory permits.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Repeated forward passes with the same weights and inputs are numerically identical. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.25121 → 0.24408 (-0.00712)
- expert 49576186 (Expert) · hms · v20→v22   Average the predicted probability distributions from all fold models for each test sample. This reduces prediction variance and typically improves calibration, yielding a better score on distribution-matching metrics like KL divergence.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused.
    leaderboard score 0.41352 → 0.36216 (-0.05135)
- expert 55621328 (Master) · learning · v12→v14   Load all fold checkpoints and average their predictions before applying any post-processing (e.g., threshold rounding). This reduces variance and typically improves ranking metrics without retraining. Prefer the model size that already performed best on the leaderboard.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.80219 → 0.80527 (+0.00308)
- expert 55621328 (Master) · learning · v37→v45   First sweep individual checkpoints one at a time to identify the strongest single variant. Then expand the ensemble by adding all folds of that variant. Finally, add checkpoints from different random seeds of the same variant. At each step, submit and keep the change only if the metric improves; rev
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.81536 → 0.81599 (+0.00063)
- expert 55621328 (Master) · learning · v53→v55   Test multi-fold averaging against the single best fold on the leaderboard. If multi-fold scores lower, revert to the single best fold and only use multi-fold when each fold's individual score is competitive. Do not assume more folds always help.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts. | ✓ Independent training seeds produce materially different errors.
    leaderboard score 0.81104 → 0.81742 (+0.00638)
- expert 55621328 (Master) · learning · v78→v80   Try replacing the single-fold checkpoint with a multi-fold ensemble (all folds averaged) from the same or a related experiment, adjusting blend weights accordingly. Multi-fold averaging typically reduces variance and outperforms any single fold. If a pseudo-labeled single checkpoint does not beat th
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.82461 → 0.82504 (+0.00043)
- expert 55621328 (Master) · learning · v92→v94   Test the multi-fold ensemble against the single best fold on the leaderboard. If the multi-fold average scores lower, the individual fold may have been better calibrated to the test distribution; revert to the single fold. Also test individual alternative folds to check whether the gain was fold-spe
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.82736 → 0.81721 (-0.01015)
- expert 55621328 (Master) · learning · v93→v94   Isolate and evaluate individual alternative folds. If they score substantially lower than the best fold, the performance gap confirms that the best fold is unusually well-aligned with the test distribution, and the ensemble is diluted by weaker folds. Keep the best single fold rather than averaging.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.82276 → 0.81721 (-0.00555)
- expert 55621328 (Master) · learning · v113→v114   Add full-data checkpoints alongside fold checkpoints in the ensemble, adjusting blend weights to account for the new members. Evaluate on the leaderboard; if the score improves, keep the expanded ensemble, otherwise revert.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.82329 → 0.82840 (+0.00511)
- expert 60197293 (Expert) · learning · v29→v35   Try increasing the fold count substantially (e.g., 5→30). If the score does not improve or degrades, the validation sets are likely too small for reliable early stopping or the additional folds add noise. Revert to a moderate count (e.g., 10) that keeps validation sets large enough for stable early-
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score n/a → 0.81788
- expert 55987255 (Master) · learning · v37→v38   Before removing debug shortcuts, recognize that a single-fold prediction can sometimes outscore a full cross-validation ensemble if the single fold's data distribution better matches the test set or if averaging introduces noise from weaker folds. Compare per-fold OOF scores to diagnose whether spec
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.81943 → 0.81711 (-0.00232)
- expert 55591012 (Grandmaster) · learning · v9→v10   Increase the fold count substantially (e.g., triple it) so each fold trains on a larger share of data and OOF predictions become more stable. Expect a small but real gain on metrics sensitive to prediction calibration, at the cost of proportionally longer training time.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.81083 → 0.81126 (+0.00043)
- expert 55591012 (Grandmaster) · learning · v37→v39   Test a modest increase in fold count (e.g., +30–50%) and compare leaderboard or holdout scores. If the score drops, revert. Avoid changing fold count simultaneously with other hyperparameters so the effect is identifiable. Prefer the fold count that balances per-fold training set size with ensemble 
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.81990 → 0.81998 (+0.00008)
- expert 55591012 (Grandmaster) · learning · v48→v50   Average the predictions (softmax or logits) of all available transformer checkpoints before blending with the tree models. This reduces variance of the neural component and typically yields a small but consistent metric gain without any retraining.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused.
    leaderboard score 0.82007 → 0.82075 (+0.00068)
- expert 15082684 (Master) · ranzcr · v18→v22   Average predictions across fold checkpoints at inference. Ensure the model architecture flag and head configuration exactly match what was used during training of those checkpoints; a mismatch silently degrades results. Verify by comparing the ensemble score against the single-checkpoint baseline.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✓ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.96509 → 0.96591 (+0.00082)
- expert 15372370 (Expert) · ranzcr · v6→v7   Switch to simple (equal-weight) averaging of predictions across all folds of a single cross-validation run. Fold-averaging is more stable because the models share the same architecture and training recipe, reducing the risk of miscalibrated blend weights.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.96670 → 0.96804 (+0.00135)
- expert 15164527 (Expert) · ranzcr · v5→v6   For each model in the ensemble, run inference with every fold's checkpoint and average their predictions before blending across models. This reduces variance in each model's contribution and typically yields a small but consistent metric gain.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.96679 → 0.96755 (+0.00076)
- expert 15164527 (Expert) · ranzcr · v23→v30   Isolate each fold by running inference with only that fold's checkpoint and submitting separately. Compare each single-fold score to the full-ensemble score. If all single-fold scores are substantially lower, averaging all folds is justified. If one fold scores much worse, consider dropping or down-
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts. | ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.96811 → 0.96220 (-0.00591)
- expert 50496431 (Grandmaster) · hms · v1→v5   Loop over all fold checkpoint files, load each model's weights, run inference on the test set collecting predictions per fold, then average the per-fold prediction arrays element-wise. Ensure the dataset class returns only inputs (no labels) during inference and that the data loader yields the expec
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score n/a → 0.42903
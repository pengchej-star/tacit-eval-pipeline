# Change the number of fold checkpoints  `T.5.1.4`   50 edits, 0 experts
41 scored cases, median improvement -0.00091, 16 improved


- expert 27799930 (Contributor) · amex · v16→v24   Persist each fold model to disk immediately after training. At inference time, load every fold model, generate predicted probabilities on the same test features, and average the probabilities across all folds. Merge the averaged predictions with the submission template and write the output file.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score n/a → 0.78812
- expert 27799930 (Contributor) · amex · v53→v55   Try a small range of fold counts (e.g., 5, 7, 10) and compare public leaderboard or held-out scores. Prefer the higher fold count if it scores better, since each fold model sees more data and the averaged prediction is smoother.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score n/a → 0.79342
- expert 27799930 (Contributor) · amex · v67→v69   Try a small range of fold counts (e.g., 5–10) and compare leaderboard or validation scores. A moderate fold count that keeps each fold's training set large enough while providing sufficient ensemble members often works best. If reducing folds hurts, revert promptly rather than continuing to tune oth
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score n/a → 0.79475
- expert 27656049 (Expert) · amex · v7→v8   Switch to stratified k-fold CV (e.g., 10 folds) to preserve class proportions in each fold. Train one model per fold and average their predicted probabilities on the test set. When increasing the number of folds, consider reducing per-model capacity (fewer boosting rounds or leaves) to keep total tr
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score n/a → 0.78584
- expert 17616127 (Contributor) · commonlitreadabilityprize · v2→v5   Blend predictions from several checkpoints using a weighted average. Even a simple three-model blend with hand-tuned weights can outperform every individual model. When removing a component worsens the score, keep it; when a single model underperforms the blend, do not discard the ensemble in favor 
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.48820 → 0.48820 (+0.00000)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v12→v14   Average the raw predictions of all ensemble members with equal weights. Start with a small set, submit, then iteratively swap out the weakest-contributing member or add stronger members, using the validation or leaderboard score to judge each change. Prefer members that are diverse (different archit
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.51701 → 0.47623 (-0.04078)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v38→v43   Add folds one at a time and measure the target metric after each addition. Track the marginal improvement per fold. Stop when the gain drops below a small threshold relative to earlier gains (e.g., an order of magnitude smaller than the first fold's contribution), as further additions are unlikely t
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.46554 → 0.45414 (-0.01140)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v75→v78   Try adding more folds from each model family one group at a time and submit. If the metric does not improve (or worsens), the original smaller blend likely already captured the diversity benefit; additional folds add redundancy rather than complementary signal. Stop expanding when two consecutive ad
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.45173 → 0.45174 (+0.00000)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v80→v81   Test a single-fold weighted combination against the multi-fold average. Expect the multi-fold average to win because averaging across folds reduces variance, especially when the test set is small and noisy. Revert if the single-fold approach scores worse.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.45266 → 0.45684 (+0.00419)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v81→v85   For each fold, compute a weighted combination of the different models' predictions for that fold, then average the fold-level blended predictions with equal weight (1/number-of-folds). This preserves fold-specific signal diversity and can outperform a single global weighted average.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.45684 → 0.45142 (-0.00542)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v92→v98   Treat fold inclusion as a discrete search variable: toggle each fold in/out, evaluate on the held-out metric, and keep the subset that scores best. Start by removing any fold that causes errors or is suspected weak, then try adding it back to confirm the effect.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.45486 → 0.45076 (-0.00410)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v140→v141   Default to returning the averaged prediction across folds for the final submission unless there is a downstream blending step that specifically benefits from per-fold granularity. The averaged output is more robust and avoids accidental mishandling of per-fold arrays.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score n/a → 0.44790
- expert 18426209 (Expert) · commonlitreadabilityprize · v8→v9   Replace automatic checkpoint discovery with an explicit list of checkpoint paths. Annotate each with its known validation score. This makes the ensemble deterministic and allows selective exclusion of weak folds. Verify the effect by submitting and comparing against the previous score.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.45918 → 0.45856 (-0.00062)
- expert 18350823 (Expert) · commonlitreadabilityprize · v2→v4   Before increasing the number of folds in the ensemble, verify that a trained checkpoint exists for every fold index and that each fold's random seed and data split are correctly assigned. Test the expanded ensemble and revert if the score worsens, as the issue is likely infrastructure (missing or mi
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.46275 → 0.46448 (+0.00173)
- expert 17371717 (Master) · commonlitreadabilityprize · v12→v14   Test single-checkpoint-per-fold first as a baseline, then add per-seed averaging (load all seed-specific checkpoints for each fold, average their predictions, then average across folds). Compare leaderboard scores to confirm that multi-seed averaging helps. Pair with newer/better-trained checkpoints
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ Independent training seeds produce materially different errors on the same examples. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.47587 → 0.46639 (-0.00948)
- expert 17371717 (Master) · commonlitreadabilityprize · v29→v30   Compare the ensemble of all fold checkpoints against the single best fold checkpoint. Expect the multi-fold ensemble to be substantially better due to variance reduction; revert to the ensemble if the single checkpoint degrades the score.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.46114 → 0.47074 (+0.00960)
- expert 7018718 (Expert) · google · v11→v13   Test removing a subset of fold models while keeping the blending method fixed. If the score drops, restore all folds. Avoid changing both the model subset and the blending method simultaneously, because the confounded result is uninterpretable.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.38408 → 0.38367 (-0.00040)
- expert 7018718 (Expert) · google · v51→v52   Ensemble predictions from multiple training runs by averaging before applying the post-processing step. The averaging reduces prediction noise, and the subsequent discretization/binning further aligns outputs with the true label distribution.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score n/a → 0.43979
- expert 7613444 (Contributor) · google · v11→v12   Ensure every trained fold model is loaded and included in the test-time average. Verify that checkpoint file paths match the actual saved names (e.g., via a print/log statement). Going from a partial to a full fold ensemble typically yields a small but consistent gain because averaging more diverse 
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.39956 → 0.40047 (+0.00091)
- expert 7573212 (Contributor) · google · v5→v7   Be cautious: dropping folds from a K-fold ensemble usually hurts because it reduces the effective training data and increases variance. If no local validation metric guides fold weighting, prefer equal-weight averaging. Leaderboard probing of fold subsets is unreliable due to noise and risks overfit
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.38598 → 0.37898 (-0.00700)
- expert 6803050 (Master) · google · v18→v19   Load each fold's checkpoint independently, run full inference on the test set with each, then average the resulting prediction arrays element-wise. This simple mean ensemble reduces variance from individual fold training randomness.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score -0.00372 → -0.00372 (+0.00000)
- expert 6803050 (Master) · google · v21→v23   Ablate by submitting a single fold's predictions alone, then compare against the full ensemble. This isolates the ensemble's contribution. If the gap is large, keep the ensemble; the magnitude also indicates how much variance reduction matters for the metric.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✗ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.36763 → 0.38182 (+0.01419)
- expert 7606235 (Master) · google · v15→v23   Test small ensembles (2–3 checkpoints) against the best single checkpoint on the leaderboard. If the ensemble consistently scores below the best single checkpoint, the weaker folds are adding noise that hurts ranking quality. In that case, keep the single best checkpoint rather than averaging, or tr
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows.
    leaderboard score 0.38524 → 0.38785 (+0.00261)
- expert 7253130 (Contributor) · google · v11→v12   Increase the number of CV folds (e.g., by 50%) so that more independently trained models contribute to the averaged prediction. This reduces variance at the cost of longer training time. Verify the improvement on the leaderboard; if the gain is meaningful, keep the higher fold count.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.37532 → 0.38610 (+0.01078)
- expert 50376011 (Grandmaster) · hms · v31→v37   Build a loop that loads each fold's saved weights into the same architecture, runs inference on the test set, and averages (or weighted-averages) the resulting predictions across all folds before producing the final submission. This reduces variance from any single fold's idiosyncrasies.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.39254 → 0.35548 (-0.03706)
- expert 50376011 (Grandmaster) · hms · v55→v57   Remove the explicit fold restriction and let the inference script average over all available fold checkpoints. If the first submission shows a small regression, re-run before concluding the change is harmful, since leaderboard noise can mask small improvements.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✗ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.34467 → 0.34376 (-0.00091)
- expert 50376011 (Grandmaster) · hms · v93→v94   Systematically increase the number of ensemble members (e.g., from 1 to 6 folds) with uniform weights. When the metric rewards calibration (e.g., KL divergence), averaging over more diverse folds tends to yield a substantial improvement. After finding the gain, verify by comparing back to fewer memb
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.33490 → 0.31316 (-0.02174)
- expert 50376011 (Grandmaster) · hms · v126→v142   Sweep individual checkpoints first to rank them by solo performance, then try small ensembles of the top-performing members. Re-submit the same configuration multiple times to estimate submission variance before concluding one config beats another. Only trust improvements that exceed the observed no
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows.
    leaderboard score 0.27192 → 0.26480 (-0.00712)
- expert 50376011 (Grandmaster) · hms · v166→v169   Try a moderate fold count (not the maximum) combined with multiple diverse checkpoints rather than maximizing fold count with a single checkpoint. Test both dimensions independently and in combination, comparing leaderboard scores to find the sweet spot.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.25358 → 0.25069 (-0.00290)
- expert 50376011 (Grandmaster) · hms · v190→v191   Incrementally add more fold checkpoints to the ensemble (e.g., double the count). If the metric improves, keep the larger set. Then try swapping individual members one at a time to fine-tune composition. Stop expanding when adding more members no longer helps or degrades the score.
    evidence: ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.24878 → 0.23917 (-0.00961)
- expert 50376011 (Grandmaster) · hms · v213→v218   Incrementally increase the number of fold predictions averaged at inference and monitor the evaluation metric. Averaging more folds typically reduces prediction variance and improves calibration. Continue adding folds as long as the metric improves and inference time/memory permits.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.25121 → 0.24408 (-0.00712)
- expert 50376011 (Grandmaster) · hms · v222→v228   Add checkpoints to the ensemble incrementally, submitting after each addition. Keep adding as long as the metric improves. Verify with single-model ablations that the ensemble is indeed better than any individual member. Continue until all available checkpoints are included or gains plateau.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✗ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.23868 → 0.23565 (-0.00303)
- expert 50376011 (Grandmaster) · hms · v252→v254   Add checkpoints incrementally, submitting after each addition. Track the marginal improvement per added member. Continue adding until the marginal gain becomes negligible or turns negative, then stop at the best count.
    evidence: ✗ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.22970 → 0.22640 (-0.00331)
- expert 49576186 (Expert) · hms · v20→v22   Average the predicted probability distributions from all fold models for each test sample. This reduces prediction variance and typically improves calibration, yielding a better score on distribution-matching metrics like KL divergence.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.41352 → 0.36216 (-0.05135)
- expert 60264017 (Master) · learning · v13→v14   Build an inference routine that loads every available checkpoint, runs each on the test data, and averages their outputs. Optionally fit a scaler (e.g., min-max) on out-of-fold predictions to align the averaged output's range with the target distribution before feeding it into the downstream ensembl
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.82848 → n/a
- expert 55621328 (Master) · learning · v12→v14   Load all fold checkpoints and average their predictions before applying any post-processing (e.g., threshold rounding). This reduces variance and typically improves ranking metrics without retraining. Prefer the model size that already performed best on the leaderboard.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.80219 → 0.80527 (+0.00308)
- expert 55621328 (Master) · learning · v53→v55   Test multi-fold averaging against the single best fold on the leaderboard. If multi-fold scores lower, revert to the single best fold and only use multi-fold when each fold's individual score is competitive. Do not assume more folds always help.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.81104 → 0.81742 (+0.00638)
- expert 55621328 (Master) · learning · v78→v80   Try replacing the single-fold checkpoint with a multi-fold ensemble (all folds averaged) from the same or a related experiment, adjusting blend weights accordingly. Multi-fold averaging typically reduces variance and outperforms any single fold. If a pseudo-labeled single checkpoint does not beat th
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.82461 → 0.82504 (+0.00043)
- expert 55621328 (Master) · learning · v80→v81   Test a single-checkpoint variant against the full ensemble. If the score drops, keep the multi-checkpoint ensemble; the diversity from multiple folds or seeds is contributing meaningfully to prediction quality.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.82504 → 0.82051 (-0.00453)
- expert 55621328 (Master) · learning · v92→v94   Test the multi-fold ensemble against the single best fold on the leaderboard. If the multi-fold average scores lower, the individual fold may have been better calibrated to the test distribution; revert to the single fold. Also test individual alternative folds to check whether the gain was fold-spe
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.82736 → 0.81721 (-0.01015)
- expert 55621328 (Master) · learning · v93→v94   Isolate and evaluate individual alternative folds. If they score substantially lower than the best fold, the performance gap confirms that the best fold is unusually well-aligned with the test distribution, and the ensemble is diluted by weaker folds. Keep the best single fold rather than averaging.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.82276 → 0.81721 (-0.00555)
- expert 60197293 (Expert) · learning · v29→v35   Try increasing the fold count substantially (e.g., 5→30). If the score does not improve or degrades, the validation sets are likely too small for reliable early stopping or the additional folds add noise. Revert to a moderate count (e.g., 10) that keeps validation sets large enough for stable early-
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score n/a → 0.81788
- expert 55591012 (Grandmaster) · learning · v9→v10   Increase the fold count substantially (e.g., triple it) so each fold trains on a larger share of data and OOF predictions become more stable. Expect a small but real gain on metrics sensitive to prediction calibration, at the cost of proportionally longer training time.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.81083 → 0.81126 (+0.00043)
- expert 55591012 (Grandmaster) · learning · v37→v39   Test a modest increase in fold count (e.g., +30–50%) and compare leaderboard or holdout scores. If the score drops, revert. Avoid changing fold count simultaneously with other hyperparameters so the effect is identifiable. Prefer the fold count that balances per-fold training set size with ensemble 
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.81990 → 0.81998 (+0.00008)
- expert 55591012 (Grandmaster) · learning · v48→v50   Average the predictions (softmax or logits) of all available transformer checkpoints before blending with the tree models. This reduces variance of the neural component and typically yields a small but consistent metric gain without any retraining.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.82007 → 0.82075 (+0.00068)
- expert 15082684 (Master) · ranzcr · v18→v22   Average predictions across fold checkpoints at inference. Ensure the model architecture flag and head configuration exactly match what was used during training of those checkpoints; a mismatch silently degrades results. Verify by comparing the ensemble score against the single-checkpoint baseline.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.96509 → 0.96591 (+0.00082)
- expert 15164527 (Expert) · ranzcr · v5→v6   For each model in the ensemble, run inference with every fold's checkpoint and average their predictions before blending across models. This reduces variance in each model's contribution and typically yields a small but consistent metric gain.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.96679 → 0.96755 (+0.00076)
- expert 15164527 (Expert) · ranzcr · v23→v30   Isolate each fold by running inference with only that fold's checkpoint and submitting separately. Compare each single-fold score to the full-ensemble score. If all single-fold scores are substantially lower, averaging all folds is justified. If one fold scores much worse, consider dropping or down-
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.96811 → 0.96220 (-0.00591)
- expert 50496431 (Grandmaster) · hms · v1→v5   Loop over all fold checkpoint files, load each model's weights, run inference on the test set collecting predictions per fold, then average the per-fold prediction arrays element-wise. Ensure the dataset class returns only inputs (no labels) during inference and that the data loader yields the expec
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score n/a → 0.42903
- expert 50496431 (Grandmaster) · hms · v7→v8   Systematically try alternative checkpoint selections—varying which epoch or run is chosen per fold—and evaluate on the leaderboard or a held-out set. Even without changing the model or augmentation, checkpoint selection alone can yield a larger gain than adding TTA.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.42697 → 0.42196 (-0.00501)
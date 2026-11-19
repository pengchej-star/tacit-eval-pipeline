# Average more fold checkpoints  `T.7.2.5`   29 edits, 0 experts
20 scored cases (improvement signed by each competition's direction), median +0.00331, 16 improved


- expert 27799930 · amex · v16→v24   Persist each fold model to disk immediately after training. At inference time, load every fold model, generate predicted probabilities on the same test features, and average the probabilities across all folds. Merge the averaged predictions with the submission template and write the output file.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✗ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation. | ✓ Most active members share one architecture or algorithm and their residuals are highly correlated.
    leaderboard score n/a → 0.78812 (higher is better)
- expert 27799930 · amex · v53→v55   Try a small range of fold counts (e.g., 5, 7, 10) and compare public leaderboard or held-out scores. Prefer the higher fold count if it scores better, since each fold model sees more data and the averaged prediction is smoother.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ Most active members share one architecture or algorithm and their residuals are highly correlated.
    leaderboard score n/a → 0.79342 (higher is better)
- expert 27799930 · amex · v67→v69   Try a small range of fold counts (e.g., 5–10) and compare leaderboard or validation scores. A moderate fold count that keeps each fold's training set large enough while providing sufficient ensemble members often works best. If reducing folds hurts, revert promptly rather than continuing to tune oth
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Training seeds produce substantial variance while architecture and fold setup remain fixed.
    leaderboard score n/a → 0.79475 (higher is better)
- expert 27799930 · amex · v73→v74   Treat the number of folds and seeds as low-cost hyperparameters to search over. Increase one at a time, verify on the leaderboard or a stable local metric, and keep the configuration that improves the score. If adding a seed or fold does not help, revert. Avoid assuming more is always better.
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Training seeds produce substantial variance while architecture and fold setup remain fixed. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score n/a → n/a (higher is better)
- expert 17616127 · commonlitreadabilityprize · v38→v43   Add folds one at a time and measure the target metric after each addition. Track the marginal improvement per fold. Stop when the gain drops below a small threshold relative to earlier gains (e.g., an order of magnitude smaller than the first fold's contribution), as further additions are unlikely t
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ Most active members share one architecture or algorithm and their residuals are highly correlated.
    leaderboard score 0.46554 → 0.45414 (lower is better; improved by 0.01140)
- expert 17616127 · commonlitreadabilityprize · v75→v78   Try adding more folds from each model family one group at a time and submit. If the metric does not improve (or worsens), the original smaller blend likely already captured the diversity benefit; additional folds add redundancy rather than complementary signal. Stop expanding when two consecutive ad
    evidence: ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score 0.45173 → 0.45174 (lower is better; worse by 0.00000)
- expert 17616127 · commonlitreadabilityprize · v80→v81   Test a single-fold weighted combination against the multi-fold average. Expect the multi-fold average to win because averaging across folds reduces variance, especially when the test set is small and noisy. Revert if the single-fold approach scores worse.
    evidence: ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score 0.45266 → 0.45684 (lower is better; worse by 0.00419)
- expert 17616127 · commonlitreadabilityprize · v140→v141   Default to returning the averaged prediction across folds for the final submission unless there is a downstream blending step that specifically benefits from per-fold granularity. The averaged output is more robust and avoids accidental mishandling of per-fold arrays.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score n/a → 0.44790 (lower is better)
- expert 18837555 · commonlitreadabilityprize · v1→v5   Load each additional checkpoint, run inference, collect all predictions into an array, average them, and blend that average with existing predictions. Even a small number of extra checkpoints can yield a meaningful RMSE reduction on regression tasks with noisy targets.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.46181 → 0.46041 (lower is better; improved by 0.00141)
- expert 17371717 · commonlitreadabilityprize · v29→v30   Compare the ensemble of all fold checkpoints against the single best fold checkpoint. Expect the multi-fold ensemble to be substantially better due to variance reduction; revert to the ensemble if the single checkpoint degrades the score.
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Training seeds produce substantial variance while architecture and fold setup remain fixed. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score 0.46114 → 0.47074 (lower is better; worse by 0.00960)
- expert 77347591 · equity · v5→v7   Increase the number of CV folds (e.g., double them) to reduce variance in OOF predictions, and simultaneously increase early-stopping patience substantially (e.g., more than double) so models train closer to their optimum before stopping. Combine this with hyperparameter re-tuning since the changed 
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.69346 → n/a (higher is better)
- expert 7018718 · google · v51→v52   Ensemble predictions from multiple training runs by averaging before applying the post-processing step. The averaging reduces prediction noise, and the subsequent discretization/binning further aligns outputs with the true label distribution.
    evidence: ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score n/a → 0.43979 (higher is better)
- expert 7613444 · google · v11→v12   Ensure every trained fold model is loaded and included in the test-time average. Verify that checkpoint file paths match the actual saved names (e.g., via a print/log statement). Going from a partial to a full fold ensemble typically yields a small but consistent gain because averaging more diverse 
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.39956 → 0.40047 (higher is better; improved by 0.00091)
- expert 6803050 · google · v18→v19   Load each fold's checkpoint independently, run full inference on the test set with each, then average the resulting prediction arrays element-wise. This simple mean ensemble reduces variance from individual fold training randomness.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score -0.00372 → -0.00372 (higher is better; unchanged by 0.00000)
- expert 7253130 · google · v11→v12   Increase the number of CV folds (e.g., by 50%) so that more independently trained models contribute to the averaged prediction. This reduces variance at the cost of longer training time. Verify the improvement on the leaderboard; if the gain is meaningful, keep the higher fold count.
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.37532 → 0.38610 (higher is better; improved by 0.01078)
- expert 50376011 · hms · v31→v37   Build a loop that loads each fold's saved weights into the same architecture, runs inference on the test set, and averages (or weighted-averages) the resulting predictions across all folds before producing the final submission. This reduces variance from any single fold's idiosyncrasies.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.39254 → 0.35548 (lower is better; improved by 0.03706)
- expert 50376011 · hms · v93→v94   Systematically increase the number of ensemble members (e.g., from 1 to 6 folds) with uniform weights. When the metric rewards calibration (e.g., KL divergence), averaging over more diverse folds tends to yield a substantial improvement. After finding the gain, verify by comparing back to fewer memb
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.33490 → 0.31316 (lower is better; improved by 0.02174)
- expert 50376011 · hms · v122→v123   Progressively increase the number of ensemble members with equal blending weights. When prior experiments show monotonic improvement from 1→2→4 members, try the full set of available checkpoints. Use uniform weights as a strong default unless there is evidence that some members are weaker.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.28870 → 0.27696 (lower is better; improved by 0.01174)
- expert 50376011 · hms · v166→v169   Try a moderate fold count (not the maximum) combined with multiple diverse checkpoints rather than maximizing fold count with a single checkpoint. Test both dimensions independently and in combination, comparing leaderboard scores to find the sweet spot.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ Most active members share one architecture or algorithm and their residuals are highly correlated.
    leaderboard score 0.25358 → 0.25069 (lower is better; improved by 0.00290)
- expert 50376011 · hms · v190→v191   Incrementally add more fold checkpoints to the ensemble (e.g., double the count). If the metric improves, keep the larger set. Then try swapping individual members one at a time to fine-tune composition. Stop expanding when adding more members no longer helps or degrades the score.
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score 0.24878 → 0.23917 (lower is better; improved by 0.00961)
- expert 50376011 · hms · v213→v218   Incrementally increase the number of fold predictions averaged at inference and monitor the evaluation metric. Averaging more folds typically reduces prediction variance and improves calibration. Continue adding folds as long as the metric improves and inference time/memory permits.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.25121 → 0.24408 (lower is better; improved by 0.00712)
- expert 50376011 · hms · v222→v228   Add checkpoints to the ensemble incrementally, submitting after each addition. Keep adding as long as the metric improves. Verify with single-model ablations that the ensemble is indeed better than any individual member. Continue until all available checkpoints are included or gains plateau.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.23868 → 0.23565 (lower is better; improved by 0.00303)
- expert 50376011 · hms · v237→v251   Incrementally add checkpoints to the ensemble, submitting after each addition. When the improvement from adding one more member falls within the noise floor, stop. If runtime is the binding constraint, reduce per-sample processing cost (e.g., smaller batch counts or fewer augmentation passes) to fit
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score 0.23496 → n/a (lower is better)
- expert 50376011 · hms · v252→v254   Add checkpoints incrementally, submitting after each addition. Track the marginal improvement per added member. Continue adding until the marginal gain becomes negligible or turns negative, then stop at the best count.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.22970 → 0.22640 (lower is better; improved by 0.00331)
- expert 49576186 · hms · v20→v22   Average the predicted probability distributions from all fold models for each test sample. This reduces prediction variance and typically improves calibration, yielding a better score on distribution-matching metrics like KL divergence.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.41352 → 0.36216 (lower is better; improved by 0.05135)
- expert 15082684 · ranzcr · v18→v22   Average predictions across fold checkpoints at inference. Ensure the model architecture flag and head configuration exactly match what was used during training of those checkpoints; a mismatch silently degrades results. Verify by comparing the ensemble score against the single-checkpoint baseline.
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation. | ✓ One or more fold checkpoints are incompatible or repeatedly harm the full average on reliable validation.
    leaderboard score 0.96509 → 0.96591 (higher is better; improved by 0.00082)
- expert 15372370 · ranzcr · v4→v5   Load all checkpoints, run each on both the original and augmented (e.g., flipped) inputs, and equally average all predictions. This simple uniform ensemble often gives a meaningful boost before any weight tuning.
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.96341 → 0.96726 (higher is better; improved by 0.00385)
- expert 15164527 · ranzcr · v5→v6   For each model in the ensemble, run inference with every fold's checkpoint and average their predictions before blending across models. This reduces variance in each model's contribution and typically yields a small but consistent metric gain.
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score 0.96679 → 0.96755 (higher is better; improved by 0.00076)
- expert 50496431 · hms · v1→v5   Loop over all fold checkpoint files, load each model's weights, run inference on the test set collecting predictions per fold, then average the per-fold prediction arrays element-wise. Ensure the dataset class returns only inputs (no labels) during inference and that the data loader yields the expec
    evidence: ✓ Additional compatible fold checkpoints are unused and prior fold additions have improved validation.
    leaderboard score n/a → 0.42903 (lower is better)
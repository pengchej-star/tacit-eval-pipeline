# Compare rank and raw averaging  `T.6.3.1`   24 edits, 0 experts
15 scored cases, median improvement +0.00091, 13 improved


- expert 13848868 (Grandmaster) · ranzcr · v1→v6   Toggle rank-conversion on and off as a binary flag while holding other settings constant. If the effect is inconsistent across configurations and the magnitude is very small (order of 0.0001–0.001), prefer the simpler raw-averaging approach and move on to higher-impact levers.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✗ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score 0.92999 → 0.93869 (+0.00870)
- expert 13848868 (Grandmaster) · ranzcr · v7→v10   Re-evaluate the toggle after every model or pipeline change by submitting both variants. Do not carry forward the previous conclusion; treat it as a cheap A/B test that must be re-run whenever upstream predictions change.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✗ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score 0.94135 → 0.94330 (+0.00195)
- expert 13848868 (Grandmaster) · ranzcr · v14→v16   Treat the choice between raw-score averaging and rank-based averaging as a binary hyperparameter. After any change to the model or ensemble setup, test both options with leaderboard or validation submissions. Do not assume the previous winner still holds.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✗ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score n/a → 0.94293
- expert 13848868 (Grandmaster) · ranzcr · v17→v21   After any significant model change, re-test both raw-score averaging and rank-averaging by toggling the post-processing flag and submitting. Do not carry over the conclusion from a previous model; treat it as an independent binary decision each time the prediction distribution changes.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✗ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score 0.93993 → 0.95233 (+0.01240)
- expert 13848868 (Grandmaster) · ranzcr · v21→v28   Re-evaluate the toggle for every new model variant by submitting both settings. Do not assume the result from a previous model configuration carries over. This costs one extra submission per model change but prevents carrying a suboptimal post-processing choice forward.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✗ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score 0.95233 → 0.94904 (-0.00329)
- expert 13848868 (Grandmaster) · ranzcr · v29→v30   After every non-trivial model change, re-test both post-processing options. Do not assume the previously better setting carries over. Submit both variants and keep whichever scores higher for that model configuration.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ.
    leaderboard score 0.94661 → 0.94719 (+0.00058)
- expert 13848868 (Grandmaster) · ranzcr · v31→v36   Toggle between raw-score averaging and rank-based averaging at each major configuration change and compare on the leaderboard or validation set. The winner can flip depending on the model and configuration, so always re-check after any architecture or resolution change rather than assuming one metho
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ.
    leaderboard score 0.95418 → 0.95509 (+0.00091)
- expert 13848868 (Grandmaster) · ranzcr · v37→v39   Treat the choice between rank-based and raw-score fold averaging as a binary toggle that must be re-evaluated after every significant model change. Submit both variants and keep whichever scores better; do not assume the previous winner still holds.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ.
    leaderboard score 0.95762 → 0.96074 (+0.00312)
- expert 13848868 (Grandmaster) · ranzcr · v39→v41   After every significant model change, test both raw-score averaging and rank-based averaging. Expect that stronger, better-calibrated models will more often favor raw averaging, while rank averaging may help weaker or poorly calibrated ensembles. Do not assume the post-processing choice transfers wh
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ.
    leaderboard score 0.96074 → 0.96470 (+0.00396)
- expert 77450317 (Grandmaster) · equity · v3→v6   Try both raw scores and rank-transformed scores in the blend. Rank transformation can destroy useful magnitude information that helps the average preserve ordering, especially when models are well-calibrated. Test both and keep whichever yields a better validation or leaderboard score; do not assume
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✗ Absolute magnitudes are required by a downstream additive correction. | ✗ Models expose both logits and probabilities and the metric evaluates distributions.
    leaderboard score n/a → n/a
- expert 75145694 (Expert) · equity · v23→v26   Combine ensemble members on their raw (or probability-scale) outputs to preserve relative magnitude information, then apply a single rank transformation to the final blended prediction before submission. Compare this against per-model ranking and no ranking to confirm the best approach.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✗ Absolute magnitudes are required by a downstream additive correction. | ✓ A fitted linear combiner receives predictors with very different variance or heavy tails.
    leaderboard score 0.68851 → 0.69023 (+0.00172)
- expert 75145694 (Expert) · equity · v26→v27   Rank-transform each member's predictions before weighted averaging. This normalizes all members to the same scale and ensures the blend respects only ordinal information, which is what the metric evaluates. Also experiment with which model serves as the seed/base, since a stronger base can anchor th
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✓ A fitted linear combiner receives predictors with very different variance or heavy tails. | ✗ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score 0.69023 → 0.69111 (+0.00088)
- expert 77276039 (Expert) · equity · v2→v3   Use a weighted average of raw predictions instead of rank-averaging when any downstream post-processing step adds or scales the combined score. Assign explicit weights to each model and merge predictions on the sample identifier before averaging, so the resulting scores retain interpretable magnitud
    evidence: ✓ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score n/a → n/a
- expert 77276039 (Expert) · equity · v8→v10   Switch from weighted averaging of raw scores to rank averaging: convert each model's predictions to ranks (or percentile scores), then average the ranks. This makes the ensemble invariant to each component's score scale, which is especially appropriate when the evaluation metric is rank-based.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✓ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score n/a → 0.69330
- expert 73937748 (Master) · equity · v44→v45   Test both raw and rank-transformed base predictions as input to the linear meta-learner. If the raw version scores equal or better, prefer it—the meta-learner can learn its own implicit ranking, and preserving magnitude gives it more information to work with.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✓ A fitted linear combiner receives predictors with very different variance or heavy tails. | ✗ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score 0.68926 → 0.68967 (+0.00041)
- expert 7018718 (Expert) · google · v3→v4   Run a controlled A/B test by toggling the rank-blending option off while keeping everything else fixed, and compare leaderboard or validation scores. Do not assume rank averaging always helps; verify empirically for each model configuration.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ.
    leaderboard score 0.37770 → 0.37851 (+0.00081)
- expert 7018718 (Expert) · google · v9→v13   Systematically try each candidate aggregation strategy (raw mean, rank-based averaging, nonlinear transformation) one at a time, keeping everything else fixed, and compare leaderboard or validation scores. If none improves over the simplest baseline, keep the baseline. Do not combine multiple change
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ.
    leaderboard score n/a → 0.38367
- expert 7018718 (Expert) · google · v14→v18   Try at least three combination strategies—rank-based averaging, sigmoid-transformed averaging, and simple mean—submitting each separately. Expect small differences; choose the best empirically rather than assuming one dominates, since the optimal strategy depends on how well-calibrated individual fo
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ.
    leaderboard score 0.38367 → 0.38508 (+0.00141)
- expert 7018718 (Expert) · google · v32→v34   Test both strategies while holding all other variables (checkpoint, preprocessing, architecture) constant. If the target labels occupy only a few discrete levels, raw averaging may preserve the relative ordering better than rank averaging because rank averaging can introduce unnecessary ties or dist
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ.
    leaderboard score n/a → 0.37705
- expert 7670859 (Contributor) · google · v13→v15   Start with simple arithmetic averaging of prediction arrays, then iteratively add or remove sources while inspecting the distribution of blended predictions (e.g., histograms). If a source degrades the blend or has misaligned distributions, drop it. Use diagnostic plots at each step to verify that t
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✗ Absolute magnitudes are required by a downstream additive correction. | ✓ Bounded component probabilities are highly concentrated before averaging.
    leaderboard score n/a → n/a
- expert 6803050 (Master) · google · v2→v9   For a purely rank-based metric, submit the raw (unclipped, unscaled) predictions first as a baseline, since monotonic transforms cannot change ranks. Only add clipping or rescaling if the submission format requires bounded values or if post-processing (e.g., rounding to discrete levels) is applied a
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✓ Bounded component probabilities are highly concentrated before averaging. | ✗ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score n/a → n/a
- expert 6803050 (Master) · google · v24→v26   Avoid inserting additional normalization between the raw predictions and a quantile/rank-based calibration step, because altering the relative scale can shift values across quantile boundaries and destroy rank order. If tried, verify immediately and revert if the score drops.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✓ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score 0.37058 → 0.25892 (-0.11166)
- expert 6803050 (Master) · google · v26→v27   Remove the unnecessary normalization. Rank-based post-processing (quantile mapping) depends on the ordering of predictions, not their scale, so any rescaling that distorts relative ordering (e.g., adding constants, dividing by a per-fold max) can only hurt. Feed raw averaged outputs directly into th
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✓ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score 0.25892 → n/a
- expert 15164527 (Expert) · ranzcr · v12→v15   Convert each model's predictions to per-column ranks (using double argsort), then take a weighted average of ranks. This removes calibration differences and is naturally suited to rank-based metrics. Compare against probability averaging to confirm the gain.
    evidence: ✓ The metric depends on ordering and member score scales or calibration differ. | ✗ Absolute magnitudes are required by a downstream additive correction.
    leaderboard score 0.96760 → 0.96778 (+0.00017)
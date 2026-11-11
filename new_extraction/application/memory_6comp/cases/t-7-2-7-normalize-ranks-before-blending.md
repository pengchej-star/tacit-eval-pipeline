# Normalize ranks before blending  `T.7.2.7`   16 edits, 0 experts
7 scored cases, median improvement +0.00081, 6 improved


- expert 77450317 (Grandmaster) · equity · v3→v6   Try both raw scores and rank-transformed scores in the blend. Rank transformation can destroy useful magnitude information that helps the average preserve ordering, especially when models are well-calibrated. Test both and keep whichever yields a better validation or leaderboard score; do not assume
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✗ Members predict class distributions and stored logits are available.
    leaderboard score n/a → n/a
- expert 75584724 (Master) · equity · v8→v11   Test with and without standardization of the meta-features (fit scaler on out-of-fold predictions, apply to test). Compare leaderboard or validation scores for both settings. If the difference is negligible or negative, keep raw predictions—ranking-based metrics are invariant to monotone transforms 
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✗ Members predict class distributions and stored logits are available. | ✓ Leakage-free out-of-fold predictions and enough examples to fit a combiner are available.
    leaderboard score n/a → 0.69408
- expert 75584724 (Master) · equity · v12→v13   Try a median-and-IQR-based scaler (robust to outliers) instead of a mean-and-variance scaler for normalizing individual model predictions before weight optimization. Compare leaderboard or validation scores to confirm the benefit.
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✗ Members predict class distributions and stored logits are available.
    leaderboard score 0.69376 → 0.69399 (+0.00023)
- expert 75584724 (Master) · equity · v15→v16   When changing the scaler, always re-optimize blend weights from scratch rather than manually adjusting them. Validate the new scaler-plus-weights combination on the same OOF metric before submitting, because the interaction between scaling and weights can cause regressions even when each change seem
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✗ Members predict class distributions and stored logits are available.
    leaderboard score n/a → 0.69376
- expert 77347591 (Expert) · equity · v14→v20   First test ablation (remove each component) to confirm every model contributes. Then try integer or small multiplicative up-weights on individual components. If none improves over equal weighting, accept that equal-weight rank averaging is near-optimal. Limit the number of submissions to avoid overf
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✓ Components have unequal validated quality and their combination changes the metric. | ✗ Members predict class distributions and stored logits are available. | ✓ Component quality is similar and fitted weights are unstable across validation folds.
    leaderboard score 0.69415 → 0.69411 (-0.00005)
- expert 75145694 (Expert) · equity · v23→v26   Combine ensemble members on their raw (or probability-scale) outputs to preserve relative magnitude information, then apply a single rank transformation to the final blended prediction before submission. Compare this against per-model ranking and no ranking to confirm the best approach.
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✗ Members predict class distributions and stored logits are available. | ✓ Components have unequal validated quality and their combination changes the metric.
    leaderboard score 0.68851 → 0.69023 (+0.00172)
- expert 75145694 (Expert) · equity · v26→v27   Rank-transform each member's predictions before weighted averaging. This normalizes all members to the same scale and ensures the blend respects only ordinal information, which is what the metric evaluates. Also experiment with which model serves as the seed/base, since a stronger base can anchor th
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✗ Members predict class distributions and stored logits are available.
    leaderboard score 0.69023 → 0.69111 (+0.00088)
- expert 77276039 (Expert) · equity · v2→v3   Use a weighted average of raw predictions instead of rank-averaging when any downstream post-processing step adds or scales the combined score. Assign explicit weights to each model and merge predictions on the sample identifier before averaging, so the resulting scores retain interpretable magnitud
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers.
    leaderboard score n/a → n/a
- expert 77276039 (Expert) · equity · v8→v10   Switch from weighted averaging of raw scores to rank averaging: convert each model's predictions to ranks (or percentile scores), then average the ranks. This makes the ensemble invariant to each component's score scale, which is especially appropriate when the evaluation metric is rank-based.
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✗ Members predict class distributions and stored logits are available.
    leaderboard score n/a → 0.69330
- expert 73937748 (Master) · equity · v44→v45   Test both raw and rank-transformed base predictions as input to the linear meta-learner. If the raw version scores equal or better, prefer it—the meta-learner can learn its own implicit ranking, and preserving magnitude gives it more information to work with.
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✗ Members predict class distributions and stored logits are available.
    leaderboard score 0.68926 → 0.68967 (+0.00041)
- expert 7018718 (Expert) · google · v3→v4   Run a controlled A/B test by toggling the rank-blending option off while keeping everything else fixed, and compare leaderboard or validation scores. Do not assume rank averaging always helps; verify empirically for each model configuration.
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers.
    leaderboard score 0.37770 → 0.37851 (+0.00081)
- expert 7018718 (Expert) · google · v9→v13   Systematically try each candidate aggregation strategy (raw mean, rank-based averaging, nonlinear transformation) one at a time, keeping everything else fixed, and compare leaderboard or validation scores. If none improves over the simplest baseline, keep the baseline. Do not combine multiple change
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers.
    leaderboard score n/a → 0.38367
- expert 7018718 (Expert) · google · v14→v18   Try at least three combination strategies—rank-based averaging, sigmoid-transformed averaging, and simple mean—submitting each separately. Expect small differences; choose the best empirically rather than assuming one dominates, since the optimal strategy depends on how well-calibrated individual fo
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers.
    leaderboard score 0.38367 → 0.38508 (+0.00141)
- expert 7018718 (Expert) · google · v32→v34   Test both strategies while holding all other variables (checkpoint, preprocessing, architecture) constant. If the target labels occupy only a few discrete levels, raw averaging may preserve the relative ordering better than rank averaging because rank averaging can introduce unnecessary ties or dist
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✗ Members predict class distributions and stored logits are available.
    leaderboard score n/a → 0.37705
- expert 7670859 (Contributor) · google · v13→v15   Start with simple arithmetic averaging of prediction arrays, then iteratively add or remove sources while inspecting the distribution of blended predictions (e.g., histograms). If a source degrades the blend or has misaligned distributions, drop it. Use diagnostic plots at each step to verify that t
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✗ Members predict class distributions and stored logits are available.
    leaderboard score n/a → n/a
- expert 77276039 (Expert) · equity · v10→v12   Train the new model independently with cross-validation, produce out-of-fold and test predictions, then rank-transform all members' predictions before averaging. This makes the combination scale-invariant and avoids destabilizing the ensemble when adding members with different output distributions.
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers. | ✗ Members predict class distributions and stored logits are available.
    leaderboard score 0.69330 → n/a
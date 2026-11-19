# Optimize global thresholds  `T.6.1.1`   26 edits, 0 experts
15 scored cases, median improvement +0.00245, 11 improved


- expert 7823861 (nan) · google · v17→v24   For each target column, determine the set of possible discrete values from training data. Sweep decision thresholds that map continuous predictions to those values. Change only a few thresholds per iteration and submit to verify improvement. Avoid changing many thresholds at once, because a single b
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Binning creates constant predictions or many ties in columns scored by a rank metric.
    leaderboard score 0.44465 → 0.42936 (-0.01529)
- expert 7823861 (nan) · google · v26→v27   Recognize that discretization thresholds are high-leverage parameters: even a correct framework of rules can underperform if individual thresholds are slightly off. After establishing a clean rule structure, systematically re-tune each threshold using validation feedback rather than guessing values.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries.
    leaderboard score n/a → 0.44173
- expert 7018718 (Expert) · google · v36→v45   Discretize continuous predictions into bins matching the known target granularity using a binning/quantization step. This aligns predicted ranks with the true discrete structure and can yield a large metric jump without any model retraining.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Binning creates constant predictions or many ties in columns scored by a rank metric.
    leaderboard score 0.37590 → 0.42580 (+0.04990)
- expert 7018718 (Expert) · google · v46→v50   Apply per-target adaptive binning: sort predictions, then merge consecutive values whose gap falls below a target-specific epsilon into the same bin. Tune each epsilon on validation data. Guard against degenerate cases where all values collapse to one bin by keeping the original predictions for that
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Binning creates constant predictions or many ties in columns scored by a rank metric. | ✓ Groups or output columns show distinct calibration with adequate held-out sample counts.
    leaderboard score 0.38762 → n/a
- expert 7548275 (Expert) · google · v21→v23   Rescale predictions to [0,1] using the training set's min/max, then quantize to the discrete levels implied by the number of annotators. This collapses predictions onto the same grid as the labels, improving rank alignment. Apply domain-specific masking (e.g., zeroing irrelevant columns) where metad
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Groups or output columns show distinct calibration with adequate held-out sample counts. | ✓ Binning creates constant predictions or many ties in columns scored by a rank metric.
    leaderboard score 0.39778 → 0.42142 (+0.02364)
- expert 7573212 (Contributor) · google · v7→v9   Discretize (bin) the continuous predictions into a number of bins matching or approximating the number of distinct target levels. This collapses near-equal predictions into the same rank, reducing spurious rank differences and better aligning with the discrete target structure.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries.
    leaderboard score 0.37898 → n/a
- expert 55621328 (Master) · learning · v5→v8   Sweep different sets of rounding thresholds and also compare against naive rounding. Even small threshold changes can shift the metric substantially (±0.01–0.02). Use the leaderboard or a representative validation set to select the best cutpoints, and keep naive rounding as a baseline reference to c
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score n/a → 0.78266
- expert 55621328 (Master) · learning · v7→v8   Include a naive-rounding baseline (round to nearest integer) in the sweep. Compare its score against the best optimized thresholds. If naive rounding is substantially worse, continue investing in threshold optimization; if comparable, the effort is better spent elsewhere.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries.
    leaderboard score 0.78996 → 0.78266 (-0.00731)
- expert 55621328 (Master) · learning · v13→v14   Re-optimize the rounding thresholds on a validation set (or probe the leaderboard) every time the prediction distribution changes—such as after adding fold averaging or changing model size. Even small threshold adjustments can yield meaningful metric gains.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries.
    leaderboard score n/a → 0.80527
- expert 55621328 (Master) · learning · v17→v18   Do not carry over or manually guess rounding thresholds from one model to another. Re-optimize thresholds on a validation set produced by the new model. A large score drop after threshold transfer is a strong signal that the raw prediction distributions differ and thresholds must be re-derived.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score n/a → 0.70865
- expert 55621328 (Master) · learning · v28→v30   Always re-optimize the rounding thresholds after any checkpoint or model change. Expect that stale thresholds alone can account for a large fraction of an apparent score drop. Iterate threshold values (grid or optimization) before concluding the new checkpoint is inferior.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries.
    leaderboard score 0.78516 → 0.80353 (+0.01837)
- expert 55621328 (Master) · learning · v36→v37   Re-optimize rounding thresholds every time the underlying model or checkpoint changes, because the prediction distribution shifts. Use cross-validation or leaderboard probing to find thresholds; do not carry over thresholds from a different model without re-tuning.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries.
    leaderboard score 0.81031 → 0.81536 (+0.00505)
- expert 55621328 (Master) · learning · v57→v63   Test naive rounding as a baseline to quantify the value of optimized thresholds. Expect optimized thresholds to outperform naive rounding by a meaningful margin on rank-sensitive ordinal metrics. Keep the optimized rounding unless the simpler approach matches or exceeds it.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries.
    leaderboard score 0.80283 → 0.81174 (+0.00890)
- expert 55621328 (Master) · learning · v101→v102   After establishing a working inference pipeline, systematically adjust the rounding thresholds—especially compressing or expanding the upper and lower boundaries—and submit to measure sensitivity. Small threshold changes can shift the score meaningfully, so iterate on thresholds as a cheap post-proc
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries.
    leaderboard score n/a → 0.82366
- expert 55621328 (Master) · learning · v133→v134   Do not replace optimized thresholds with uniform spacing. The gap can be large (multiple percentage points on the metric). Always preserve and carry forward the tuned thresholds; if experimenting with new post-processing, keep the optimized thresholds as the fallback.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries.
    leaderboard score 0.82503 → 0.80343 (-0.02159)
- expert 55621328 (Master) · learning · v145→v146   Build an inference script that (1) averages predictions across multiple fold checkpoints to reduce variance, (2) optionally rescales predictions using statistics from out-of-fold data so the test prediction distribution matches training, and (3) applies pre-optimized rounding thresholds (tuned on OO
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score 0.81937 → 0.82442 (+0.00504)
- expert 55431616 (Grandmaster) · learning · v29→v30   Blend predictions from multiple gradient-boosted tree models trained with stratified cross-validation, then optimize rounding thresholds on the out-of-fold predictions to maximize the ordinal agreement metric. Use enough CV folds (e.g., 15) so the threshold optimization has a stable, representative 
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score n/a → 0.82433
- expert 59253662 (Contributor) · learning · v34→v36   Try a custom training objective that approximates the evaluation metric, and separately try data-driven threshold optimization on validation folds. Test each change independently. If neither improves validation or leaderboard score, revert to the simpler fixed-threshold approach—custom objectives ca
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score 0.81851 → 0.81826 (-0.00025)
- expert 59253662 (Contributor) · learning · v35→v36   Compare CV-optimized thresholds against fixed (e.g., evenly spaced or domain-informed) thresholds by submitting both. If the optimized thresholds do not improve or slightly hurt the leaderboard score, prefer the fixed thresholds—they are more robust when there is a distribution shift between trainin
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score n/a → 0.81826
- expert 58130512 (Master) · learning · v10→v12   Start with the simplest discretization (clip to valid range, round to nearest integer) and ensure the training objective is correct first. Add complexity to post-processing only after the baseline is stable, since elaborate remapping can mask or amplify errors in the loss function.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries.
    leaderboard score 0.79271 → 0.81929 (+0.02657)
- expert 58130512 (Master) · learning · v18→v19   Replace naive rounding with numerical optimization (e.g., simplex method minimizing negative metric) of the bin thresholds on out-of-fold predictions. This can recover much of the score that expensive features provided, at negligible cost.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score 0.81755 → 0.81927 (+0.00172)
- expert 58130512 (Master) · learning · v18→v19   Treat the bin boundaries as free parameters and optimize them on out-of-fold predictions using a derivative-free optimizer (e.g., Nelder–Mead) that directly minimizes the negative of the target metric. Apply the optimized thresholds to test predictions.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score 0.81755 → 0.81927 (+0.00172)
- expert 58130512 (Master) · learning · v28→v29   Optimize the rounding thresholds (one fewer than the number of classes) using a derivative-free optimizer (e.g., Nelder-Mead) that directly maximizes the evaluation metric on out-of-fold predictions. Fit thresholds on the subset whose distribution matches the test set, then apply the same thresholds
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score 0.81971 → 0.82105 (+0.00133)
- expert 58130512 (Master) · learning · v73→v77   Optimize the discretization thresholds on the validation subset whose label distribution matches the expected test distribution, not on the full validation set. Compare full-set optimization, subset optimization, and naive rounding to confirm which aligns best with the leaderboard.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint. | ✓ Groups or output columns show distinct calibration with adequate held-out sample counts.
    leaderboard score n/a → 0.82224
- expert 58130512 (Master) · learning · v96→v97   Try replacing optimized ordinal thresholds with simple clip-and-round as a baseline. If the simpler approach scores comparably or better on the leaderboard, the threshold optimization is overfitting and should be removed or regularized.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score 0.81933 → 0.82179 (+0.00245)
- expert 60197293 (Expert) · learning · v125→v127   Compare simple rounding (with clipping to the valid range) against optimized threshold binning. If threshold optimization is done without robust cross-validation, prefer simple rounding as the safer default.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score n/a → 0.81385
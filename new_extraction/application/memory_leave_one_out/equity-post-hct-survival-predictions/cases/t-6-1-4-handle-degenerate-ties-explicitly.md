# Handle degenerate ties explicitly  `T.6.1.4`   5 edits, 0 experts
1 scored cases, median improvement +0.00000, 0 improved


- expert 7018718 (Expert) · google · v37→v45   After discretization, check each column for degeneracy (all values identical). For any degenerate column, revert to the original continuous predictions. Prefer an exact constant-check over a variance threshold, as the threshold can be fragile. Also rescale surviving discretized columns to a standard
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Binning creates constant predictions or many ties in columns scored by a rank metric.
    leaderboard score n/a → 0.42580
- expert 7018718 (Expert) · google · v49→v50   After binning, check whether the result has more than one distinct value. If it has collapsed to a constant, fall back to the original continuous predictions for that column to preserve ranking information.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Binning creates constant predictions or many ties in columns scored by a rank metric.
    leaderboard score n/a → n/a
- expert 7548275 (Expert) · google · v14→v15   Add negligible random noise (e.g., Gaussian with standard deviation many orders of magnitude smaller than the prediction range) to break ties before submission. This preserves the intended ordering while ensuring the rank-based metric sees distinct values.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Binning creates constant predictions or many ties in columns scored by a rank metric.
    leaderboard score n/a → 0.00596
- expert 6803050 (Master) · google · v35→v39   Avoid adding random noise to predictions when the evaluation metric is rank-based, as it can only degrade signal. Clipping to avoid exact 0/1 is also unnecessary for rank metrics. Use raw model outputs or deterministic post-processing (e.g., quantile mapping) instead.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Binning creates constant predictions or many ties in columns scored by a rank metric.
    leaderboard score n/a → 0.38287
- expert 6803050 (Master) · google · v59→v60   Recognize that for rank-based metrics, replacing a group of predictions with any single constant produces identical ranks within that group. Focus tuning effort on the threshold boundary rather than the replacement value.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Binning creates constant predictions or many ties in columns scored by a rank metric.
    leaderboard score 0.39008 → 0.39008 (+0.00000)
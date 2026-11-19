# Test explicit tie handling  `T.7.2.4`   2 edits, 0 experts

- expert 7548275 (Expert) · google · v14→v15   Add negligible random noise (e.g., Gaussian with standard deviation many orders of magnitude smaller than the prediction range) to break ties before submission. This preserves the intended ordering while ensuring the rank-based metric sees distinct values.
    evidence: ✓ Targets occupy a finite ordered set and continuous outputs need a discrete mapping. | ✓ Outputs contain exact ties whose treatment differs across the metric or ranking implementation.
    leaderboard score n/a → 0.00596
- expert 6803050 (Master) · google · v35→v39   Avoid adding random noise to predictions when the evaluation metric is rank-based, as it can only degrade signal. Clipping to avoid exact 0/1 is also unnecessary for rank metrics. Use raw model outputs or deterministic post-processing (e.g., quantile mapping) instead.
    evidence: ✓ Targets occupy a finite ordered set and continuous outputs need a discrete mapping. | ✓ Outputs contain exact ties whose treatment differs across the metric or ranking implementation.
    leaderboard score n/a → 0.38287
# Use equal member weights  `T.7.3.1`   9 edits, 0 experts
5 scored cases, median improvement -0.00056, 1 improved


- expert 17616127 (Contributor) · commonlitreadabilityprize · v67→v68   Fall back to a simple equal-weight average of the strongest individual base models. When a complex stacking approach degrades performance, simplify first to re-establish a strong baseline, then add complexity incrementally.
    evidence: ✓ Members have comparable quality and tuned weights have not reliably improved the simple average. | ✓ Component quality differs reproducibly or a member’s predictions have changed since weights were tuned. | ✗ Model families contain unequal numbers of folds or variants.
    leaderboard score 0.46804 → n/a
- expert 18837555 (Expert) · commonlitreadabilityprize · v12→v13   Start with equal-weight (simple mean) averaging when adding a new member. Only deviate from equal weights if cross-validation on a sufficiently large held-out set clearly supports it; on small or noisy data, equal weighting is a robust default that avoids overfitting the blend coefficients.
    evidence: ✓ Members have comparable quality and tuned weights have not reliably improved the simple average. | ✓ Current weights depend on statistics of a very small or varying inference sample.
    leaderboard score 0.45714 → 0.45676 (-0.00038)
- expert 18851026 (Master) · commonlitreadabilityprize · v10→v11   Start with the simplest blend that already scores well. When adding more components and manually adjusting weights, submit and compare. If the new weights do not improve the score, revert to the previous blend rather than continuing to tune, because with a tiny evaluation set, small regressions like
    evidence: ✓ Model families contain unequal numbers of folds or variants. | ✓ Current weights depend on statistics of a very small or varying inference sample.
    leaderboard score 0.45773 → 0.45786 (+0.00013)
- expert 7670859 (Contributor) · google · v13→v15   Start with simple arithmetic averaging of prediction arrays, then iteratively add or remove sources while inspecting the distribution of blended predictions (e.g., histograms). If a source degrades the blend or has misaligned distributions, drop it. Use diagnostic plots at each step to verify that t
    evidence: ✓ Members have comparable quality and tuned weights have not reliably improved the simple average. | ✓ Component quality differs reproducibly or a member’s predictions have changed since weights were tuned.
    leaderboard score n/a → n/a
- expert 7573212 (Contributor) · google · v7→v8   Revert to equal-weight averaging and redirect effort to a different improvement lever (e.g., output post-processing or model diversity) rather than continuing to search over blend weights without reliable validation signal.
    evidence: ✓ Members have comparable quality and tuned weights have not reliably improved the simple average.
    leaderboard score 0.37898 → n/a
- expert 53747598 (Master) · hms · v28→v30   Start with equal weighting between the old and new components rather than keeping extreme weights. Equal weighting is a safer default when relative quality is unknown, and can be refined afterward based on leaderboard or validation feedback.
    evidence: ✓ Members have comparable quality and tuned weights have not reliably improved the simple average. | ✓ Component quality differs reproducibly or a member’s predictions have changed since weights were tuned.
    leaderboard score n/a → 0.22587
- expert 52860091 (Grandmaster) · hms · v27→v28   Try equal weighting when both members are similarly strong. Iteratively adjust weights in small increments (e.g., 0.1 steps) and submit. When individual model qualities converge after similar training procedures, equal blending often outperforms skewed weights because it maximizes diversity benefit.
    evidence: ✓ Members have comparable quality and tuned weights have not reliably improved the simple average.
    leaderboard score 0.26010 → 0.25703 (-0.00307)
- expert 15372370 (Expert) · ranzcr · v5→v6   Start with equal weights and keep test-time augmentation on. Only shift to non-uniform weights when per-model validation scores clearly justify it; arbitrary weighting and removing augmentation can hurt. If the weighted version scores worse on the leaderboard, revert to uniform averaging.
    evidence: ✗ Members have comparable quality and tuned weights have not reliably improved the simple average.
    leaderboard score 0.96726 → 0.96670 (-0.00056)
- expert 50496431 (Grandmaster) · hms · v101→v104   Reset to a simple equal-weight (mean) ensemble as a stable baseline. Then upgrade or swap individual members one at a time, re-adding each only after confirming it improves the mean blend. This isolates each member's contribution without introducing fragile weight tuning.
    evidence: ✓ Members have comparable quality and tuned weights have not reliably improved the simple average. | ✓ Component quality differs reproducibly or a member’s predictions have changed since weights were tuned. | ✓ Current weights depend on statistics of a very small or varying inference sample.
    leaderboard score 0.27434 → 0.27115 (-0.00318)
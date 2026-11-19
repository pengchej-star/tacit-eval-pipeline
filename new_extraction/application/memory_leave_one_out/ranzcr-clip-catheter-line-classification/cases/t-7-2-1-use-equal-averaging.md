# Use equal averaging  `T.7.2.1`   5 edits, 0 experts
2 scored cases, median improvement +0.00006, 1 improved


- expert 17616127 (Contributor) · commonlitreadabilityprize · v17→v18   Start with equal-weight averaging for fold-based members (similar expected quality). If members vary in validation performance, optimize weights on a held-out set or use a meta-learner. Always compare the chosen aggregation against the previous best before finalizing.
    evidence: ✓ Component quality is similar and fitted weights are unstable across validation folds. | ✗ Members predict class distributions and stored logits are available.
    leaderboard score n/a → 0.48999
- expert 17616127 (Contributor) · commonlitreadabilityprize · v59→v60   Test the hierarchical blend against the flat blend on the leaderboard. If the additional averaging layer does not improve the score, prefer the simpler flat blend — extra averaging tends to regress predictions toward the mean and can dilute the strongest individual signals when the component predict
    evidence: ✓ Component quality is similar and fitted weights are unstable across validation folds. | ✓ Components have unequal validated quality and their combination changes the metric.
    leaderboard score n/a → 0.45499
- expert 7573212 (Contributor) · google · v7→v8   Revert to equal-weight averaging and redirect effort to a different improvement lever (e.g., output post-processing or model diversity) rather than continuing to search over blend weights without reliable validation signal.
    evidence: ✓ Component quality is similar and fitted weights are unstable across validation folds. | ✗ Components have unequal validated quality and their combination changes the metric.
    leaderboard score 0.37898 → n/a
- expert 50496431 (Grandmaster) · hms · v101→v104   Reset to a simple equal-weight (mean) ensemble as a stable baseline. Then upgrade or swap individual members one at a time, re-adding each only after confirming it improves the mean blend. This isolates each member's contribution without introducing fragile weight tuning.
    evidence: ✓ Component quality is similar and fitted weights are unstable across validation folds. | ✓ Components have unequal validated quality and their combination changes the metric. | ✗ Leakage-free out-of-fold predictions and enough examples to fit a combiner are available. | ✓ Members predict class distributions and stored logits are available.
    leaderboard score 0.27434 → 0.27115 (-0.00318)
- expert 50496431 (Grandmaster) · hms · v200→v206   Test both simple averaging and weighted blending on the leaderboard. When removing members and switching to equal averaging consistently degrades the score, keep the weighted blend with all diverse members. Revert immediately if a simplification worsens the metric by a noticeable margin, as the dive
    evidence: ✓ Components have unequal validated quality and their combination changes the metric. | ✓ Members predict class distributions and stored logits are available. | ✗ Component quality is similar and fitted weights are unstable across validation folds.
    leaderboard score 0.22621 → 0.22628 (+0.00006)
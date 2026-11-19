# Use a uniform arithmetic average  `T.5.3.1`   9 edits, 0 experts
4 scored cases (improvement signed by each competition's direction), median +0.00261, 3 improved


- expert 17616127 · commonlitreadabilityprize · v17→v18   Start with equal-weight averaging for fold-based members (similar expected quality). If members vary in validation performance, optimize weights on a held-out set or use a meta-learner. Always compare the chosen aggregation against the previous best before finalizing.
    evidence: ✓ Members have similar quality or optimized combinations have unstable held-out gains. | ✗ Members differ in useful contribution and held-out predictions support weight comparisons. | ✗ Families have unequal numbers of checkpoints that would otherwise determine their influence.
    leaderboard score n/a → 0.48999 (lower is better)
- expert 17616127 · commonlitreadabilityprize · v64→v65   Test equal-weight averaging as a baseline. If it underperforms the tuned blend by a meaningful margin relative to the leaderboard granularity, invest in weight optimization (e.g., grid search or CV-based optimization) rather than defaulting to uniform weights.
    evidence: ✓ Members have similar quality or optimized combinations have unstable held-out gains.
    leaderboard score n/a → 0.45576 (lower is better)
- expert 17616127 · commonlitreadabilityprize · v67→v68   Fall back to a simple equal-weight average of the strongest individual base models. When a complex stacking approach degrades performance, simplify first to re-establish a strong baseline, then add complexity incrementally.
    evidence: ✓ Members have similar quality or optimized combinations have unstable held-out gains. | ✗ Enough OOF examples exist to learn stable complementary relationships among base outputs.
    leaderboard score 0.46804 → n/a (lower is better)
- expert 18523075 · commonlitreadabilityprize · v5→v7   When rebalancing after adding members, compare non-uniform (optimized) weights against uniform weights. If both degrade the score relative to the previous best, the new members may be hurting; revert to the previous composition and weights rather than forcing inclusion. Evaluate each configuration a
    evidence: ✓ Families have unequal numbers of checkpoints that would otherwise determine their influence. | ✗ Enough OOF examples exist to learn stable complementary relationships among base outputs. | ✓ Members have similar quality or optimized combinations have unstable held-out gains.
    leaderboard score 0.45684 → 0.45870 (lower is better; worse by 0.00187)
- expert 18426209 · commonlitreadabilityprize · v3→v5   Temporarily equalize weights among existing members, then after adding the new member, test dropping the weakest original member entirely. The new diverse member may replace rather than supplement the weakest existing one, yielding a better two-model blend than a three-model blend.
    evidence: ✗ Members differ in useful contribution and held-out predictions support weight comparisons. | ✓ Members have similar quality or optimized combinations have unstable held-out gains.
    leaderboard score 0.74137 → 0.46021 (lower is better; improved by 0.28116)
- expert 18837555 · commonlitreadabilityprize · v5→v6   Reset to a simple equal-weight average when adding new members, then re-optimize weights if needed. Equal averaging is a robust default that avoids overfitting blend weights on a small validation set.
    evidence: ✓ Members have similar quality or optimized combinations have unstable held-out gains. | ✗ Members differ in useful contribution and held-out predictions support weight comparisons.
    leaderboard score 0.46041 → n/a (lower is better)
- expert 7573212 · google · v7→v8   Revert to equal-weight averaging and redirect effort to a different improvement lever (e.g., output post-processing or model diversity) rather than continuing to search over blend weights without reliable validation signal.
    evidence: ✓ Members have similar quality or optimized combinations have unstable held-out gains. | ✗ Members differ in useful contribution and held-out predictions support weight comparisons.
    leaderboard score 0.37898 → n/a (higher is better)
- expert 55431616 · learning · v11→v13   Strip the ensemble back to the single stronger model, simplify infrastructure, and simultaneously improve the cross-validation scheme (use stratified folds for imbalanced/ordinal targets) and align the training objective with the evaluation metric. Evaluate the cleaner pipeline before re-adding comp
    evidence: none recorded
    leaderboard score 0.81502 → 0.81762 (higher is better; improved by 0.00261)
- expert 58130512 · learning · v102→v103   Try a weighted average where weights are derived from fold-level validation performance or tuned externally. Squaring the weights before normalizing concentrates influence on the best-performing folds. Compare against simple averaging and keep whichever scores better on the leaderboard.
    evidence: ✓ Members have similar quality or optimized combinations have unstable held-out gains. | ✓ Members differ in useful contribution and held-out predictions support weight comparisons.
    leaderboard score 0.82313 → 0.82432 (higher is better; improved by 0.00119)
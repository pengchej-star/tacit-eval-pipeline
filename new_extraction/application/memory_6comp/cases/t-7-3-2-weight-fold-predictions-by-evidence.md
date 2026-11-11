# Weight fold predictions by evidence  `T.7.3.2`   6 edits, 0 experts
5 scored cases, median improvement -0.00037, 1 improved


- expert 28093671 (Contributor) · amex · v42→v43   Compare the weighted combination against a simple equal-weight average on the held-out leaderboard. If the difference is negligible or the simple average is worse, keep the weighted version; the small drop (~0.0004 in this case) suggests custom weights can capture real per-fold quality differences a
    evidence: ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.79245 → 0.79208 (-0.00037)
- expert 27825577 (Expert) · amex · v3→v4   Record each fold's validation metric, then weight each fold's test predictions proportionally to its validation score when aggregating. This gives higher influence to better-performing folds.
    evidence: ✓ Fold quality differs consistently on comparable validation evidence. | ✗ The model has usable stochastic layers and repeated inference is intended to sample them. | ✗ Stochastic layers are active at inference without a validated repeated-pass strategy.
    leaderboard score 0.79384 → n/a
- expert 17616127 (Contributor) · commonlitreadabilityprize · v81→v85   For each fold, compute a weighted combination of the different models' predictions for that fold, then average the fold-level blended predictions with equal weight (1/number-of-folds). This preserves fold-specific signal diversity and can outperform a single global weighted average.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.45684 → 0.45142 (-0.00542)
- expert 7573212 (Contributor) · google · v3→v4   Try both uniform and quality-weighted averaging and compare on the leaderboard or a held-out set. If the difference is negligible, prefer the simpler uniform average to avoid overfitting to noisy fold-level metrics.
    evidence: ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.38325 → 0.38324 (-0.00001)
- expert 58130512 (Master) · learning · v91→v92   Test uniform averaging against the weighted version on the leaderboard. If the weighted version consistently scores higher, keep it; removing it for simplicity can cost meaningful performance, especially when the component models vary in quality.
    evidence: ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.82432 → 0.82158 (-0.00274)
- expert 58130512 (Master) · learning · v102→v103   Try a weighted average where weights are derived from fold-level validation performance or tuned externally. Squaring the weights before normalizing concentrates influence on the best-performing folds. Compare against simple averaging and keep whichever scores better on the leaderboard.
    evidence: ✓ Fold quality differs consistently on comparable validation evidence.
    leaderboard score 0.82313 → 0.82432 (+0.00119)
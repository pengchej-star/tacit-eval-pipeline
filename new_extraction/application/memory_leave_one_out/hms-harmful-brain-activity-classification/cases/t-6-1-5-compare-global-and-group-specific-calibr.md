# Compare global and group-specific calibration  `T.6.1.5`   3 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00307, 2 improved


- expert 7548275 · google · v23→v26   Start with a manually chosen subset of columns where the transformation is most justified (e.g., columns with clearly discrete structure). Avoid applying it globally. Then incrementally add columns one at a time, submitting after each addition, and keep only those that improve the metric. Stop when 
    evidence: ✓ Residual distributions differ reproducibly across groups available at inference. | ✓ The metric depends on order and proposed transformations only erase or perturb useful ordering.
    leaderboard score 0.42142 → 0.42449 (higher is better; improved by 0.00307)
- expert 55621328 · learning · v72→v74   Train a separate classifier to predict the subgroup, then apply per-group rounding thresholds. If the subgroup classifier is imperfect, errors in group assignment propagate into worse thresholds, often degrading the overall metric. Verify on the leaderboard or a held-out set; if the score drops, rev
    evidence: ✓ Residual distributions differ reproducibly across groups available at inference. | ✓ Continuous outputs carry signal but fixed cutpoints systematically misallocate ordinal labels. | ✓ Target-level frequencies are stable enough that a reference distribution may improve mapping. | ✓ Previously optimized cutpoints fail to improve a separate held-out set.
    leaderboard score 0.82142 → 0.81373 (higher is better; worse by 0.00769)
- expert 55621328 · learning · v74→v76   Revert the per-group post-processing and return to a single global calibration. When group-specific tuning hurts, it usually means the groups are too small or the test distribution differs from training; prefer the simpler global approach unless there is strong evidence of distinct subpopulations in
    evidence: ✓ Residual distributions differ reproducibly across groups available at inference. | ✓ Previously optimized cutpoints fail to improve a separate held-out set.
    leaderboard score 0.81373 → 0.82461 (higher is better; improved by 0.01088)
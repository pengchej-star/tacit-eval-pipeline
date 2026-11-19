# Use subgroup-specific cutpoints  `T.7.2.3`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.01088, 1 improved


- expert 55621328 · learning · v72→v74   Train a separate classifier to predict the subgroup, then apply per-group rounding thresholds. If the subgroup classifier is imperfect, errors in group assignment propagate into worse thresholds, often degrading the overall metric. Verify on the leaderboard or a held-out set; if the score drops, rev
    evidence: ✓ Targets occupy a finite ordered set and continuous outputs need a discrete mapping. | ✓ Large identifiable subgroups have different held-out calibration curves. | ✓ Training and expected test label frequencies differ. | ✓ The expected test label proportions are credibly stable relative to training. | ✓ Subgroup assignment is noisy or each subgroup has few calibration examples.
    leaderboard score 0.82142 → 0.81373 (higher is better; worse by 0.00769)
- expert 55621328 · learning · v74→v76   Revert the per-group post-processing and return to a single global calibration. When group-specific tuning hurts, it usually means the groups are too small or the test distribution differs from training; prefer the simpler global approach unless there is strong evidence of distinct subpopulations in
    evidence: ✓ Targets occupy a finite ordered set and continuous outputs need a discrete mapping. | ✗ Large identifiable subgroups have different held-out calibration curves. | ✓ Subgroup assignment is noisy or each subgroup has few calibration examples. | ✓ Training and expected test label frequencies differ. | ✓ The expected test label proportions are credibly stable relative to training.
    leaderboard score 0.81373 → 0.82461 (higher is better; improved by 0.01088)
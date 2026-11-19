# Match discrete label frequencies  `T.7.2.2`   3 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00000, 1 improved


- expert 6803050 · google · v12→v17   Implement per-target quantile mapping: compute cumulative frequencies of each discrete level in training, then assign each test prediction to the level whose cumulative frequency bracket contains the prediction's percentile rank. This can only help when the base model already produces meaningful ord
    evidence: ✓ Targets occupy a finite ordered set and continuous outputs need a discrete mapping.
    leaderboard score -0.00372 → -0.00372 (higher is better; unchanged by 0.00000)
- expert 6803050 · google · v22→v23   Apply quantile mapping or nearest-level rounding to snap ensemble-averaged predictions onto the discrete values observed in training. This aligns predicted ranks with the true rank structure and typically improves rank-based metrics. Validate by comparing submissions with and without the mapping.
    evidence: ✓ Targets occupy a finite ordered set and continuous outputs need a discrete mapping.
    leaderboard score 0.35115 → 0.38182 (higher is better; improved by 0.03067)
- expert 55621328 · learning · v63→v68   Sort all test predictions by their continuous value and assign discrete labels so cumulative counts match the expected distribution. Compare the resulting metric against per-sample optimized-threshold rounding. Be aware that distribution matching ignores per-sample confidence and can hurt metrics th
    evidence: ✓ Targets occupy a finite ordered set and continuous outputs need a discrete mapping. | ✓ The expected test label proportions are credibly stable relative to training. | ✓ Training and expected test label frequencies differ.
    leaderboard score 0.81174 → 0.81082 (higher is better; worse by 0.00092)
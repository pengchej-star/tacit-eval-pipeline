# Test target-frequency mapping  `T.6.1.4`   4 edits, 0 experts
3 scored cases, median improvement +0.00000, 1 improved


- expert 6803050 (Master) · google · v12→v17   Implement per-target quantile mapping: compute cumulative frequencies of each discrete level in training, then assign each test prediction to the level whose cumulative frequency bracket contains the prediction's percentile rank. This can only help when the base model already produces meaningful ord
    evidence: ✓ Previously optimized cutpoints fail to improve a separate held-out set. | ✓ Target-level frequencies are stable enough that a reference distribution may improve mapping. | ✓ The metric depends on order and proposed transformations only erase or perturb useful ordering.
    leaderboard score -0.00372 → -0.00372 (+0.00000)
- expert 6803050 (Master) · google · v22→v23   Apply quantile mapping or nearest-level rounding to snap ensemble-averaged predictions onto the discrete values observed in training. This aligns predicted ranks with the true rank structure and typically improves rank-based metrics. Validate by comparing submissions with and without the mapping.
    evidence: ✓ Target-level frequencies are stable enough that a reference distribution may improve mapping. | ✗ Previously optimized cutpoints fail to improve a separate held-out set.
    leaderboard score 0.35115 → 0.38182 (+0.03067)
- expert 6803050 (Master) · google · v47→v48   Test the postprocessing on each new model configuration separately rather than assuming it always helps. When model outputs are less well-calibrated, discretization can introduce ties that hurt rank correlation. Compare submitted scores with and without the postprocessing for each ensemble variant.
    evidence: ✓ The metric depends on order and proposed transformations only erase or perturb useful ordering. | ✓ Target-level frequencies are stable enough that a reference distribution may improve mapping.
    leaderboard score n/a → 0.37184
- expert 55621328 (Master) · learning · v63→v68   Sort all test predictions by their continuous value and assign discrete labels so cumulative counts match the expected distribution. Compare the resulting metric against per-sample optimized-threshold rounding. Be aware that distribution matching ignores per-sample confidence and can hurt metrics th
    evidence: ✓ Target-level frequencies are stable enough that a reference distribution may improve mapping. | ✓ Previously optimized cutpoints fail to improve a separate held-out set. | ✓ Residual distributions differ reproducibly across groups available at inference.
    leaderboard score 0.81174 → 0.81082 (-0.00092)
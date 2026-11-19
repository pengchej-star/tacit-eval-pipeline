# Match a supported label distribution  `T.6.1.2`   5 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00000, 1 improved


- expert 6803050 · google · v12→v17   Implement per-target quantile mapping: compute cumulative frequencies of each discrete level in training, then assign each test prediction to the level whose cumulative frequency bracket contains the prediction's percentile rank. This can only help when the base model already produces meaningful ord
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Binning creates constant predictions or many ties in columns scored by a rank metric.
    leaderboard score -0.00372 → -0.00372 (higher is better; unchanged by 0.00000)
- expert 6803050 · google · v22→v23   Apply quantile mapping or nearest-level rounding to snap ensemble-averaged predictions onto the discrete values observed in training. This aligns predicted ranks with the true rank structure and typically improves rank-based metrics. Validate by comparing submissions with and without the mapping.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score 0.35115 → 0.38182 (higher is better; improved by 0.03067)
- expert 6803050 · google · v47→v48   Test the postprocessing on each new model configuration separately rather than assuming it always helps. When model outputs are less well-calibrated, discretization can introduce ties that hurt rank correlation. Compare submitted scores with and without the postprocessing for each ensemble variant.
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Binning creates constant predictions or many ties in columns scored by a rank metric.
    leaderboard score n/a → 0.37184 (higher is better)
- expert 55621328 · learning · v63→v68   Sort all test predictions by their continuous value and assign discrete labels so cumulative counts match the expected distribution. Compare the resulting metric against per-sample optimized-threshold rounding. Be aware that distribution matching ignores per-sample confidence and can hurt metrics th
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score 0.81174 → 0.81082 (higher is better; worse by 0.00092)
- expert 55621328 · learning · v131→v134   If rounding thresholds are already optimized on the same fold predictions used to fit the scaler, adding a distribution-matching normalization step is redundant and can hurt. Test this only when there is evidence of a genuine distribution shift between OOF and test predictions, and verify on a held-
    evidence: ✓ Labels are ordered discrete values and continuous errors cross meaningful class boundaries. | ✓ Held-out and expected test label frequencies are stable enough to justify a distribution constraint.
    leaderboard score n/a → 0.80343 (higher is better)
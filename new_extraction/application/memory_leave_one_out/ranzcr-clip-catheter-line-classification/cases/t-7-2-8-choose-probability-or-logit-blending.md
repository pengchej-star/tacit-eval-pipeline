# Choose probability or logit blending  `T.7.2.8`   3 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00102, 3 improved


- expert 53747598 · hms · v15→v21   Export pre-softmax logits from each model, compute the weighted average in logit space, then apply softmax to obtain the final distribution. Compare this against probability-space averaging on the leaderboard. Logit-space averaging often yields a better-calibrated blend for log-based or divergence m
    evidence: ✓ Members predict class distributions and stored logits are available. | ✓ The metric depends on ordering and member outputs have incompatible scales or outliers.
    leaderboard score 0.22838 → 0.22689 (lower is better; improved by 0.00149)
- expert 50496431 · hms · v16→v17   Move TTA duplication, softmax, and averaging into the model's forward pass so that every inference call returns fully normalized, TTA-averaged probabilities. This ensures softmax is applied before averaging (averaging probabilities rather than logits) and eliminates mismatches between training and i
    evidence: ✓ Members predict class distributions and stored logits are available.
    leaderboard score 0.34815 → 0.34713 (lower is better; improved by 0.00102)
- expert 50496431 · hms · v192→v200   Sweep over ensemble subsets and weighting schemes by alternating between simple averaging and hand-tuned weighted blends. Include all diverse members rather than pruning to a small subset, and assign higher weight to the single strongest individual model. Evaluate each configuration on the leaderboa
    evidence: ✓ Components have unequal validated quality and their combination changes the metric. | ✓ Members predict class distributions and stored logits are available. | ✓ Component quality is similar and fitted weights are unstable across validation folds. | ✓ The auxiliary source is substantially weaker than the established baseline.
    leaderboard score 0.22694 → 0.22621 (lower is better; improved by 0.00073)
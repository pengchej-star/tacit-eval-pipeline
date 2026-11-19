# Average within families before blending  `T.5.3.6`   4 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00542, 2 improved


- expert 27502740 · amex · v6→v8   Before committing, compare the OOF metric of the manual blend against the original single-pipeline OOF metric. If the manual blend does not improve OOF, do not submit—it likely means the AutoML's internal combination was already near-optimal for that algorithm mix. Reserve manual blending for genuin
    evidence: ✓ Families have unequal numbers of checkpoints that would otherwise determine their influence. | ✓ Enough OOF examples exist to learn stable complementary relationships among base outputs. | ✓ The available meta-features contain in-sample predictions or have unverifiable fold provenance.
    leaderboard score 0.79501 → 0.79461 (higher is better; worse by 0.00040)
- expert 17616127 · commonlitreadabilityprize · v20→v27   First average the homogeneous fold-level predictions into a single group prediction to avoid over-representing one family. Then blend the group prediction with predictions from other architectures and the meta-model using a small weighted average. Sweep the weights and membership (add/remove members
    evidence: ✓ Families have unequal numbers of checkpoints that would otherwise determine their influence. | ✓ Enough OOF examples exist to learn stable complementary relationships among base outputs. | ✓ Members differ in useful contribution and held-out predictions support weight comparisons.
    leaderboard score 0.48052 → 0.45549 (lower is better; improved by 0.02503)
- expert 17616127 · commonlitreadabilityprize · v59→v60   Test the hierarchical blend against the flat blend on the leaderboard. If the additional averaging layer does not improve the score, prefer the simpler flat blend — extra averaging tends to regress predictions toward the mean and can dilute the strongest individual signals when the component predict
    evidence: ✓ Members differ in useful contribution and held-out predictions support weight comparisons. | ✓ Families have unequal numbers of checkpoints that would otherwise determine their influence.
    leaderboard score n/a → 0.45499 (lower is better)
- expert 17616127 · commonlitreadabilityprize · v81→v85   For each fold, compute a weighted combination of the different models' predictions for that fold, then average the fold-level blended predictions with equal weight (1/number-of-folds). This preserves fold-specific signal diversity and can outperform a single global weighted average.
    evidence: ✓ Families have unequal numbers of checkpoints that would otherwise determine their influence.
    leaderboard score 0.45684 → 0.45142 (lower is better; improved by 0.00542)
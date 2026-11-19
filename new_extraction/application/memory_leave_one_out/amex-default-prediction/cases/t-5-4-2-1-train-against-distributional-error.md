# Train against distributional error  `T.5.4.2.1`   1 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.02644, 1 improved


- expert 49576186 · hms · v68→v70   Replace the surrogate loss with the actual evaluation metric (or its differentiable equivalent) as the training objective. When the metric is a divergence between distributions and labels are already soft distributions, train directly with that divergence as the loss function.
    evidence: ✓ Targets are probability distributions and the evaluation uses distributional divergence. | ✗ Outputs are independent labels or bounded independent targets rather than mutually exclusive classes.
    leaderboard score 0.37990 → 0.35346 (lower is better; improved by 0.02644)
# Average compatible weights  `T.5.1.3`   1 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00016, 1 improved


- expert 18550705 · commonlitreadabilityprize · v10→v11   Apply stochastic weight averaging to each constituent model's checkpoints before inference. This smooths the loss landscape and reduces variance of individual model predictions, which can translate to a small ensemble-level improvement.
    evidence: ✓ Several nearby snapshots from the same parameterization are available. | ✗ The candidate snapshots come from different architectures or unrelated initializations.
    leaderboard score 0.45300 → 0.45284 (lower is better; improved by 0.00016)
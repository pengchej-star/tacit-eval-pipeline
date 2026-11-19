# Average model weights  `T.5.3.4`   1 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00016, 1 improved


- expert 18550705 · commonlitreadabilityprize · v10→v11   Apply stochastic weight averaging to each constituent model's checkpoints before inference. This smooths the loss landscape and reduces variance of individual model predictions, which can translate to a small ensemble-level improvement.
    evidence: ✗ A known spatial or channel symmetry preserves the target. | ✓ Compatible snapshots from the same architecture and training trajectory are available. | ✓ The marginal gain from the proposed TTA variation has not yet been measured for the current model/ensemble configuration. | ✗ The proposed TTA variation was previously tried and caused a score regression. | ✓ The proposed TTA technique is a standard approach used in strong public solutions for this competition.
    leaderboard score 0.45300 → 0.45284 (lower is better; improved by 0.00016)
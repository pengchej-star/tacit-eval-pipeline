# Average compatible model weights  `T.7.3.6`   1 edits, 0 experts
1 scored cases, median improvement -0.00016, 0 improved


- expert 18550705 (Master) · commonlitreadabilityprize · v10→v11   Apply stochastic weight averaging to each constituent model's checkpoints before inference. This smooths the loss landscape and reduces variance of individual model predictions, which can translate to a small ensemble-level improvement.
    evidence: ✓ Several compatible training snapshots of one model are available for weight averaging.
    leaderboard score 0.45300 → 0.45284 (-0.00016)
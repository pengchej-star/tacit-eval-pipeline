# Train pairwise ordering  `T.5.4.2.3`   1 edits, 0 experts
1 scored cases, median improvement +0.00010, 1 improved


- expert 75145694 (Expert) · equity · v32→v33   Implement a pairwise ranking loss (optionally with focal weighting to emphasize hard pairs) for a tabular neural network with categorical embeddings. Add it as a new ensemble member. Expect a small but positive marginal gain from the loss-metric alignment, mainly through diversity in the blend.
    evidence: ✗ Targets are probability distributions and the evaluation uses distributional divergence. | ✓ The metric rewards pair ordering while training uses only pointwise errors. | ✗ Labels occupy an ordered finite scale.
    leaderboard score 0.69285 → 0.69296 (+0.00010)
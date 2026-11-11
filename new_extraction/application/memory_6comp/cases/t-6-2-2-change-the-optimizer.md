# Change the optimizer  `T.6.2.2`   2 edits, 0 experts
2 scored cases, median improvement +0.00034, 1 improved


- expert 77129691 (Master) · equity · v20→v22   Try the alternative optimizer and note the leaderboard change. If it regresses, revert to the original optimizer but use the experiment as an opportunity to re-tune learning rate, epoch count, and batch size around the original optimizer. The act of experimenting often reveals that the original opti
    evidence: ✓ Stable learning-rate trials have plateaued with the same optimizer. | ✓ Multiple hyperparameters were changed simultaneously in a previous edit, so individual effects are confounded and need isolated testing.
    leaderboard score 0.69534 → 0.69568 (+0.00034)
- expert 6803050 (Master) · google · v23→v24   Swap in the alternative checkpoints with no other changes, compare the leaderboard score, and revert if the score is worse. Isolate exactly one variable (the checkpoint variant) per submission to get a clean signal.
    evidence: ✓ Stable learning-rate trials have plateaued with the same optimizer. | ✓ Multiple hyperparameters were changed simultaneously in a previous edit, so individual effects are confounded and need isolated testing.
    leaderboard score 0.38182 → 0.37058 (-0.01124)
# Compare optimizer or learning-rate schedule  `T.4.3.5`   3 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00034, 2 improved


- expert 77450317 · equity · v16→v17   Try switching from a smooth continuous schedule (e.g., cosine annealing) to a stepped schedule that holds the learning rate constant for several epochs then drops it at predefined milestones. Apply the schedule at epoch granularity and add a toggle flag so you can A/B test with and without the sched
    evidence: ✗ Training fit or the train-validation gap suggests an inappropriate tree capacity. | ✓ Convergence behavior suggests the current optimization schedule is a bottleneck. | ✗ The current boosting mode (e.g., DART) makes early-stopping callbacks unreliable, requiring manual iteration tuning. | ✓ Multiple hyperparameters are being changed simultaneously without isolating individual effects.
    leaderboard score 0.69671 → 0.69690 (higher is better; improved by 0.00019)
- expert 77129691 · equity · v20→v22   Try the alternative optimizer and note the leaderboard change. If it regresses, revert to the original optimizer but use the experiment as an opportunity to re-tune learning rate, epoch count, and batch size around the original optimizer. The act of experimenting often reveals that the original opti
    evidence: ✓ Convergence behavior suggests the current optimization schedule is a bottleneck. | ✓ Multiple hyperparameters are being changed simultaneously without isolating individual effects.
    leaderboard score 0.69534 → 0.69568 (higher is better; improved by 0.00034)
- expert 77276039 · equity · v18→v21   Avoid bundling many changes (optimizer swap, scheduler addition, encoding change, hyperparameter tuning) into a single submission. When the combined result regresses, it is impossible to identify which change helped or hurt. Instead, change one lever at a time and measure its effect before adding th
    evidence: ✓ GPU training caused instability or errors requiring fallback to CPU. | ✓ Multiple hyperparameters are being changed simultaneously without isolating individual effects. | ✗ GPU acceleration is available and would meaningfully speed up training iterations.
    leaderboard score n/a → 0.69037 (higher is better)
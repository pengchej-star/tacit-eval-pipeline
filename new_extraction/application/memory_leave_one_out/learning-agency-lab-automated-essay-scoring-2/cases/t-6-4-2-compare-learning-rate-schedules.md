# Compare learning-rate schedules  `T.6.4.2`   1 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00019, 1 improved


- expert 77450317 · equity · v16→v17   Try switching from a smooth continuous schedule (e.g., cosine annealing) to a stepped schedule that holds the learning rate constant for several epochs then drops it at predefined milestones. Apply the schedule at epoch granularity and add a toggle flag so you can A/B test with and without the sched
    evidence: ✓ Convergence stalls around the current decay schedule’s transitions. | ✗ A recent change to the loss function or architecture invalidates previously tuned hyperparameters, requiring re-tuning of LR and regularization.
    leaderboard score 0.69671 → 0.69690 (higher is better; improved by 0.00019)
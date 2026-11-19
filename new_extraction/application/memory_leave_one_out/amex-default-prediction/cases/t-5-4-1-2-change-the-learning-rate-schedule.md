# Change the learning-rate schedule  `T.5.4.1.2`   1 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00019, 1 improved


- expert 77450317 · equity · v16→v17   Try switching from a smooth continuous schedule (e.g., cosine annealing) to a stepped schedule that holds the learning rate constant for several epochs then drops it at predefined milestones. Apply the schedule at epoch granularity and add a toggle flag so you can A/B test with and without the sched
    evidence: ✓ Progress stalls or deteriorates at a specific schedule transition. | ✗ The proposed edit changes only one hyperparameter at a time, consistent with controlled experimentation.
    leaderboard score 0.69671 → 0.69690 (higher is better; improved by 0.00019)
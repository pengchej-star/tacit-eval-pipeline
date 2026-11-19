# Train with validated pseudo-labels  `T.5.1.3`   2 edits, 0 experts
2 scored cases, median improvement -0.00304, 0 improved


- expert 52860091 (Grandmaster) · hms · v26→v27   Swap in the enhanced-training checkpoints for the second architecture and measure the ensemble score. Techniques that leverage unlabeled data or soft labels tend to generalize across architectures on the same task, so the upgrade is usually beneficial and worth testing early.
    evidence: ✓ Unlabeled examples and a pseudo-labeling procedure already improved another comparable member. | ✗ The competition metric is rank-based or otherwise insensitive to the class-weight direction being explored. | ✗ Previous filtering or data-selection changes regressed the score, suggesting the current selection should be reverted or refined rather than extended.
    leaderboard score 0.26613 → 0.26010 (-0.00603)
- expert 52860091 (Grandmaster) · hms · v38→v43   Retrain the weak member using the same semi-supervised (pseudo-labeling) pipeline that benefited existing members. If pseudo-labeling consistently helped other architectures in the same competition, it is likely to help the new architecture as well, making it a viable ensemble component.
    evidence: ✓ Unlabeled examples and a pseudo-labeling procedure already improved another comparable member. | ✗ The competition metric is rank-based or otherwise insensitive to the class-weight direction being explored. | ✗ Previous filtering or data-selection changes regressed the score, suggesting the current selection should be reverted or refined rather than extended.
    leaderboard score 0.25910 → 0.25606 (-0.00304)
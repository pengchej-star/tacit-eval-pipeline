# Enforce required output ranges  `T.7.3.3`   3 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median -0.00437, 0 improved


- expert 6803050 · google · v9→v10   Apply per-column min-max normalization so each column's predictions span [0,1]. This is a safe first baseline: it satisfies format constraints and preserves within-column ranks perfectly, which is all a rank-correlation metric needs.
    evidence: ✓ Predictions violate the required range or do not sum to one for a distributional task. | ✓ The metric only uses within-column rank and no later blend or rounding depends on magnitude.
    leaderboard score n/a → -0.00372 (higher is better)
- expert 50376011 · hms · v2→v3   Test submitting both with and without an extra softmax normalization. If the metric penalizes miscalibration (e.g., KL divergence), removing redundant softmax often helps. Keep whichever version scores better.
    evidence: ✓ Predictions violate the required range or do not sum to one for a distributional task. | ✗ The metric only uses within-column rank and no later blend or rounding depends on magnitude.
    leaderboard score n/a → 0.49067 (lower is better)
- expert 52551258 · hms · v3→v4   Always normalize averaged probability predictions to sum to 1 before submission when the metric is a divergence or log-likelihood. However, change only one thing at a time so the effect of normalization can be isolated from other modifications.
    evidence: ✓ Predictions violate the required range or do not sum to one for a distributional task. | ✗ The metric only uses within-column rank and no later blend or rounding depends on magnitude.
    leaderboard score 0.37116 → 0.37553 (lower is better; worse by 0.00437)
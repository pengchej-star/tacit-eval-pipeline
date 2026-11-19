# Choose probability or logit-space aggregation  `T.6.2.1.3`   6 edits, 0 experts
5 scored cases (improvement signed by each competition's direction), median +0.00073, 4 improved


- expert 53747598 · hms · v15→v21   Export pre-softmax logits from each model, compute the weighted average in logit space, then apply softmax to obtain the final distribution. Compare this against probability-space averaging on the leaderboard. Logit-space averaging often yields a better-calibrated blend for log-based or divergence m
    evidence: ✓ The task scores probability distributions and logits are available before normalization. | ✗ Rank-space averaging has consistently produced the best leaderboard scores across recent iterations.
    leaderboard score 0.22838 → 0.22689 (lower is better; improved by 0.00149)
- expert 50376011 · hms · v2→v3   Test submitting both with and without an extra softmax normalization. If the metric penalizes miscalibration (e.g., KL divergence), removing redundant softmax often helps. Keep whichever version scores better.
    evidence: ✓ The task scores probability distributions and logits are available before normalization. | ✗ The upstream model changed after the last raw-versus-rank comparison.
    leaderboard score n/a → 0.49067 (lower is better)
- expert 50376011 · hms · v112→v113   Apply the softmax (or other normalization) to each individual model's output before averaging across ensemble members, so that the ensemble operates in probability space. Verify by comparing leaderboard or validation scores against the alternative order, and keep whichever is better.
    evidence: ✓ The task scores probability distributions and logits are available before normalization. | ✗ The upstream model changed after the last raw-versus-rank comparison.
    leaderboard score 0.30121 → 0.30077 (lower is better; improved by 0.00044)
- expert 52551258 · hms · v3→v4   Always normalize averaged probability predictions to sum to 1 before submission when the metric is a divergence or log-likelihood. However, change only one thing at a time so the effect of normalization can be isolated from other modifications.
    evidence: ✓ The task scores probability distributions and logits are available before normalization.
    leaderboard score 0.37116 → 0.37553 (lower is better; worse by 0.00437)
- expert 50496431 · hms · v16→v17   Move TTA duplication, softmax, and averaging into the model's forward pass so that every inference call returns fully normalized, TTA-averaged probabilities. This ensures softmax is applied before averaging (averaging probabilities rather than logits) and eliminates mismatches between training and i
    evidence: ✗ The metric depends on ordering and members use incompatible output scales or target transforms. | ✓ The task scores probability distributions and logits are available before normalization.
    leaderboard score 0.34815 → 0.34713 (lower is better; improved by 0.00102)
- expert 50496431 · hms · v192→v200   Sweep over ensemble subsets and weighting schemes by alternating between simple averaging and hand-tuned weighted blends. Include all diverse members rather than pruning to a small subset, and assign higher weight to the single strongest individual model. Evaluate each configuration on the leaderboa
    evidence: ✓ The task scores probability distributions and logits are available before normalization. | ✗ Rank-space averaging has consistently produced the best leaderboard scores across recent iterations. | ✓ The upstream model changed after the last raw-versus-rank comparison. | ✓ The last raw-versus-rank comparison is confounded by an unrelated change (member subset, untuned weights, or a code bug), making the result unreliable.
    leaderboard score 0.22694 → 0.22621 (lower is better; improved by 0.00073)
# Compare logit and probability pooling  `T.6.3.5`   3 edits, 0 experts
2 scored cases, median improvement -0.00044, 0 improved


- expert 53747598 (Master) · hms · v15→v21   Export pre-softmax logits from each model, compute the weighted average in logit space, then apply softmax to obtain the final distribution. Compare this against probability-space averaging on the leaderboard. Logit-space averaging often yields a better-calibrated blend for log-based or divergence m
    evidence: ✓ Models output class distributions and confidence differs across members. | ✗ The metric is ranking-based and member prediction scales or calibrations differ. | ✓ Probability tails or output scale differences dominate an arithmetic blend.
    leaderboard score 0.22838 → 0.22689 (-0.00149)
- expert 50376011 (Grandmaster) · hms · v2→v3   Test submitting both with and without an extra softmax normalization. If the metric penalizes miscalibration (e.g., KL divergence), removing redundant softmax often helps. Keep whichever version scores better.
    evidence: ✓ Models output class distributions and confidence differs across members. | ✓ Probability tails or output scale differences dominate an arithmetic blend.
    leaderboard score n/a → 0.49067
- expert 50376011 (Grandmaster) · hms · v112→v113   Apply the softmax (or other normalization) to each individual model's output before averaging across ensemble members, so that the ensemble operates in probability space. Verify by comparing leaderboard or validation scores against the alternative order, and keep whichever is better.
    evidence: ✗ The metric is ranking-based and member prediction scales or calibrations differ. | ✓ Models output class distributions and confidence differs across members. | ✓ The only evaluation feedback is a small public subset and many weights have already been tried.
    leaderboard score 0.30121 → 0.30077 (-0.00044)
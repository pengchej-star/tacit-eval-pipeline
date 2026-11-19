# Choose logits or probabilities  `T.6.3.4`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00149, 2 improved


- expert 53747598 · hms · v15→v21   Export pre-softmax logits from each model, compute the weighted average in logit space, then apply softmax to obtain the final distribution. Compare this against probability-space averaging on the leaderboard. Logit-space averaging often yields a better-calibrated blend for log-based or divergence m
    evidence: ✓ Models expose both logits and probabilities and the metric evaluates distributions.
    leaderboard score 0.22838 → 0.22689 (lower is better; improved by 0.00149)
- expert 50376011 · hms · v112→v113   Apply the softmax (or other normalization) to each individual model's output before averaging across ensemble members, so that the ensemble operates in probability space. Verify by comparing leaderboard or validation scores against the alternative order, and keep whichever is better.
    evidence: ✓ Models expose both logits and probabilities and the metric evaluates distributions.
    leaderboard score 0.30121 → 0.30077 (lower is better; improved by 0.00044)
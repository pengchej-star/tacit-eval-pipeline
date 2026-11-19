# Average logits before softmax  `T.7.4.5`   1 edits, 0 experts
1 scored cases, median improvement -0.00149, 0 improved


- expert 53747598 (Master) · hms · v15→v21   Export pre-softmax logits from each model, compute the weighted average in logit space, then apply softmax to obtain the final distribution. Compare this against probability-space averaging on the leaderboard. Logit-space averaging often yields a better-calibrated blend for log-based or divergence m
    evidence: ✗ The metric is rank-based and member score distributions differ in calibration or scale. | ✓ Compatible pre-softmax logits are available and the task scores categorical probability distributions. | ✗ With only one model source, rank averaging is a no-op or potentially harmful compared to raw predictions. | ✓ Simple weight tuning of the arithmetic blend has already been tried and yielded only marginal improvement. | ✓ An alternative blend strategy (e.g., sigmoid, logit-space) was implemented but never scored on the leaderboard.
    leaderboard score 0.22838 → 0.22689 (-0.00149)
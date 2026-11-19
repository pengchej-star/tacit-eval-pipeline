# Use a validated auxiliary prediction  `T.8.4.1`   7 edits, 0 experts
4 scored cases, median improvement +0.00010, 3 improved


- expert 17616127 (Contributor) · commonlitreadabilityprize · v109→v111   Build a confidence-gated correction step: run the classification model on test data, apply softmax to get per-bin probabilities, take the argmax as the predicted bin, and when the classification confidence exceeds a tunable threshold, shift the regression prediction toward the bin center. Start with
    evidence: ✓ An auxiliary classifier or head gives held-out information not captured by the main prediction. | ✓ The current post-processing was tuned for older checkpoints or its contribution is unverified.
    leaderboard score 0.44854 → n/a
- expert 73671444 (Grandmaster) · equity · v25→v26   Try combining an event-indicator prediction with a time-to-event prediction (e.g., dividing event probability by exponentiated log-time) to create a hazard-like risk score. Evaluate whether this ad-hoc combination improves over using either prediction alone. If the gain is marginal compared to the f
    evidence: ✓ An auxiliary classifier or head gives held-out information not captured by the main prediction. | ✓ The current post-processing was tuned for older checkpoints or its contribution is unverified.
    leaderboard score n/a → 0.68463
- expert 77347591 (Expert) · equity · v1→v2   Probe the additive correction magnitude by halving it and checking the leaderboard or validation metric. If the score worsens, revert to the original value (or try increasing it). Small probes around the current value reveal whether the correction is too large or too small without risking a large sc
    evidence: ✓ An auxiliary classifier or head gives held-out information not captured by the main prediction. | ✓ The current post-processing was tuned for older checkpoints or its contribution is unverified.
    leaderboard score 0.69330 → 0.69321 (-0.00009)
- expert 77347591 (Expert) · equity · v20→v22   Apply the subset adjustment as a direct additive offset to the final blended prediction rather than manipulating individual model ranks before averaging. This preserves the ensemble's rank structure for unflagged samples while cleanly separating flagged ones. Tune the offset magnitude in small incre
    evidence: ✓ An auxiliary classifier or head gives held-out information not captured by the main prediction. | ✓ The current post-processing was tuned for older checkpoints or its contribution is unverified.
    leaderboard score 0.69411 → 0.69416 (+0.00005)
- expert 75145694 (Expert) · equity · v37→v45   Test at least three strategies: (1) use only the continuous score, (2) stack both outputs as separate features, (3) add a fixed bonus to the continuous score for samples the classifier labels as positive. Compare on the leaderboard or validation. The fixed-bonus approach is simple and avoids overfit
    evidence: ✓ An auxiliary classifier or head gives held-out information not captured by the main prediction. | ✓ The current post-processing was tuned for older checkpoints or its contribution is unverified.
    leaderboard score 0.57664 → 0.69275 (+0.11611)
- expert 75145694 (Expert) · equity · v56→v57   Include the new model's binary classification output in the aggregation that drives the discrete post-processing rule. This adds diversity to the binary vote without changing blend weights, and can recover small score losses from weight-only tuning.
    evidence: ✓ An auxiliary classifier or head gives held-out information not captured by the main prediction.
    leaderboard score 0.69307 → 0.69317 (+0.00010)
- expert 77276039 (Expert) · equity · v5→v9   Sweep the additive boost in both directions (increase and decrease) over several values while monitoring the validation metric. If the metric barely changes and the best value is near the starting point, the parameter is insensitive and further tuning is unwarranted — invest effort elsewhere.
    evidence: ✓ An auxiliary classifier or head gives held-out information not captured by the main prediction. | ✓ The current post-processing was tuned for older checkpoints or its contribution is unverified.
    leaderboard score n/a → n/a
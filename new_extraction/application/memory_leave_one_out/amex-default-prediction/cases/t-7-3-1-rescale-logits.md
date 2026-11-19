# Rescale logits  `T.7.3.1`   2 edits, 0 experts
2 scored cases, median improvement +0.00064, 2 improved


- expert 77450317 (Grandmaster) · equity · v14→v15   Multiply the NN's pre-activation logits by a constant greater than 1 before applying the sigmoid, sharpening the output distribution. Then retune the ensemble blend coefficients to account for the changed scale. Evaluate on the leaderboard or validation to confirm the gain.
    evidence: ✓ Logits are consistently too sharp or too flat on held-out examples. | ✗ Predictions violate the required range or do not sum to one for a distributional task. | ✗ The metric only uses within-column rank and no later blend or rounding depends on magnitude. | ✗ The logit scaling is applied inside the model's forward pass during training, altering gradient flow and training dynamics rather than only adjusting inference-time outputs.
    leaderboard score 0.69597 → 0.69661 (+0.00064)
- expert 77129691 (Master) · equity · v18→v19   Apply a multiplicative temperature scaling factor (e.g., 2×) to the logits before the sigmoid activation at inference time. This stretches the score distribution and can improve rank discrimination. Treat the scaling factor as a tunable hyperparameter and validate on the leaderboard or a held-out se
    evidence: ✗ Predictions violate the required range or do not sum to one for a distributional task. | ✓ The metric only uses within-column rank and no later blend or rounding depends on magnitude. | ✓ The logit scaling is applied inside the model's forward pass during training, altering gradient flow and training dynamics rather than only adjusting inference-time outputs.
    leaderboard score 0.69481 → 0.69540 (+0.00059)
# Resize the neural feature extractor  `T.5.2.5`   2 edits, 0 experts
2 scored cases, median improvement +0.00856, 1 improved


- expert 49524919 (Grandmaster) · hms · v46→v47   Scale up the model width (number of feature channels) by several times, add a few more residual blocks, enlarge the classification head accordingly, and switch to a slightly more expressive activation function. Ensure the inference code architecture exactly matches the new checkpoints. Expect a noti
    evidence: ✓ The neural feature extractor is narrow or explicitly truncates usable feature channels. | ✗ The proposed aggregation head is incompatible with existing trained checkpoints, requiring retraining or architectural bridging.
    leaderboard score 0.46059 → 0.41674 (-0.04385)
- expert 49576186 (Expert) · hms · v103→v105   Test with and without truncation on the leaderboard. If the full-dimensional vector degrades the score, revert to the truncated version — the extra dimensions may introduce noise or overfitting when the classification head is small relative to the feature dimension.
    evidence: ✓ The neural feature extractor is narrow or explicitly truncates usable feature channels.
    leaderboard score 0.27315 → 0.28170 (+0.00856)
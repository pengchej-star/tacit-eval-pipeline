# Align prediction direction  `T.1.2.5`   3 edits, 0 experts
2 scored cases, median improvement +0.39986, 2 improved


- expert 77129691 (Master) · equity · v1→v2   Negate the predictions and resubmit. If the score jumps to roughly (1 − old_score), the sign was inverted. Always verify whether the evaluation expects higher predictions to mean higher risk or longer survival, and align accordingly.
    evidence: ✓ Output axes, activation, or loss derivatives disagree with the target definition. | ✗ Predictions are constant or unchanged after changes that should affect them. | ✓ One member orders risk or target values in the opposite direction.
    leaderboard score 0.29019 → 0.69005 (+0.39986)
- expert 75145694 (Expert) · equity · v20→v21   Before blending, verify that all model outputs share the same monotonic direction with respect to the target. Compute rank correlations between each model's predictions and the others; if one is negatively correlated, negate its outputs. Add an explicit sign-correction step in the blending pipeline 
    evidence: ✓ One member orders risk or target values in the opposite direction.
    leaderboard score 0.68959 → 0.68978 (+0.00020)
- expert 75145694 (Expert) · equity · v36→v38   Before blending, verify the new model's prediction direction by checking its standalone concordance or correlation with the target. If the metric is sign-sensitive (e.g., concordance index), negate or rank-transform the predictions and compare. Add debug prints of prediction statistics to catch the 
    evidence: ✓ A code block for one of the intended ensemble or pipeline components is commented out, disabled, or otherwise not executed. | ✓ The model loading paths point to wrong experiment directories or files, causing incorrect or failed model loads. | ✓ One member orders risk or target values in the opposite direction.
    leaderboard score n/a → 0.69283
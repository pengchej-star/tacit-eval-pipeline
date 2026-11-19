# Calibrate class probabilities  `T.6.2.2`   3 edits, 0 experts
2 scored cases, median improvement -0.00800, 0 improved


- expert 49524919 (Grandmaster) · hms · v13→v14   Apply per-class multiplicative scaling factors to the predicted probabilities, then renormalize each sample's predictions to sum to 1. Choose the factors by estimating the ratio of true class frequencies (or vote shares) to predicted class frequencies on a validation set. Submit and compare against 
    evidence: ✓ Probability vectors are valid but classwise calibration is consistently biased.
    leaderboard score 0.47129 → 0.46329 (-0.00800)
- expert 49524919 (Grandmaster) · hms · v16→v21   Test per-class multipliers by enabling and disabling them as a single controlled change. If the metric worsens or is inconsistent across checkpoint versions, the multipliers are likely adding noise rather than correcting a real bias—remove them and rely on the model's calibrated outputs.
    evidence: ✓ Probability vectors are valid but classwise calibration is consistently biased. | ✓ The proposed correction risks overfitting to training-distribution statistics given the size or noise level of the test set. | ✗ Raw model outputs may exceed the valid target range or hit exact boundaries.
    leaderboard score n/a → 0.48815
- expert 49524919 (Grandmaster) · hms · v21→v25   For each new checkpoint, submit once with and once without the post-processing adjustment. If the adjustment consistently fails to improve or worsens the score across multiple checkpoint versions, disable it permanently and let the model's own calibration stand.
    evidence: ✓ Probability vectors are valid but classwise calibration is consistently biased. | ✓ The proposed correction risks overfitting to training-distribution statistics given the size or noise level of the test set. | ✗ Raw model outputs may exceed the valid target range or hit exact boundaries.
    leaderboard score 0.48815 → 0.45926 (-0.02889)
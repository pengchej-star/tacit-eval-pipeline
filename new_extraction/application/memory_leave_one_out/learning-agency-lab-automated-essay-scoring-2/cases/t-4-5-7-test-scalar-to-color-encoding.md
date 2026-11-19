# Test scalar-to-color encoding  `T.4.5.7`   1 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median -0.01220, 0 improved


- expert 49576186 · hms · v22→v24   Apply a standard colormap (e.g., jet) to map scalar spectrogram values to 3-channel RGB, then feed to the pretrained backbone. Compare against the baseline input format on the leaderboard or validation. Be aware this may not help and can even hurt if the original channel encoding already carries use
    evidence: ✓ A natural-image backbone receives scalar spectral images and a color encoding has not been tested. | ✓ A previous experiment changed the encoding parameter together with another variable, so the encoding effect is confounded and must be isolated. | ✓ Missing or NaN values in the signal or spectrogram need explicit handling before normalization and model input.
    leaderboard score 0.36216 → 0.37436 (lower is better; worse by 0.01220)
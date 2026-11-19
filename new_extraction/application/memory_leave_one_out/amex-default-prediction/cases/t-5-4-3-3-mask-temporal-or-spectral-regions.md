# Mask temporal or spectral regions  `T.5.4.3.3`   1 edits, 0 experts
1 scored cases, median improvement +0.00298, 1 improved


- expert 49576186 (Expert) · hms · v157→v163   Add random zeroing of contiguous time-frequency regions in the spectrogram (applied stochastically per sample during training only). Test across multiple runs. If the score does not improve after several attempts, the augmentation is not beneficial for this input representation and should be reverte
    evidence: ✓ Spectrogram blackout/masking augmentation code was previously scaffolded or introduced but has not yet been scored. | ✓ Previous spectrogram masking augmentation attempts have not clearly improved the score, warranting re-runs or parameter iteration. | ✓ Spectral inputs contain locally redundant regions and masking preserves the event label. | ✗ The task relies on exact orientation or a small localized event. | ✓ NaN values exist in the input data (spectrograms or EEG) that could corrupt mixed or masked samples. | ✓ MixUp-style augmentation was previously tried and did not sufficiently address overfitting.
    leaderboard score 0.27394 → 0.27691 (+0.00298)
# Mask local signal regions  `T.5.3.2`   1 edits, 0 experts
1 scored cases, median improvement +0.00298, 1 improved


- expert 49576186 (Expert) · hms · v157→v163   Add random zeroing of contiguous time-frequency regions in the spectrogram (applied stochastically per sample during training only). Test across multiple runs. If the score does not improve after several attempts, the augmentation is not beneficial for this input representation and should be reverte
    evidence: ✓ The model sees spectrograms and should tolerate missing local time-frequency evidence. | ✓ The proposed augmentation code was already scaffolded or commented out in a prior version and only needs to be activated, not written from scratch. | ✓ The previous augmentation run did not clearly improve over the non-augmented baseline, so a re-run is needed to distinguish signal from variance. | ✗ Geometric transforms (e.g., rotation) have not been previously tried and are now being introduced into the augmentation pipeline. | ✓ Labels are soft distributions and the existing training code already supports weighted example mixing.
    leaderboard score 0.27394 → 0.27691 (+0.00298)
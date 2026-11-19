# Change input scaling and rendering  `T.4.3.4`   6 edits, 0 experts
5 scored cases, median improvement +0.00542, 3 improved


- expert 49576186 (Expert) · hms · v22→v24   Apply a standard colormap (e.g., jet) to map scalar spectrogram values to 3-channel RGB, then feed to the pretrained backbone. Compare against the baseline input format on the leaderboard or validation. Be aware this may not help and can even hurt if the original channel encoding already carries use
    evidence: ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs. | ✓ Channel order, derived channels, or pseudo-image layout limits information accessible to the backbone.
    leaderboard score 0.36216 → 0.37436 (+0.01220)
- expert 52200959 (Master) · hms · v33→v34   Fill missing values, clip extreme values, apply a log-transform to compress dynamic range, then z-score normalize. Resize to a resolution the pretrained backbone expects. This chain brings the distribution closer to what ImageNet-pretrained weights assume and avoids numerical issues from raw spectro
    evidence: ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs.
    leaderboard score n/a → 0.41865
- expert 50496431 (Grandmaster) · hms · v32→v33   Probe the dB clipping threshold by small increments (e.g., increase by ~25%). If the change alone hurts, do not immediately revert—it may interact positively with other pipeline changes. Evaluate in combination before deciding.
    evidence: ✗ The current crop omits relevant context or includes long irrelevant regions. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs.
    leaderboard score 0.35396 → 0.35938 (+0.00542)
- expert 50496431 (Grandmaster) · hms · v89→v90   Tighten the clipping range (e.g., halve it) to suppress outliers and increase the effective dynamic range of typical signal values in the spectrogram. Verify on the leaderboard that the tighter range improves or maintains performance; if it hurts, widen slightly.
    evidence: ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs.
    leaderboard score 0.32370 → 0.27848 (-0.04521)
- expert 50496431 (Grandmaster) · hms · v206→v208   When experimenting with input normalization at inference, keep changes small and consistent with training preprocessing. If a normalization change (e.g., switching from linear scaling to log scaling) causes a large score regression, revert immediately rather than trying to tune it further, because t
    evidence: ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs. | ✓ The current crop omits relevant context or includes long irrelevant regions.
    leaderboard score 0.22628 → 0.25986 (+0.03359)
- expert 49524919 (Grandmaster) · hms · v26→v27   Apply channel-wise instance normalization (zero-mean, unit-variance per channel per sample) instead of global transforms. This aligns each channel's distribution independently, which better suits multi-channel spectrograms where channels have heterogeneous scales.
    evidence: ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs.
    leaderboard score 0.47345 → 0.45265 (-0.02080)
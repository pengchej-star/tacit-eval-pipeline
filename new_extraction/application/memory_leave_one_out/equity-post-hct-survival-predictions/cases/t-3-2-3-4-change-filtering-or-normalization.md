# Change filtering or normalization  `T.3.2.3.4`   10 edits, 0 experts
6 scored cases, median improvement -0.00573, 2 improved


- expert 49524919 (Grandmaster) · hms · v26→v27   Apply channel-wise instance normalization (zero-mean, unit-variance per channel per sample) instead of global transforms. This aligns each channel's distribution independently, which better suits multi-channel spectrograms where channels have heterogeneous scales.
    evidence: ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
    leaderboard score 0.47345 → 0.45265 (-0.02080)
- expert 49576186 (Expert) · hms · v50→v52   Test the lower sampling rate and narrower filter as a pair against the original settings. If the score degrades, revert both. Physiological signals (especially brain activity) can carry discriminative information in higher frequency bands, so do not aggressively downsample or narrow the filter witho
    evidence: ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
    leaderboard score 0.36844 → 0.37019 (+0.00175)
- expert 52200959 (Master) · hms · v33→v34   Fill missing values, clip extreme values, apply a log-transform to compress dynamic range, then z-score normalize. Resize to a resolution the pretrained backbone expects. This chain brings the distribution closer to what ImageNet-pretrained weights assume and avoids numerical issues from raw spectro
    evidence: ✓ Discriminative image detail is lost at the current resolution and the checkpoint supports another size. | ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
    leaderboard score n/a → 0.41865
- expert 15082684 (Master) · ranzcr · v17→v18   Compute the channel-wise mean and standard deviation on the training set and use those values for normalization at both training and inference. For single-channel images replicated to three channels, use the same statistic for all channels. Verify the statistics match between training and inference 
    evidence: ✗ Discriminative image detail is lost at the current resolution and the checkpoint supports another size. | ✗ Relevant frequency structure is unresolved or blurred by the current transform. | ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
    leaderboard score n/a → 0.96509
- expert 15173072 (Contributor) · ranzcr · v15→v21   Default to the canonical normalization statistics for the pretraining dataset (e.g., the dataset-wide mean/std the model was trained with). Deviating from these values almost always hurts because the model's learned features expect a specific input distribution. If the exact training stats are unkno
    evidence: ✗ Discriminative image detail is lost at the current resolution and the checkpoint supports another size. | ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation. | ✗ Relevant frequency structure is unresolved or blurred by the current transform.
    leaderboard score n/a → 0.95243
- expert 50496431 (Grandmaster) · hms · v32→v33   Probe the dB clipping threshold by small increments (e.g., increase by ~25%). If the change alone hurts, do not immediately revert—it may interact positively with other pipeline changes. Evaluate in combination before deciding.
    evidence: ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
    leaderboard score 0.35396 → 0.35938 (+0.00542)
- expert 50496431 (Grandmaster) · hms · v89→v90   Tighten the clipping range (e.g., halve it) to suppress outliers and increase the effective dynamic range of typical signal values in the spectrogram. Verify on the leaderboard that the tighter range improves or maintains performance; if it hurts, widen slightly.
    evidence: ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
    leaderboard score 0.32370 → 0.27848 (-0.04521)
- expert 50496431 (Grandmaster) · hms · v171→v172   Apply a notch filter at the known interference frequency before any further signal processing (bandpass, spectrogram). This removes a predictable artifact that can leak into frequency-domain features and hurt generalization. Verify the effect by submitting with and without the filter while keeping o
    evidence: ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
    leaderboard score 0.28928 → 0.23376 (-0.05551)
- expert 50496431 (Grandmaster) · hms · v181→v182   Swap the filtering backend (e.g., from an FIR library filter to a low-order IIR Butterworth via a scientific-computing library) while keeping the same cutoff frequencies. Compare leaderboard or validation scores to decide which filter to keep. A low filter order (e.g., 2) reduces ringing and phase d
    evidence: ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation.
    leaderboard score 0.23815 → 0.23243 (-0.00573)
- expert 50496431 (Grandmaster) · hms · v208→v210   Test a higher filter order in one experiment. If the score does not clearly improve, revert to the lower order, since a sharper filter risks removing information the model expects. Keep the filter order consistent with what was used during training whenever possible.
    evidence: ✓ Outliers, fixed-frequency interference, or inconsistent input scale dominate the representation. | ✓ Unused channels or modalities contain potentially complementary information, or existing branches may be redundant.
    leaderboard score 0.25986 → n/a
# Change signal filtering  `T.4.3.3`   4 edits, 0 experts
3 scored cases, median improvement -0.00573, 1 improved


- expert 49576186 (Expert) · hms · v50→v52   Test the lower sampling rate and narrower filter as a pair against the original settings. If the score degrades, revert both. Physiological signals (especially brain activity) can carry discriminative information in higher frequency bands, so do not aggressively downsample or narrow the filter witho
    evidence: ✓ Signals contain identifiable narrow-band artifacts or passband-sensitive information.
    leaderboard score 0.36844 → 0.37019 (+0.00175)
- expert 50496431 (Grandmaster) · hms · v171→v172   Apply a notch filter at the known interference frequency before any further signal processing (bandpass, spectrogram). This removes a predictable artifact that can leak into frequency-domain features and hurt generalization. Verify the effect by submitting with and without the filter while keeping o
    evidence: ✓ Signals contain identifiable narrow-band artifacts or passband-sensitive information.
    leaderboard score 0.28928 → 0.23376 (-0.05551)
- expert 50496431 (Grandmaster) · hms · v181→v182   Swap the filtering backend (e.g., from an FIR library filter to a low-order IIR Butterworth via a scientific-computing library) while keeping the same cutoff frequencies. Compare leaderboard or validation scores to decide which filter to keep. A low filter order (e.g., 2) reduces ringing and phase d
    evidence: ✓ Signals contain identifiable narrow-band artifacts or passband-sensitive information.
    leaderboard score 0.23815 → 0.23243 (-0.00573)
- expert 50496431 (Grandmaster) · hms · v208→v210   Test a higher filter order in one experiment. If the score does not clearly improve, revert to the lower order, since a sharper filter risks removing information the model expects. Keep the filter order consistent with what was used during training whenever possible.
    evidence: ✓ Signals contain identifiable narrow-band artifacts or passband-sensitive information. | ✓ An available raw or transformed modality contains information absent from the active branch. | ✓ Input dynamic range or channel statistics differ materially from the backbone’s expected inputs.
    leaderboard score 0.25986 → n/a
# Tune raw-signal filtering and clipping  `T.3.3.5`   6 edits, 0 experts
5 scored cases (improvement signed by each competition's direction), median +0.02738, 4 improved


- expert 49576186 · hms · v50→v52   Test the lower sampling rate and narrower filter as a pair against the original settings. If the score degrades, revert both. Physiological signals (especially brain activity) can carry discriminative information in higher frequency bands, so do not aggressively downsample or narrow the filter witho
    evidence: ✓ Raw signals show fixed-frequency interference or extreme amplitude artifacts. | ✓ Existing checkpoints were trained with different transforms from the proposed inference change.
    leaderboard score 0.36844 → 0.37019 (lower is better; worse by 0.00175)
- expert 50496431 · hms · v89→v90   Tighten the clipping range (e.g., halve it) to suppress outliers and increase the effective dynamic range of typical signal values in the spectrogram. Verify on the leaderboard that the tighter range improves or maintains performance; if it hurts, widen slightly.
    evidence: ✓ Raw signals show fixed-frequency interference or extreme amplitude artifacts.
    leaderboard score 0.32370 → 0.27848 (lower is better; improved by 0.04521)
- expert 50496431 · hms · v93→v95   Keep inference-time preprocessing (filter bands, normalization, clipping) consistent with training-time settings. If you want to test a different preprocessing, retrain models with that setting; changing only inference preprocessing typically degrades scores because the input distribution shifts awa
    evidence: ✓ Existing checkpoints were trained with different transforms from the proposed inference change.
    leaderboard score 0.30691 → 0.27954 (lower is better; improved by 0.02738)
- expert 50496431 · hms · v171→v172   Apply a notch filter at the known interference frequency before any further signal processing (bandpass, spectrogram). This removes a predictable artifact that can leak into frequency-domain features and hurt generalization. Verify the effect by submitting with and without the filter while keeping o
    evidence: ✓ Raw signals show fixed-frequency interference or extreme amplitude artifacts.
    leaderboard score 0.28928 → 0.23376 (lower is better; improved by 0.05551)
- expert 50496431 · hms · v181→v182   Swap the filtering backend (e.g., from an FIR library filter to a low-order IIR Butterworth via a scientific-computing library) while keeping the same cutoff frequencies. Compare leaderboard or validation scores to decide which filter to keep. A low filter order (e.g., 2) reduces ringing and phase d
    evidence: ✓ Raw signals show fixed-frequency interference or extreme amplitude artifacts. | ✓ Existing checkpoints were trained with different transforms from the proposed inference change.
    leaderboard score 0.23815 → 0.23243 (lower is better; improved by 0.00573)
- expert 50496431 · hms · v208→v210   Test a higher filter order in one experiment. If the score does not clearly improve, revert to the lower order, since a sharper filter risks removing information the model expects. Keep the filter order consistent with what was used during training whenever possible.
    evidence: ✓ Existing checkpoints were trained with different transforms from the proposed inference change.
    leaderboard score 0.25986 → n/a (lower is better)
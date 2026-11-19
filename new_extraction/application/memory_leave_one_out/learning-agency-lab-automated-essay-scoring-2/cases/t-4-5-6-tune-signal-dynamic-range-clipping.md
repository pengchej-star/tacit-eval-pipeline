# Tune signal dynamic-range clipping  `T.4.5.6`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.04521, 1 improved


- expert 50496431 · hms · v32→v33   Probe the dB clipping threshold by small increments (e.g., increase by ~25%). If the change alone hurts, do not immediately revert—it may interact positively with other pipeline changes. Evaluate in combination before deciding.
    evidence: ✓ A few extreme values dominate the raw or spectral dynamic range. | ✓ A previous experiment changed the encoding parameter together with another variable, so the encoding effect is confounded and must be isolated.
    leaderboard score 0.35396 → 0.35938 (lower is better; worse by 0.00542)
- expert 50496431 · hms · v89→v90   Tighten the clipping range (e.g., halve it) to suppress outliers and increase the effective dynamic range of typical signal values in the spectrogram. Verify on the leaderboard that the tighter range improves or maintains performance; if it hurts, widen slightly.
    evidence: ✓ A few extreme values dominate the raw or spectral dynamic range. | ✓ A previous experiment changed the encoding parameter together with another variable, so the encoding effect is confounded and must be isolated.
    leaderboard score 0.32370 → 0.27848 (lower is better; improved by 0.04521)
# Clip signal outliers  `T.4.4.3`   1 edits, 0 experts
1 scored cases, median improvement -0.04521, 0 improved


- expert 50496431 (Grandmaster) · hms · v89→v90   Tighten the clipping range (e.g., halve it) to suppress outliers and increase the effective dynamic range of typical signal values in the spectrogram. Verify on the leaderboard that the tighter range improves or maintains performance; if it hurts, widen slightly.
    evidence: ✓ Rare amplitude spikes dominate the signal range. | ✗ The most recent front-end changes have not yet been scored, so the immediate next step is a scoring run rather than a new front-end experiment.
    leaderboard score 0.32370 → 0.27848 (-0.04521)
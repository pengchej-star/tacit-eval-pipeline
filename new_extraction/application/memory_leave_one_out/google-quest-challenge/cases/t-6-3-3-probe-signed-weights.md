# Probe signed weights  `T.6.3.3`   2 edits, 0 experts

- expert 29588171 (Master) · amex · v5→v7   Test one negative-weight configuration early in the sweep. If the score drops noticeably compared to small positive weights, conclude the auxiliary carries a genuine positive signal and restrict further search to positive weights only.
    evidence: ✓ The only evaluation feedback is a small public subset and many weights have already been tried. | ✓ Members differ in quality or residual patterns and the current blend has not been retuned after a component change. | ✓ An auxiliary prediction has a stable residual correction that may require subtraction.
    leaderboard score n/a → 0.79983
- expert 75584724 (Master) · equity · v1→v2   Extend the per-model weight search range to include negative values (e.g., from −0.5 to +0.5). Keep the step size unchanged. Evaluate on the validation metric to confirm that the optimizer can exploit negative weights without overfitting to noise.
    evidence: ✓ The metric is ranking-based and member prediction scales or calibrations differ. | ✗ Models output class distributions and confidence differs across members.
    leaderboard score 0.69137 → n/a
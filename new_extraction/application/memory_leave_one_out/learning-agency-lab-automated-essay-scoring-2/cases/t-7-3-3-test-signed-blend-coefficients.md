# Test signed blend coefficients  `T.7.3.3`   3 edits, 0 experts
1 scored cases, median improvement +0.00254, 1 improved


- expert 29588171 (Master) · amex · v5→v7   Test one negative-weight configuration early in the sweep. If the score drops noticeably compared to small positive weights, conclude the auxiliary carries a genuine positive signal and restrict further search to positive weights only.
    evidence: ✓ Component quality differs reproducibly or a member’s predictions have changed since weights were tuned. | ✗ Members have comparable quality and tuned weights have not reliably improved the simple average. | ✓ A candidate’s residual contribution appears negatively correlated with the remaining blend’s error.
    leaderboard score n/a → 0.79983
- expert 75584724 (Master) · equity · v1→v2   Extend the per-model weight search range to include negative values (e.g., from −0.5 to +0.5). Keep the step size unchanged. Evaluate on the validation metric to confirm that the optimizer can exploit negative weights without overfitting to noise.
    evidence: ✓ A candidate’s residual contribution appears negatively correlated with the remaining blend’s error.
    leaderboard score 0.69137 → n/a
- expert 73937748 (Master) · equity · v49→v51   Allow negative weights and do not force normalization. This lets the optimizer effectively subtract correlated or noisy models. If the unconstrained search overfits on validation, add light regularization (e.g., a penalty term on weight magnitude) rather than hard positivity/sum constraints.
    evidence: ✓ A candidate’s residual contribution appears negatively correlated with the remaining blend’s error.
    leaderboard score 0.68846 → 0.69100 (+0.00254)
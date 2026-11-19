# Allow subtractive coefficients  `T.6.2.1.3`   2 edits, 0 experts
1 scored cases, median improvement +0.00254, 1 improved


- expert 75584724 (Master) · equity · v1→v2   Extend the per-model weight search range to include negative values (e.g., from −0.5 to +0.5). Keep the step size unchanged. Evaluate on the validation metric to confirm that the optimizer can exploit negative weights without overfitting to noise.
    evidence: none recorded
    leaderboard score 0.69137 → n/a
- expert 73937748 (Master) · equity · v49→v51   Allow negative weights and do not force normalization. This lets the optimizer effectively subtract correlated or noisy models. If the unconstrained search overfits on validation, add light regularization (e.g., a penalty term on weight magnitude) rather than hard positivity/sum constraints.
    evidence: ✓ Residual covariance suggests that subtracting a correlated source could correct systematic error. | ✗ Members have comparable held-out quality and weight tweaks have not generalized.
    leaderboard score 0.68846 → 0.69100 (+0.00254)
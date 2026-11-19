# Test signed blend weights  `T.7.2.4`   2 edits, 0 experts

- expert 29588171 (Master) · amex · v5→v7   Test one negative-weight configuration early in the sweep. If the score drops noticeably compared to small positive weights, conclude the auxiliary carries a genuine positive signal and restrict further search to positive weights only.
    evidence: ✓ The auxiliary source is substantially weaker than the established baseline. | ✓ Components have unequal validated quality and their combination changes the metric. | ✓ An auxiliary source is negatively associated with the baseline residual after controlling for the base prediction.
    leaderboard score n/a → 0.79983
- expert 75584724 (Master) · equity · v1→v2   Extend the per-model weight search range to include negative values (e.g., from −0.5 to +0.5). Keep the step size unchanged. Evaluate on the validation metric to confirm that the optimizer can exploit negative weights without overfitting to noise.
    evidence: ✓ The metric depends on ordering and member outputs have incompatible scales or outliers.
    leaderboard score 0.69137 → n/a
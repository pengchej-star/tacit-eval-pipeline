# Subsample rows or columns  `T.6.1.3`   1 edits, 0 experts
1 scored cases, median improvement +0.00296, 1 improved


- expert 27389424 (Grandmaster) · amex · v63→v64   Enable column subsampling and row subsampling (e.g., both around 0.3) so each tree sees a random subset of features and rows. Also increase early-stopping patience proportionally so the model can still find its best iteration under the added noise.
    evidence: ✓ Training fit is strong but validation worsens as complexity grows. | ✓ Trees repeatedly use the same dominant rows or feature groups.
    leaderboard score 0.78859 → 0.79155 (+0.00296)
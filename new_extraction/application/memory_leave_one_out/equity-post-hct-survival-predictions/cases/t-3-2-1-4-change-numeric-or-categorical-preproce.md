# Change numeric or categorical preprocessing  `T.3.2.1.4`   6 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00391, 2 improved


- expert 27836972 · amex · v12→v16   Start by leaving NaNs for the tree model to handle natively. Only add explicit imputation if validation shows it helps. Aggregation-induced NaNs (e.g., std with one row) often carry information (small group size), so preserving them as missing is a reasonable default.
    evidence: ✓ Missingness, category handling, quantization, or scaling differs between model families. | ✓ Adding many aggregations caused pipeline failures or excessive complexity that prevented end-to-end execution. | ✓ Previous S_2 temporal encoding variants have consistently failed to improve over the baseline.
    leaderboard score n/a → n/a (higher is better)
- expert 27836972 · amex · v21→v25   Round continuous features to a small number of decimal places, replace the originals, and evaluate on the leaderboard or validation set. Expect only a marginal gain; treat it as a low-effort addition rather than a major lever.
    evidence: ✓ Missingness, category handling, quantization, or scaling differs between model families. | ✓ Adding many aggregations caused pipeline failures or excessive complexity that prevented end-to-end execution. | ✓ Previously added lag-difference and lag-ratio features failed to improve the score over the simpler aggregation baseline. | ✓ Previous S_2 temporal encoding variants have consistently failed to improve over the baseline.
    leaderboard score n/a → 0.79366 (higher is better)
- expert 27502740 · amex · v5→v6   Before training, upcast low-precision float columns to a higher-precision type, round to a fixed number of decimal places that preserves meaningful variation, then cast back. Apply identically to train and test. Verify on the leaderboard that the rounding level chosen does not discard useful signal.
    evidence: ✓ Missingness, category handling, quantization, or scaling differs between model families.
    leaderboard score 0.79418 → 0.79501 (higher is better; improved by 0.00083)
- expert 28093671 · amex · v32→v34   Convert to the CPU dataframe library before the groupby, use the transform method to get row-aligned group statistics for fillna, then convert back to the GPU library. This isolates the unsupported operation while keeping GPU acceleration elsewhere.
    evidence: ✓ Missingness, category handling, quantization, or scaling differs between model families.
    leaderboard score n/a → n/a (higher is better)
- expert 28093671 · amex · v34→v37   Try disabling scaling, outlier filtering, and manual imputation for tree-based models. Validate on the leaderboard or holdout. If the score improves or stays the same, keep the simpler pipeline. Only re-add such steps if there is clear evidence they help.
    evidence: ✓ Missingness, category handling, quantization, or scaling differs between model families. | ✓ Adding many aggregations caused pipeline failures or excessive complexity that prevented end-to-end execution.
    leaderboard score n/a → 0.79304 (higher is better)
- expert 28093671 · amex · v39→v40   When using a tree-based model that handles NaNs natively, try leaving NaNs as-is rather than imputing with a constant. Compare validation or leaderboard scores with and without imputation; if removing imputation improves the score, keep NaNs for the model to handle.
    evidence: ✓ Missingness, category handling, quantization, or scaling differs between model families.
    leaderboard score 0.78971 → 0.79361 (higher is better; improved by 0.00391)
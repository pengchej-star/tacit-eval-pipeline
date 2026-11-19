# Preserve native tree inputs  `T.4.3.1`   4 edits, 0 experts
2 scored cases, median improvement +0.00391, 2 improved


- expert 27836972 (Expert) · amex · v12→v16   Start by leaving NaNs for the tree model to handle natively. Only add explicit imputation if validation shows it helps. Aggregation-induced NaNs (e.g., std with one row) often carry information (small group size), so preserving them as missing is a reasonable default.
    evidence: ✓ The current tree implementation handles missing values and added preprocessing erases missingness or removes useful extremes. | ✗ At least one active model rejects missing values or lacks native handling.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v34→v37   Try disabling scaling, outlier filtering, and manual imputation for tree-based models. Validate on the leaderboard or holdout. If the score improves or stays the same, keep the simpler pipeline. Only re-add such steps if there is clear evidence they help.
    evidence: ✓ The current tree implementation handles missing values and added preprocessing erases missingness or removes useful extremes. | ✗ At least one active model rejects missing values or lacks native handling.
    leaderboard score n/a → 0.79304
- expert 28093671 (Contributor) · amex · v39→v40   When using a tree-based model that handles NaNs natively, try leaving NaNs as-is rather than imputing with a constant. Compare validation or leaderboard scores with and without imputation; if removing imputation improves the score, keep NaNs for the model to handle.
    evidence: ✓ The current tree implementation handles missing values and added preprocessing erases missingness or removes useful extremes. | ✗ At least one active model rejects missing values or lacks native handling.
    leaderboard score 0.78971 → 0.79361 (+0.00391)
- expert 73937748 (Master) · equity · v12→v13   Try disabling standard scaling of numeric features when the pipeline uses only tree-based models. If the score stays the same or improves, remove scaling permanently to simplify the pipeline.
    evidence: ✓ The current tree implementation handles missing values and added preprocessing erases missingness or removes useful extremes. | ✗ At least one active model rejects missing values or lacks native handling.
    leaderboard score 0.68793 → 0.68805 (+0.00012)
# Use model-appropriate missing values  `T.3.4.4.1`   5 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00016, 3 improved


- expert 27836972 · amex · v12→v16   Start by leaving NaNs for the tree model to handle natively. Only add explicit imputation if validation shows it helps. Aggregation-induced NaNs (e.g., std with one row) often carry information (small group size), so preserving them as missing is a reasonable default.
    evidence: ✓ Missing or non-finite values reach a learner with a known missing-value policy.
    leaderboard score n/a → n/a (higher is better)
- expert 28093671 · amex · v32→v34   Convert to the CPU dataframe library before the groupby, use the transform method to get row-aligned group statistics for fillna, then convert back to the GPU library. This isolates the unsupported operation while keeping GPU acceleration elsewhere.
    evidence: ✓ Missing or non-finite values reach a learner with a known missing-value policy.
    leaderboard score n/a → n/a (higher is better)
- expert 28093671 · amex · v39→v40   When using a tree-based model that handles NaNs natively, try leaving NaNs as-is rather than imputing with a constant. Compare validation or leaderboard scores with and without imputation; if removing imputation improves the score, keep NaNs for the model to handle.
    evidence: ✓ Missing or non-finite values reach a learner with a known missing-value policy.
    leaderboard score 0.78971 → 0.79361 (higher is better; improved by 0.00391)
- expert 75145694 · equity · v34→v35   Make the feature-generation function model-aware by accepting a model identifier and branching on it: apply the imputation strategy each model family expects (e.g., sentinel value for tree models that lack native NaN support, median/mean for others). This ensures every ensemble member receives corre
    evidence: ✓ Missing or non-finite values reach a learner with a known missing-value policy.
    leaderboard score 0.69296 → 0.69312 (higher is better; improved by 0.00016)
- expert 75145694 · equity · v66→v67   Add explicit NaN/Inf checks on both inputs and intermediate outputs at each pipeline stage. Replace missing values with a safe sentinel before feeding data to the network. Use stable weight initialization schemes. Insert runtime warnings that fire when any tensor contains non-finite values, so probl
    evidence: ✓ Missing or non-finite values reach a learner with a known missing-value policy.
    leaderboard score 0.69348 → 0.69358 (higher is better; improved by 0.00010)
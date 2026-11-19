# Use model-specific imputation  `T.4.3.2`   1 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00016, 1 improved


- expert 75145694 · equity · v34→v35   Make the feature-generation function model-aware by accepting a model identifier and branching on it: apply the imputation strategy each model family expects (e.g., sentinel value for tree models that lack native NaN support, median/mean for others). This ensures every ensemble member receives corre
    evidence: ✓ The current tree implementation handles missing values and added preprocessing erases missingness or removes useful extremes. | ✓ At least one active model rejects missing values or lacks native handling. | ✓ The existing preprocessing code contains an implementation bug that prevents it from executing correctly and must be fixed before evaluating the preprocessing strategy.
    leaderboard score 0.69296 → 0.69312 (higher is better; improved by 0.00016)
# Impute and encode explicitly  `T.4.4.5`   4 edits, 0 experts
3 scored cases, median improvement +0.00016, 3 improved


- expert 75145694 (Expert) · equity · v34→v35   Make the feature-generation function model-aware by accepting a model identifier and branching on it: apply the imputation strategy each model family expects (e.g., sentinel value for tree models that lack native NaN support, median/mean for others). This ensures every ensemble member receives corre
    evidence: ✓ The learner supports missing values and is insensitive to feature scaling. | ✓ A model requires finite inputs or the test set contains unseen categories.
    leaderboard score 0.69296 → 0.69312 (+0.00016)
- expert 75145694 (Expert) · equity · v66→v67   Add explicit NaN/Inf checks on both inputs and intermediate outputs at each pipeline stage. Replace missing values with a safe sentinel before feeding data to the network. Use stable weight initialization schemes. Insert runtime warnings that fire when any tensor contains non-finite values, so probl
    evidence: ✗ The learner supports missing values and is insensitive to feature scaling. | ✓ A model requires finite inputs or the test set contains unseen categories.
    leaderboard score 0.69348 → 0.69358 (+0.00010)
- expert 7823861 (nan) · google · v8→v10   Fit the encoder on training data only. At test time, call transform (not fit_transform) on the test data. Ensure the output array has exactly as many rows as the test set. Set the encoder to handle unknown categories gracefully (e.g., ignore or map to a default) so unseen test categories do not caus
    evidence: ✓ A model requires finite inputs or the test set contains unseen categories.
    leaderboard score n/a → 0.41495
- expert 7823861 (nan) · google · v10→v15   Use two layers of defense: configure the encoder to ignore unknown categories (producing a zero-vector), and also remap unknown values to the most frequent or most representative training category before encoding. This avoids both crashes and degenerate feature vectors.
    evidence: ✓ A model requires finite inputs or the test set contains unseen categories.
    leaderboard score 0.41495 → 0.42097 (+0.00603)
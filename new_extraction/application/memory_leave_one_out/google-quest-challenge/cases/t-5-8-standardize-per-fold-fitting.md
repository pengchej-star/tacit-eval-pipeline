# Standardize per-fold fitting  `T.5.8`   4 edits, 0 experts
4 scored cases (improvement signed by each competition's direction), median +0.00038, 4 improved


- expert 75584724 · equity · v6→v7   Restructure the neural network training into proper K-fold cross-validation with per-fold model saving, tune its architecture/training hyperparameters, and regenerate its out-of-fold and test predictions for the ensemble. Even small improvements in a single ensemble member can translate to modest bu
    evidence: ✓ A component is fitted ad hoc without the fold discipline used by the rest of the ensemble.
    leaderboard score 0.69427 → 0.69453 (higher is better; improved by 0.00027)
- expert 75924487 · equity · v8→v9   Rewrite the neural network training to use the same K-Fold splits as other ensemble members, save each fold's trained weights separately, and tune architecture hyperparameters. Expect the direct LB gain to be marginal; the main value is a cleaner, more reliable ensemble member that enables future ga
    evidence: ✓ A component is fitted ad hoc without the fold discipline used by the rest of the ensemble.
    leaderboard score 0.69347 → 0.69350 (higher is better; improved by 0.00003)
- expert 73937748 · equity · v60→v61   Refactor the neural network training to use the framework's standard dataset/dataloader abstractions, train a separate model per cross-validation fold, save each fold's weights to disk, and generate out-of-fold predictions from the corresponding held-out fold. This improves prediction quality and re
    evidence: ✓ A component is fitted ad hoc without the fold discipline used by the rest of the ensemble.
    leaderboard score 0.69283 → 0.69321 (higher is better; improved by 0.00038)
- expert 73937748 · equity · v60→v61   Audit each ensemble member's training pipeline for engineering deficiencies (inconsistent cross-validation, missing batch loading, no model checkpointing, suboptimal hyperparameters). Fixing these issues in the least-rigorous component can yield incremental but real gains without increasing ensemble
    evidence: ✓ A component is fitted ad hoc without the fold discipline used by the rest of the ensemble.
    leaderboard score 0.69283 → 0.69321 (higher is better; improved by 0.00038)
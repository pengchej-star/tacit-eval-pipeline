# Train and persist models with proper cross-validation  `T.4.3.6`   4 edits, 0 experts
3 scored cases, median improvement +0.00027, 3 improved


- expert 28093671 (Contributor) · amex · v9→v10   Create a k-fold cross-validation loop with early stopping on a held-out fold. Include all preprocessing inside the loop to avoid leakage. Use GPU-accelerated tree training if available to shorten iteration time. Produce out-of-fold predictions so the full training set is scored.
    evidence: ✓ An ensemble member lacks reproducible fold-trained models or unbiased validation predictions. | ✓ GPU acceleration is available and would meaningfully speed up training iterations. | ✗ GPU training caused instability or errors requiring fallback to CPU. | ✓ The training loop currently lacks early-stopping and iteration-logging callbacks.
    leaderboard score n/a → n/a
- expert 75584724 (Master) · equity · v6→v7   Restructure the neural network training into proper K-fold cross-validation with per-fold model saving, tune its architecture/training hyperparameters, and regenerate its out-of-fold and test predictions for the ensemble. Even small improvements in a single ensemble member can translate to modest bu
    evidence: ✓ An ensemble member lacks reproducible fold-trained models or unbiased validation predictions. | ✓ Multiple hyperparameters are being changed simultaneously without isolating individual effects.
    leaderboard score 0.69427 → 0.69453 (+0.00027)
- expert 75924487 (Master) · equity · v8→v9   Rewrite the neural network training to use the same K-Fold splits as other ensemble members, save each fold's trained weights separately, and tune architecture hyperparameters. Expect the direct LB gain to be marginal; the main value is a cleaner, more reliable ensemble member that enables future ga
    evidence: ✓ An ensemble member lacks reproducible fold-trained models or unbiased validation predictions. | ✓ Multiple hyperparameters are being changed simultaneously without isolating individual effects.
    leaderboard score 0.69347 → 0.69350 (+0.00003)
- expert 73937748 (Master) · equity · v60→v61   Refactor the neural network training to use the framework's standard dataset/dataloader abstractions, train a separate model per cross-validation fold, save each fold's weights to disk, and generate out-of-fold predictions from the corresponding held-out fold. This improves prediction quality and re
    evidence: ✓ An ensemble member lacks reproducible fold-trained models or unbiased validation predictions. | ✓ Multiple hyperparameters are being changed simultaneously without isolating individual effects.
    leaderboard score 0.69283 → 0.69321 (+0.00038)
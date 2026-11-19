# Generate aligned out-of-fold predictions  `T.1.1.4`   2 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00003, 1 improved


- expert 28093671 · amex · v9→v10   Create a k-fold cross-validation loop with early stopping on a held-out fold. Include all preprocessing inside the loop to avoid leakage. Use GPU-accelerated tree training if available to shorten iteration time. Produce out-of-fold predictions so the full training set is scored.
    evidence: ✗ Several candidate configurations can be scored on an existing representative holdout. | ✓ A proposed stacker lacks held-out predictions aligned to common row and fold identifiers. | ✗ Local and public scores have ranked existing checkpoints differently. | ✓ The expert lacks local cross-validation infrastructure to rank checkpoints without relying on the noisy public leaderboard. | ✓ Multiple recent versions have not been submitted to the leaderboard, making submission budget conservation relevant.
    leaderboard score n/a → n/a (higher is better)
- expert 75924487 · equity · v8→v9   Use the identical K-Fold split indices for the new model as for existing members. Train one model per fold, generate out-of-fold predictions, and persist each fold's weights. Add the resulting prediction column to the meta-learner's input set. Verify the contribution is positive by checking whether 
    evidence: ✓ A proposed stacker lacks held-out predictions aligned to common row and fold identifiers.
    leaderboard score 0.69347 → 0.69350 (higher is better; improved by 0.00003)
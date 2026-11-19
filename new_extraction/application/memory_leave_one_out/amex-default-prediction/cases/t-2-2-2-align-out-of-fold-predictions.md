# Align out-of-fold predictions  `T.2.2.2`   3 edits, 0 experts
1 scored cases, median improvement +0.00003, 1 improved


- expert 75924487 (Master) · equity · v8→v9   Use the identical K-Fold split indices for the new model as for existing members. Train one model per fold, generate out-of-fold predictions, and persist each fold's weights. Add the resulting prediction column to the meta-learner's input set. Verify the contribution is positive by checking whether 
    evidence: ✓ Stacking members use incompatible folds or cannot establish exclusion of each predicted training row.
    leaderboard score 0.69347 → 0.69350 (+0.00003)
- expert 55987255 (Master) · learning · v156→v160   Use cross-validated out-of-fold predictions for the training set to avoid target leakage in stacking. If runtime or implementation complexity is prohibitive, verify with a held-out validation set that full-train predictions do not inflate the primary model's apparent performance. Always measure the 
    evidence: ✓ A training feature uses held-out labels or predictions made on its own training rows. | ✓ Stacking members use incompatible folds or cannot establish exclusion of each predicted training row. | ✓ Early-exit or runtime guards truncate training or evaluation, producing incomplete CV scores that misrepresent true model quality.
    leaderboard score n/a → n/a
- expert 55987255 (Master) · learning · v163→v164   Compute out-of-fold predictions from the base model inside the same notebook using the same cross-validation splits, collect them into a dataframe, and join them as features for the meta-learner. This ensures predictions are always fresh and aligned with the current data/splits.
    evidence: ✓ A training feature uses held-out labels or predictions made on its own training rows. | ✓ Stacking members use incompatible folds or cannot establish exclusion of each predicted training row. | ✓ Local model rankings disagree with earlier external results or the public evaluation set is tiny. | ✓ Early-exit or runtime guards truncate training or evaluation, producing incomplete CV scores that misrepresent true model quality.
    leaderboard score 0.80174 → n/a
# Preserve target balance  `T.2.2.1`   3 edits, 0 experts
1 scored cases, median improvement +0.00261, 1 improved


- expert 18851026 (Master) · commonlitreadabilityprize · v26→v28   Discretize the continuous target into bins and apply stratified K-fold splitting on those bins. This ensures each fold mirrors the overall target distribution, stabilizing both the CV metric and the out-of-fold predictions used for stacking.
    evidence: ✓ The target distribution is imbalanced and ordinary random folds omit rare levels.
    leaderboard score n/a → 0.45803
- expert 55431616 (Grandmaster) · learning · v11→v13   Use stratified cross-validation splits that preserve the target distribution in every fold, so that per-fold threshold optimization and objective alignment reflect the true test-time distribution.
    evidence: ✓ The target distribution is imbalanced and ordinary random folds omit rare levels. | ✓ A known training subpopulation resembles the test population more than the rest.
    leaderboard score 0.81502 → 0.81762 (+0.00261)
- expert 55987255 (Master) · learning · v117→v118   Before calling a stratified splitter, cast the target to integer (or bin it into a small number of discrete classes). For ordinal targets stored as floats, round or truncate to int. Verify the number of unique values in the cast target is small and matches the expected number of classes.
    evidence: ✓ The target distribution is imbalanced and ordinary random folds omit rare levels. | ✓ Rows share an entity, prompt, overlapping window, or other dependence that would cross random folds.
    leaderboard score n/a → n/a
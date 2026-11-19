# Stratify independent examples  `T.2.2.1`   3 edits, 0 experts
1 scored cases, median improvement +0.00261, 1 improved


- expert 27799930 (Contributor) · amex · v48→v52   Use stratified folds to maintain consistent class ratios across folds. Implement the competition metric as a custom evaluation function so early stopping and model selection optimize the true objective. Moderately reduce early-stopping patience to avoid overfitting on the training metric while still
    evidence: ✓ Labels or binned regression targets are unevenly represented across current folds. | ✗ Rows share entities, overlapping signals, or near-duplicate content across folds. | ✓ Examples are approximately independent and no source shift or target-stratum imbalance requires a specialized split.
    leaderboard score n/a → 0.79418
- expert 18851026 (Master) · commonlitreadabilityprize · v26→v28   Discretize the continuous target into bins and apply stratified K-fold splitting on those bins. This ensures each fold mirrors the overall target distribution, stabilizing both the CV metric and the out-of-fold predictions used for stacking.
    evidence: ✓ Labels or binned regression targets are unevenly represented across current folds. | ✗ Examples are approximately independent and no source shift or target-stratum imbalance requires a specialized split.
    leaderboard score n/a → 0.45803
- expert 55431616 (Grandmaster) · learning · v11→v13   Use stratified cross-validation splits that preserve the target distribution in every fold, so that per-fold threshold optimization and objective alignment reflect the true test-time distribution.
    evidence: ✓ Labels or binned regression targets are unevenly represented across current folds. | ✓ The expected test population matches only an identifiable subset of training data. | ✗ Examples are approximately independent and no source shift or target-stratum imbalance requires a specialized split.
    leaderboard score 0.81502 → 0.81762 (+0.00261)
# Filter or down-weight noisy and mismatched examples  `T.3.3.1`   4 edits, 0 experts
3 scored cases, median improvement +0.00034, 2 improved


- expert 77450317 (Grandmaster) · equity · v17→v19   Load the precomputed outlier IDs and filter them from the training set before fitting. Treat this as a quick probe: make the minimal code change, re-run, and compare validation or leaderboard scores to the baseline. If no improvement is observed, revert.
    evidence: ✓ A known subset has unreliable labels or differs from the intended test population. | ✗ Training images exhibit nuisance variation that valid augmentation could reproduce. | ✓ The competition metric is ranking-based or ordinal, so class reweighting may be invariant or harmful because it affects calibration rather than score ordering.
    leaderboard score 0.69690 → n/a
- expert 77129691 (Master) · equity · v22→v23   Pre-compute outlier scores (e.g., via out-of-fold residuals or prediction confidence thresholds) and remove the flagged samples from training. Use a held-out or public leaderboard score to verify the removal helps rather than hurts. Keep the threshold moderate to avoid discarding too much signal.
    evidence: ✓ A known subset has unreliable labels or differs from the intended test population. | ✗ Training images exhibit nuisance variation that valid augmentation could reproduce. | ✓ The competition metric is ranking-based or ordinal, so class reweighting may be invariant or harmful because it affects calibration rather than score ordering.
    leaderboard score 0.69568 → 0.69602 (+0.00034)
- expert 60264017 (Master) · learning · v1→v2   Train a 'clean' variant of the model using only the subset of training data whose distribution matches the test set (or down-weight the mismatched portion). Compare its predictions against the original model's predictions within the ensemble to measure the gain from distribution alignment.
    evidence: ✓ A known subset has unreliable labels or differs from the intended test population. | ✗ The competition metric is ranking-based or ordinal, so class reweighting may be invariant or harmful because it affects calibration rather than score ordering.
    leaderboard score 0.82788 → 0.82941 (+0.00153)
- expert 58130512 (Master) · learning · v35→v36   Test subsetting training data to only the distribution-matching portion. Expect that the loss of training volume may outweigh the distribution-matching benefit, especially for models that can learn to handle mixed distributions. If the score drops substantially, revert and instead use softer approac
    evidence: ✓ A known subset has unreliable labels or differs from the intended test population. | ✗ The competition metric is ranking-based or ordinal, so class reweighting may be invariant or harmful because it affects calibration rather than score ordering.
    leaderboard score 0.82196 → 0.80408 (-0.01788)
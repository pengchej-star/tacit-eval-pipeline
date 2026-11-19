# Filter or curate examples  `T.3.1.1`   10 edits, 0 experts
9 scored cases, median improvement -0.00325, 4 improved


- expert 77450317 (Grandmaster) · equity · v17→v19   Load the precomputed outlier IDs and filter them from the training set before fitting. Treat this as a quick probe: make the minimal code change, re-run, and compare validation or leaderboard scores to the baseline. If no improvement is observed, revert.
    evidence: ✓ Low-confidence labels, duplicates, or a mismatched source subset can be identified.
    leaderboard score 0.69690 → n/a
- expert 77129691 (Master) · equity · v22→v23   Pre-compute outlier scores (e.g., via out-of-fold residuals or prediction confidence thresholds) and remove the flagged samples from training. Use a held-out or public leaderboard score to verify the removal helps rather than hurts. Keep the threshold moderate to avoid discarding too much signal.
    evidence: ✓ Low-confidence labels, duplicates, or a mismatched source subset can be identified.
    leaderboard score 0.69568 → 0.69602 (+0.00034)
- expert 49576186 (Expert) · hms · v78→v81   Aggregate labels to the unique observation level, remove overlapping windows so each appears once, balance the resulting set across classes, and cache the cleaned dataset for reproducibility. This reduces noise from duplicates and ensures the model sees a representative class distribution.
    evidence: ✓ Low-confidence labels, duplicates, or a mismatched source subset can be identified. | ✓ Rare classes or relevant subgroups contribute too little to the current objective.
    leaderboard score 0.32680 → 0.27977 (-0.04703)
- expert 49576186 (Expert) · hms · v83→v90   Sweep one variable at a time: first toggle which training stage is active, then vary the class filter (include all classes, exclude one class, include only one class), submitting each to get feedback. When filtering out a class degrades the score substantially, revert to using all data. Keep the com
    evidence: ✓ Low-confidence labels, duplicates, or a mismatched source subset can be identified. | ✓ Rare classes or relevant subgroups contribute too little to the current objective.
    leaderboard score 0.27931 → 0.27366 (-0.00565)
- expert 49576186 (Expert) · hms · v93→v95   Test both union and intersection filtering and compare on the leaderboard. Be cautious with intersection filtering: it can reduce the training set too much, causing underfitting or poor generalization, especially when individual criteria are already selective.
    evidence: ✓ Low-confidence labels, duplicates, or a mismatched source subset can be identified.
    leaderboard score 0.26921 → 0.32367 (+0.05446)
- expert 49576186 (Expert) · hms · v125→v127   Try excluding the ambiguous class from training. If the metric worsens, the model likely benefits from seeing those examples — possibly because they regularize predictions or because test data contains such cases. Revert the exclusion and instead try combining it with other improvements.
    evidence: ✓ Low-confidence labels, duplicates, or a mismatched source subset can be identified.
    leaderboard score 0.26861 → 0.27932 (+0.01071)
- expert 49576186 (Expert) · hms · v127→v131   Instead of reverting completely, simplify the data selection logic and combine it with complementary training improvements (label smoothing, mixed-precision training, early stopping). Test the bundle together. If the combined changes beat the original baseline, keep them; the synergy of multiple sma
    evidence: ✓ Low-confidence labels, duplicates, or a mismatched source subset can be identified. | ✓ Rare classes or relevant subgroups contribute too little to the current objective. | ✓ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.27932 → 0.26637 (-0.01295)
- expert 49576186 (Expert) · hms · v152→v157   Try isolating the extra data in a dedicated early training stage so it does not contaminate fine-tuning on clean data. If that still hurts, revert the extra data inclusion entirely and reduce other changed hyperparameters (e.g., input resolution, batch size) back to their proven values. Accept that 
    evidence: ✓ Low-confidence labels, duplicates, or a mismatched source subset can be identified. | ✓ Additional labeled data cover relevant cases with compatible targets.
    leaderboard score 0.27719 → 0.27394 (-0.00325)
- expert 60264017 (Master) · learning · v1→v2   Train a 'clean' variant of the model using only the subset of training data whose distribution matches the test set (or down-weight the mismatched portion). Compare its predictions against the original model's predictions within the ensemble to measure the gain from distribution alignment.
    evidence: ✓ Low-confidence labels, duplicates, or a mismatched source subset can be identified. | ✓ A minority subgroup matches the expected test population and is currently underrepresented.
    leaderboard score 0.82788 → 0.82941 (+0.00153)
- expert 58130512 (Master) · learning · v35→v36   Test subsetting training data to only the distribution-matching portion. Expect that the loss of training volume may outweigh the distribution-matching benefit, especially for models that can learn to handle mixed distributions. If the score drops substantially, revert and instead use softer approac
    evidence: ✓ Low-confidence labels, duplicates, or a mismatched source subset can be identified. | ✓ A minority subgroup matches the expected test population and is currently underrepresented. | ✓ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.82196 → 0.80408 (-0.01788)
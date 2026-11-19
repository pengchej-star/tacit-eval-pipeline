# Filter or deduplicate examples  `T.3.1.1`   6 edits, 0 experts
6 scored cases, median improvement +0.00153, 3 improved


- expert 49576186 (Expert) · hms · v78→v81   Aggregate labels to the unique observation level, remove overlapping windows so each appears once, balance the resulting set across classes, and cache the cleaned dataset for reproducibility. This reduces noise from duplicates and ensures the model sees a representative class distribution.
    evidence: ✓ Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source. | ✓ Rare labels or the test-like subgroup receive little influence under the current loss.
    leaderboard score 0.32680 → 0.27977 (-0.04703)
- expert 49576186 (Expert) · hms · v83→v90   Sweep one variable at a time: first toggle which training stage is active, then vary the class filter (include all classes, exclude one class, include only one class), submitting each to get feedback. When filtering out a class degrades the score substantially, revert to using all data. Keep the com
    evidence: ✓ Rare labels or the test-like subgroup receive little influence under the current loss. | ✓ Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source. | ✓ Training overfits and label-preserving perturbations are supported by the input semantics. | ✓ Previous augmentation attempts beyond the current minimal setup degraded performance.
    leaderboard score 0.27931 → 0.27366 (-0.00565)
- expert 49576186 (Expert) · hms · v93→v95   Test both union and intersection filtering and compare on the leaderboard. Be cautious with intersection filtering: it can reduce the training set too much, causing underfitting or poor generalization, especially when individual criteria are already selective.
    evidence: ✓ Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source.
    leaderboard score 0.26921 → 0.32367 (+0.05446)
- expert 49576186 (Expert) · hms · v125→v127   Try excluding the ambiguous class from training. If the metric worsens, the model likely benefits from seeing those examples — possibly because they regularize predictions or because test data contains such cases. Revert the exclusion and instead try combining it with other improvements.
    evidence: ✓ Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source. | ✓ Rare labels or the test-like subgroup receive little influence under the current loss.
    leaderboard score 0.26861 → 0.27932 (+0.01071)
- expert 60264017 (Master) · learning · v1→v2   Train a 'clean' variant of the model using only the subset of training data whose distribution matches the test set (or down-weight the mismatched portion). Compare its predictions against the original model's predictions within the ensemble to measure the gain from distribution alignment.
    evidence: ✓ Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source.
    leaderboard score 0.82788 → 0.82941 (+0.00153)
- expert 58130512 (Master) · learning · v35→v36   Test subsetting training data to only the distribution-matching portion. Expect that the loss of training volume may outweigh the distribution-matching benefit, especially for models that can learn to handle mixed distributions. If the score drops substantially, revert and instead use softer approac
    evidence: ✓ Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source. | ✓ Rare labels or the test-like subgroup receive little influence under the current loss.
    leaderboard score 0.82196 → 0.80408 (-0.01788)
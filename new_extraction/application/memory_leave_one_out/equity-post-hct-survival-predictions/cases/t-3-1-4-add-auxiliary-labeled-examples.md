# Add auxiliary labeled examples  `T.3.1.4`   4 edits, 0 experts
4 scored cases (improvement signed by each competition's direction), median +0.01763, 3 improved


- expert 49576186 · hms · v150→v152   Filter extra data to keep only high-confidence examples (e.g., those where the dominant class has positive votes and the catch-all/ambiguous class has zero votes), deduplicate by sample identifier, and evaluate on the leaderboard. If the score worsens, the extra data may introduce distribution shift
    evidence: ✓ Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source. | ✓ Compatible extra labeled examples exist but differ in quality or source.
    leaderboard score 0.27393 → 0.27719 (lower is better; worse by 0.00326)
- expert 49576186 · hms · v152→v157   Try isolating the extra data in a dedicated early training stage so it does not contaminate fine-tuning on clean data. If that still hurts, revert the extra data inclusion entirely and reduce other changed hyperparameters (e.g., input resolution, batch size) back to their proven values. Accept that 
    evidence: ✓ Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source. | ✓ Compatible extra labeled examples exist but differ in quality or source. | ✓ Previous augmentation attempts beyond the current minimal setup degraded performance.
    leaderboard score 0.27719 → 0.27394 (lower is better; improved by 0.00325)
- expert 49576186 · hms · v169→v171   Merge the extra samples into the training pipeline, ensuring all feature arrays are padded or truncated to match the expected input dimensions. Evaluate on the held-out metric. If the score improves, keep the extra data; otherwise revert.
    evidence: ✓ Compatible extra labeled examples exist but differ in quality or source. | ✓ Previous augmentation attempts beyond the current minimal setup degraded performance.
    leaderboard score 0.28251 → 0.26488 (lower is better; improved by 0.01763)
- expert 49576186 · hms · v172→v180   Add the external data, train, and evaluate on the leaderboard. Then remove it and evaluate with the same or updated checkpoint. Compare both scores. If the extra data does not improve or hurts the score, remove it and keep the simpler pipeline. The cleaner pipeline may generalize better if the exter
    evidence: ✓ Compatible extra labeled examples exist but differ in quality or source. | ✓ Previous augmentation attempts beyond the current minimal setup degraded performance. | ✓ Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source.
    leaderboard score 0.28320 → 0.26166 (lower is better; improved by 0.02155)
# Simplify the prediction head  `T.4.4.2`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00940, 1 improved


- expert 13848868 · ranzcr · v16→v21   Replace the per-class multi-head design with a single shared classification head. Evaluate with the same fold ensemble. An initial score drop may occur if checkpoints are mismatched; ensure weights correspond to the new architecture before concluding the comparison.
    evidence: ✓ Extra heads or layers have failed controlled comparisons or overfit. | ✓ The checkpoints being loaded were trained with a different head architecture than the current inference model, causing dimension or weight mismatches.
    leaderboard score 0.94293 → 0.95233 (higher is better; improved by 0.00940)
- expert 17371717 · commonlitreadabilityprize · v9→v11   Be cautious about changing the model head architecture at inference time without retraining checkpoints to match. If checkpoints were trained with a simpler head, loading them into a more complex head will likely degrade performance. Verify architecture-checkpoint compatibility before submitting, an
    evidence: ✓ The current pooling or linear head discards useful spatial, temporal, or hidden-layer information. | ✓ Extra heads or layers have failed controlled comparisons or overfit. | ✓ The checkpoints being loaded were trained with a different head architecture than the current inference model, causing dimension or weight mismatches.
    leaderboard score 0.47268 → 0.47606 (lower is better; worse by 0.00338)
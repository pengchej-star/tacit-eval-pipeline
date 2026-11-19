# Average valid transformed input views  `T.5.2.3`   8 edits, 0 experts
7 scored cases (improvement signed by each competition's direction), median +0.00028, 6 improved


- expert 15372370 · ranzcr · v1→v3   Run inference on both the original and the transformed input, apply the output activation to each, average the two prediction arrays, and use the mean as the final prediction. Compare the leaderboard score with and without TTA to decide whether to keep it.
    evidence: ✓ The task is invariant to candidate transformations and predictions vary across those views.
    leaderboard score n/a → 0.96342 (higher is better)
- expert 15372370 · ranzcr · v3→v4   Run inference with and without the TTA and compare leaderboard or validation scores. If the gain is negligible for a single model, drop TTA to save compute and instead pursue multi-model ensembling, which typically yields larger gains.
    evidence: ✓ The task is invariant to candidate transformations and predictions vary across those views.
    leaderboard score 0.96342 → 0.96341 (higher is better; worse by 0.00001)
- expert 15372370 · ranzcr · v4→v5   Load all checkpoints, run each on both the original and augmented (e.g., flipped) inputs, and equally average all predictions. This simple uniform ensemble often gives a meaningful boost before any weight tuning.
    evidence: ✓ The task is invariant to candidate transformations and predictions vary across those views.
    leaderboard score 0.96341 → 0.96726 (higher is better; improved by 0.00385)
- expert 15372370 · ranzcr · v7→v8   Apply horizontal-flip test-time augmentation by averaging the model's post-activation outputs on the original and flipped inputs. Expect a small but reliable improvement; the gain is additive on top of fold averaging because it reduces a different source of variance (spatial symmetry).
    evidence: ✗ Useful fold-trained checkpoints are omitted or too few folds limit training coverage. | ✓ The task is invariant to candidate transformations and predictions vary across those views.
    leaderboard score 0.96804 → 0.96830 (higher is better; improved by 0.00025)
- expert 15372370 · ranzcr · v8→v11   Test stochastic augmentation-based TTA cautiously: if it causes a large score drop, revert immediately. Random spatial transforms at test time can introduce harmful distortions that hurt more than they help, especially when the task has orientation-sensitive semantics. Prefer deterministic, semantic
    evidence: ✓ The task is invariant to candidate transformations and predictions vary across those views. | ✗ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.96830 → 0.96835 (higher is better; improved by 0.00005)
- expert 15372370 · ranzcr · v11→v14   Run full inference at the original resolution and at a higher resolution separately, average across folds at each resolution, then blend the two sets of predictions with a weighted average (e.g., giving slightly more weight to the original resolution). Verify that the blend outperforms either resolu
    evidence: ✓ The task is invariant to candidate transformations and predictions vary across those views. | ✓ Useful fold-trained checkpoints are omitted or too few folds limit training coverage.
    leaderboard score 0.96835 → 0.96883 (higher is better; improved by 0.00049)
- expert 15164527 · ranzcr · v15→v16   Apply test-time augmentation by running each model on both the original and a geometrically transformed version of each input (e.g., horizontal flip), then average the outputs before ensemble blending. This is complementary to blend-weight tuning and typically yields a small but consistent gain when
    evidence: ✓ The task is invariant to candidate transformations and predictions vary across those views.
    leaderboard score 0.96778 → 0.96806 (higher is better; improved by 0.00028)
- expert 15164527 · ranzcr · v15→v16   Add test-time augmentation on top of the already-tuned ensemble rather than before tuning it. TTA and ensemble combination address different error sources (single-model variance vs. inter-model calibration), so their gains tend to stack. After adding TTA, re-tuning blend weights may yield little fur
    evidence: ✓ The task is invariant to candidate transformations and predictions vary across those views.
    leaderboard score 0.96778 → 0.96806 (higher is better; improved by 0.00028)
# Average valid transformed views  `T.6.2.3`   25 edits, 0 experts
23 scored cases (improvement signed by each competition's direction), median +0.00048, 17 improved


- expert 53424936 · hms · v8→v12   Pass each available temporal crop through the model independently, convert logits to probabilities, and average the probability vectors across crops before (or after) averaging across ensemble members. Expect small but consistent gains; verify with a leaderboard or held-out set submission.
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✗ Available fold checkpoints were trained with incompatible feature layouts. | ✗ Available fold checkpoints differ in quality or some are currently unused.
    leaderboard score 0.22803 → 0.22786 (lower is better; improved by 0.00018)
- expert 53424936 · hms · v24→v26   Run a controlled A/B comparison: first enable multi-view TTA and submit, then disable it (center-only) and submit, keeping everything else identical. Compare leaderboard scores. If the difference is negligible or negative, drop TTA to reduce complexity and inference cost. Be cautious when combining 
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.22647 → 0.22650 (lower is better; worse by 0.00003)
- expert 50376011 · hms · v59→v62   Toggle the stochastic test-time feature on and off in otherwise identical runs and compare leaderboard scores. If the stochastic version does not beat the deterministic baseline, revert and move on. Keep the experiment isolated to a single model so the signal is not confounded by ensemble effects.
    evidence: ✓ Dropout or other random inference operations are active or being proposed. | ✗ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.34053 → 0.35531 (lower is better; worse by 0.01479)
- expert 50376011 · hms · v77→v79   Introduce a configurable count of test-time augmentation or repeated inference passes. This can substantially improve a single-model score (closing the gap toward the ensemble), but may not fully replace a diverse multi-model ensemble. Tune the count alongside batch size to stay within memory limits
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✓ Dropout or other random inference operations are active or being proposed. | ✗ Repeated forward passes with the same weights and inputs are numerically identical. | ✓ Available fold checkpoints differ in quality or some are currently unused.
    leaderboard score 0.36160 → 0.33044 (lower is better; improved by 0.03116)
- expert 50376011 · hms · v166→v169   Try a moderate fold count (not the maximum) combined with multiple diverse checkpoints rather than maximizing fold count with a single checkpoint. Test both dimensions independently and in combination, comparing leaderboard scores to find the sweet spot.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✗ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.25358 → 0.25069 (lower is better; improved by 0.00290)
- expert 49524919 · hms · v6→v13   For each candidate checkpoint, evaluate with and without test-time augmentation. Do not assume the TTA effect is constant across checkpoints—always test the combination. When the metric consistently improves with TTA across checkpoints, keep it enabled in the final submission.
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.51388 → 0.47129 (lower is better; improved by 0.04259)
- expert 52551258 · hms · v13→v14   Apply horizontal and vertical flips as TTA, average predictions across all augmented views and models, then renormalize. Monitor the leaderboard: if the score worsens, the augmentations likely break meaningful spatial structure (e.g., frequency ordering or temporal direction) and should be removed. 
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.30219 → 0.31017 (lower is better; worse by 0.00798)
- expert 52551258 · hms · v17→v18   Apply spatial flips (horizontal, vertical, combined) as test-time augmentations and average predictions across all augmented views and folds. When the base model is already strong and the flips respect the data's physical symmetry, expect a small but reliable gain. If the base model is weak, TTA may
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.28185 → 0.28137 (lower is better; improved by 0.00048)
- expert 15082684 · ranzcr · v31→v33   Increase the inference resolution to match a checkpoint trained at that higher resolution. When the larger input size exceeds single-device memory, enable multi-device inference to accommodate it.
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✓ Available fold checkpoints differ in quality or some are currently unused.
    leaderboard score 0.96823 → n/a (higher is better)
- expert 15372370 · ranzcr · v1→v3   Run inference on both the original and the transformed input, apply the output activation to each, average the two prediction arrays, and use the mean as the final prediction. Compare the leaderboard score with and without TTA to decide whether to keep it.
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score n/a → 0.96342 (higher is better)
- expert 15372370 · ranzcr · v3→v4   Run inference with and without the TTA and compare leaderboard or validation scores. If the gain is negligible for a single model, drop TTA to save compute and instead pursue multi-model ensembling, which typically yields larger gains.
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.96342 → 0.96341 (higher is better; worse by 0.00001)
- expert 15372370 · ranzcr · v4→v5   Load all checkpoints, run each on both the original and augmented (e.g., flipped) inputs, and equally average all predictions. This simple uniform ensemble often gives a meaningful boost before any weight tuning.
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✗ Dropout or other random inference operations are active or being proposed. | ✓ Repeated forward passes with the same weights and inputs are numerically identical. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.96341 → 0.96726 (higher is better; improved by 0.00385)
- expert 15372370 · ranzcr · v7→v8   Apply horizontal-flip test-time augmentation by averaging the model's post-activation outputs on the original and flipped inputs. Expect a small but reliable improvement; the gain is additive on top of fold averaging because it reduces a different source of variance (spatial symmetry).
    evidence: ✗ Available fold checkpoints differ in quality or some are currently unused. | ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.96804 → 0.96830 (higher is better; improved by 0.00025)
- expert 15372370 · ranzcr · v8→v11   Test stochastic augmentation-based TTA cautiously: if it causes a large score drop, revert immediately. Random spatial transforms at test time can introduce harmful distortions that hurt more than they help, especially when the task has orientation-sensitive semantics. Prefer deterministic, semantic
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✗ Available fold checkpoints differ in quality or some are currently unused. | ✓ Dropout or other random inference operations are active or being proposed. | ✓ Repeated forward passes with the same weights and inputs are numerically identical. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.96830 → 0.96835 (higher is better; improved by 0.00005)
- expert 15372370 · ranzcr · v11→v14   Run full inference at the original resolution and at a higher resolution separately, average across folds at each resolution, then blend the two sets of predictions with a weighted average (e.g., giving slightly more weight to the original resolution). Verify that the blend outperforms either resolu
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✗ Available fold checkpoints were trained with incompatible feature layouts. | ✗ Dropout or other random inference operations are active or being proposed. | ✓ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.96835 → 0.96883 (higher is better; improved by 0.00049)
- expert 15164527 · ranzcr · v15→v16   Apply test-time augmentation by running each model on both the original and a geometrically transformed version of each input (e.g., horizontal flip), then average the outputs before ensemble blending. This is complementary to blend-weight tuning and typically yields a small but consistent gain when
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.96778 → 0.96806 (higher is better; improved by 0.00028)
- expert 15164527 · ranzcr · v15→v16   Add test-time augmentation on top of the already-tuned ensemble rather than before tuning it. TTA and ensemble combination address different error sources (single-model variance vs. inter-model calibration), so their gains tend to stack. After adding TTA, re-tuning blend weights may yield little fur
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.96778 → 0.96806 (higher is better; improved by 0.00028)
- expert 50496431 · hms · v5→v7   Apply horizontal flip TTA: run inference on both the original and horizontally-flipped input, apply softmax to each, and average the two probability vectors. This is low-cost (doubles inference time) and typically yields a small but consistent improvement.
    evidence: ✗ Available fold checkpoints differ in quality or some are currently unused. | ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.42903 → 0.42697 (lower is better; improved by 0.00206)
- expert 50496431 · hms · v16→v17   Move TTA duplication, softmax, and averaging into the model's forward pass so that every inference call returns fully normalized, TTA-averaged probabilities. This ensures softmax is applied before averaging (averaging probabilities rather than logits) and eliminates mismatches between training and i
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✗ Dropout or other random inference operations are active or being proposed. | ✓ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.34815 → 0.34713 (lower is better; improved by 0.00102)
- expert 50496431 · hms · v18→v22   Toggle ensemble members and augmentation on/off one or two at a time, submitting each variant. Start by isolating the effect of test-time augmentation alone, then ablate model groups. Track which additions improve the score and which hurt, converging on the subset where every included component cont
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.34209 → 0.33898 (lower is better; improved by 0.00311)
- expert 50496431 · hms · v18→v20   Re-evaluate TTA after each significant change to ensemble composition. If removing TTA improves or matches the score, drop it—the additional diversity from more models can substitute for augmentation-based variance reduction, and TTA adds inference cost and potential shape/logic bugs.
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.34209 → 0.37365 (lower is better; worse by 0.03157)
- expert 50496431 · hms · v52→v54   Test with and without the augmentation in consecutive submissions after other preprocessing changes have stabilized. Implement it efficiently by concatenating original and augmented inputs into one batch, running a single forward pass, and averaging paired outputs. Keep it enabled only when the metr
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.33128 → 0.31954 (lower is better; improved by 0.01174)
- expert 50496431 · hms · v56→v57   Identify the domain-specific symmetry (e.g., swapping left/right sensor channels), implement a transform that permutes input channels accordingly, run a separate inference pass with the transformed input, and average those predictions into the ensemble. This adds a complementary augmentation grounde
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.31538 → 0.30899 (lower is better; improved by 0.00639)
- expert 50496431 · hms · v58→v60   Test flip TTA on each model branch independently, changing only one variable at a time. Do not combine a new TTA with simultaneous preprocessing changes (e.g., resolution), because confounded changes make it impossible to attribute score changes. If the combined change hurts, revert both and re-test
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.31716 → 0.31262 (lower is better; improved by 0.00454)
- expert 50496431 · hms · v75→v77   Toggle the augmentation off and on in separate submissions, comparing each against the current best. If the score difference is very small (within noise), re-run or check for non-determinism before concluding. Accept the setting that yields the better score, but be aware that re-running the same con
    evidence: ✓ The task has valid input symmetries or multiple aligned views of the same target. | ✗ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.27839 → 0.29564 (lower is better; worse by 0.01725)
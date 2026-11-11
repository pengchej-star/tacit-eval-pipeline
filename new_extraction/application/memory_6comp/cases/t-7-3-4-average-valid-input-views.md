# Average valid input views  `T.7.3.4`   16 edits, 0 experts
16 scored cases, median improvement -0.00048, 5 improved


- expert 49524919 (Grandmaster) · hms · v3→v6   First fix any data-loading or preprocessing bugs and disable test-time augmentation to establish a clean single-pass baseline. Only after confirming the baseline is reasonable, toggle augmentation on and measure its isolated effect. If the gain is negligible, focus effort on improving the model weig
    evidence: ✓ Input transformations preserve target meaning and were supported by the training representation.
    leaderboard score 0.51664 → 0.51388 (-0.00276)
- expert 53424936 (Master) · hms · v8→v12   Pass each available temporal crop through the model independently, convert logits to probabilities, and average the probability vectors across crops before (or after) averaging across ensemble members. Expect small but consistent gains; verify with a leaderboard or held-out set submission.
    evidence: ✗ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Input transformations preserve target meaning and were supported by the training representation.
    leaderboard score 0.22803 → 0.22786 (-0.00018)
- expert 53424936 (Master) · hms · v24→v26   Run a controlled A/B comparison: first enable multi-view TTA and submit, then disable it (center-only) and submit, keeping everything else identical. Compare leaderboard scores. If the difference is negligible or negative, drop TTA to reduce complexity and inference cost. Be cautious when combining 
    evidence: ✓ Input transformations preserve target meaning and were supported by the training representation.
    leaderboard score 0.22647 → 0.22650 (+0.00003)
- expert 50376011 (Grandmaster) · hms · v59→v62   Toggle the stochastic test-time feature on and off in otherwise identical runs and compare leaderboard scores. If the stochastic version does not beat the deterministic baseline, revert and move on. Keep the experiment isolated to a single model so the signal is not confounded by ensemble effects.
    evidence: ✓ The model has usable stochastic layers and repeated inference is intended to sample them. | ✓ Stochastic layers are active at inference without a validated repeated-pass strategy.
    leaderboard score 0.34053 → 0.35531 (+0.01479)
- expert 50376011 (Grandmaster) · hms · v77→v79   Introduce a configurable count of test-time augmentation or repeated inference passes. This can substantially improve a single-model score (closing the gap toward the ensemble), but may not fully replace a diverse multi-model ensemble. Tune the count alongside batch size to stay within memory limits
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Independent training seeds produce materially different errors. | ✓ The model has usable stochastic layers and repeated inference is intended to sample them. | ✗ Stochastic layers are active at inference without a validated repeated-pass strategy.
    leaderboard score 0.36160 → 0.33044 (-0.03116)
- expert 50376011 (Grandmaster) · hms · v166→v169   Try a moderate fold count (not the maximum) combined with multiple diverse checkpoints rather than maximizing fold count with a single checkpoint. Test both dimensions independently and in combination, comparing leaderboard scores to find the sweet spot.
    evidence: ✓ Only part of an available compatible cross-validation checkpoint set is used. | ✓ Fold quality differs consistently on comparable validation evidence. | ✓ Independent training seeds produce materially different errors. | ✓ Several compatible training snapshots of one model are available for weight averaging.
    leaderboard score 0.25358 → 0.25069 (-0.00290)
- expert 49524919 (Grandmaster) · hms · v6→v13   For each candidate checkpoint, evaluate with and without test-time augmentation. Do not assume the TTA effect is constant across checkpoints—always test the combination. When the metric consistently improves with TTA across checkpoints, keep it enabled in the final submission.
    evidence: ✓ Input transformations preserve target meaning and were supported by the training representation.
    leaderboard score 0.51388 → 0.47129 (-0.04259)
- expert 49524919 (Grandmaster) · hms · v66→v67   When swapping to a new checkpoint, also update the inference-time transforms (dropout, normalization order, additional augmentations) to match or complement the training regime of that checkpoint. Test the combined change as a single submission; if it beats both the old checkpoint and the new checkp
    evidence: ✓ Input transformations preserve target meaning and were supported by the training representation. | ✓ The model has usable stochastic layers and repeated inference is intended to sample them.
    leaderboard score 0.29086 → 0.29040 (-0.00045)
- expert 52551258 (Expert) · hms · v13→v14   Apply horizontal and vertical flips as TTA, average predictions across all augmented views and models, then renormalize. Monitor the leaderboard: if the score worsens, the augmentations likely break meaningful spatial structure (e.g., frequency ordering or temporal direction) and should be removed. 
    evidence: ✗ Input transformations preserve target meaning and were supported by the training representation.
    leaderboard score 0.30219 → 0.31017 (+0.00798)
- expert 52551258 (Expert) · hms · v17→v18   Apply spatial flips (horizontal, vertical, combined) as test-time augmentations and average predictions across all augmented views and folds. When the base model is already strong and the flips respect the data's physical symmetry, expect a small but reliable gain. If the base model is weak, TTA may
    evidence: ✓ Input transformations preserve target meaning and were supported by the training representation.
    leaderboard score 0.28185 → 0.28137 (-0.00048)
- expert 50496431 (Grandmaster) · hms · v5→v7   Apply horizontal flip TTA: run inference on both the original and horizontally-flipped input, apply softmax to each, and average the two probability vectors. This is low-cost (doubles inference time) and typically yields a small but consistent improvement.
    evidence: ✓ Input transformations preserve target meaning and were supported by the training representation. | ✗ Only part of an available compatible cross-validation checkpoint set is used.
    leaderboard score 0.42903 → 0.42697 (-0.00206)
- expert 50496431 (Grandmaster) · hms · v18→v20   Re-evaluate TTA after each significant change to ensemble composition. If removing TTA improves or matches the score, drop it—the additional diversity from more models can substitute for augmentation-based variance reduction, and TTA adds inference cost and potential shape/logic bugs.
    evidence: ✓ Input transformations preserve target meaning and were supported by the training representation.
    leaderboard score 0.34209 → 0.37365 (+0.03157)
- expert 50496431 (Grandmaster) · hms · v52→v54   Test with and without the augmentation in consecutive submissions after other preprocessing changes have stabilized. Implement it efficiently by concatenating original and augmented inputs into one batch, running a single forward pass, and averaging paired outputs. Keep it enabled only when the metr
    evidence: ✓ Input transformations preserve target meaning and were supported by the training representation.
    leaderboard score 0.33128 → 0.31954 (-0.01174)
- expert 50496431 (Grandmaster) · hms · v56→v57   Identify the domain-specific symmetry (e.g., swapping left/right sensor channels), implement a transform that permutes input channels accordingly, run a separate inference pass with the transformed input, and average those predictions into the ensemble. This adds a complementary augmentation grounde
    evidence: ✓ Input transformations preserve target meaning and were supported by the training representation.
    leaderboard score 0.31538 → 0.30899 (-0.00639)
- expert 50496431 (Grandmaster) · hms · v58→v60   Test flip TTA on each model branch independently, changing only one variable at a time. Do not combine a new TTA with simultaneous preprocessing changes (e.g., resolution), because confounded changes make it impossible to attribute score changes. If the combined change hurts, revert both and re-test
    evidence: ✓ Input transformations preserve target meaning and were supported by the training representation.
    leaderboard score 0.31716 → 0.31262 (-0.00454)
- expert 50496431 (Grandmaster) · hms · v75→v77   Toggle the augmentation off and on in separate submissions, comparing each against the current best. If the score difference is very small (within noise), re-run or check for non-determinism before concluding. Accept the setting that yields the better score, but be aware that re-running the same con
    evidence: ✓ Input transformations preserve target meaning and were supported by the training representation.
    leaderboard score 0.27839 → 0.29564 (+0.01725)
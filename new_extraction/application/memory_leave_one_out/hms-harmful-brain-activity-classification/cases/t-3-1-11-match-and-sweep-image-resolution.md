# Match and sweep image resolution  `T.3.1.11`   13 edits, 0 experts
12 scored cases, median improvement +0.00540, 10 improved


- expert 13848868 (Grandmaster) · ranzcr · v2→v5   First increase the input resolution (which typically has the larger effect), then sweep the number of folds upward. Use all available folds unless a specific fold degrades the score. Confirm each change with a leaderboard submission since the two levers can interact.
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail.
    leaderboard score 0.93064 → 0.93873 (+0.00809)
- expert 13848868 (Grandmaster) · ranzcr · v10→v11   If testing a resolution increase at inference time, change only the resolution and keep all other architecture details (head layers, post-processing) identical so the effect can be isolated. If the score drops, revert; do not assume higher resolution is always better when weights were trained at a d
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail.
    leaderboard score 0.94330 → 0.93722 (-0.00608)
- expert 13848868 (Grandmaster) · ranzcr · v30→v35   Sweep inference resolution in discrete steps around the training resolution. Test one step above and one step below. If going larger hurts, revert. The best inference resolution is often at or modestly above the training resolution, not the maximum that fits in memory.
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail.
    leaderboard score 0.94719 → 0.95590 (+0.00871)
- expert 13848868 (Grandmaster) · ranzcr · v36→v37   Set the inference input resolution to match the resolution the checkpoint was trained at. Start with raw score averaging (no rank transform) as the baseline, then toggle the rank transform to see which post-processing is better for this particular checkpoint.
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail.
    leaderboard score 0.95509 → 0.95762 (+0.00253)
- expert 15173072 (Contributor) · ranzcr · v12→v13   Try reducing the input resolution by ~20% while proportionally increasing the batch size. If the score holds or improves, keep the smaller resolution — it likely better matches the resolution the checkpoint was trained on and avoids distribution shift from upscaling.
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail. | ✗ Image input statistics differ from the checkpoint’s training preprocessing.
    leaderboard score 0.95987 → 0.96062 (+0.00075)
- expert 13521245 (Grandmaster) · ranzcr · v8→v10   Sweep the test-time input resolution in small increments around the training resolution, submitting each to evaluate. Expect a non-monotonic curve: slightly larger resolution than training can help (capturing more detail), but too large or too small hurts. Keep the resolution that peaks on the evalu
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail. | ✗ Image input statistics differ from the checkpoint’s training preprocessing.
    leaderboard score 0.94959 → 0.95705 (+0.00746)
- expert 13521245 (Grandmaster) · ranzcr · v10→v11   Probe resolutions on both sides of the current best by changing only the resize target and submitting. If a smaller resolution drops the score noticeably (e.g., more than 1% absolute on the ranking metric), revert to the larger resolution and stop searching downward. The best resolution is typically
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail. | ✗ Image input statistics differ from the checkpoint’s training preprocessing.
    leaderboard score 0.95705 → 0.94487 (-0.01218)
- expert 13521245 (Grandmaster) · ranzcr · v12→v13   Read the expected spatial dimensions directly from the model's input tensor shape and use that to set the image decoding/resizing target, rather than maintaining a separate hardcoded resolution variable.
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail.
    leaderboard score 0.81275 → 0.83623 (+0.02348)
- expert 13702907 (Contributor) · ranzcr · v5→v6   Audit the full pipeline to ensure the image dimensions in the data-loading/decoding step and the model input-shape specification both match the resolution used during training. A single index or variable mismatch can cause a significant score drop without raising any runtime error.
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail.
    leaderboard score n/a → 0.95131
- expert 13702907 (Contributor) · ranzcr · v8→v9   Increase the image decoding/resizing resolution at inference time in moderate increments (e.g., ~15-20% larger). Compare the leaderboard score to the baseline resolution. Note that gains depend on whether the pretrained model generalizes to the new resolution; if the model was trained at a fixed siz
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail.
    leaderboard score 0.94510 → 0.95050 (+0.00540)
- expert 13702907 (Contributor) · ranzcr · v20→v23   Increase the inference resolution and use the matching higher-resolution checkpoint. Submit multiple times (or use cross-validation) to separate genuine improvement from leaderboard noise. If the gain is comparable to run-to-run variance, treat it as inconclusive rather than a confirmed improvement.
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail.
    leaderboard score 0.95173 → 0.95237 (+0.00064)
- expert 13577502 (Expert) · ranzcr · v4→v5   Replace the legacy image-loading pipeline with the framework's optimized data pipeline, increase input resolution substantially, and swap in a stronger pretrained checkpoint. Expect that the resolution increase and better checkpoint together can yield a large score jump (several AUC points), though 
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail.
    leaderboard score 0.88199 → 0.95180 (+0.06981)
- expert 13577502 (Expert) · ranzcr · v6→v12   Sweep the inference resize dimension in coarse steps (e.g., 512, 600, 800, 900, 1000) and evaluate each on the target metric. Expect a non-monotonic curve: too small loses detail, too large mismatches the training distribution. Narrow the search around the best region and pick the resolution that pe
    evidence: ✓ The inference image size differs from training or may discard task-relevant detail.
    leaderboard score 0.94950 → 0.95324 (+0.00373)
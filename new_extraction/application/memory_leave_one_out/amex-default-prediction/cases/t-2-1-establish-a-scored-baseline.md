# Establish a scored baseline  `T.2.1`   4 edits, 0 experts
1 scored cases, median improvement +0.00071, 1 improved


- expert 75145694 (Expert) · equity · v1→v3   In the first version, assemble a complete pipeline that includes: (1) a non-parametric survival transform (e.g., Kaplan-Meier probabilities) as the regression target, (2) importing one or more external pretrained models for blending, (3) a local evaluation function matching the competition metric, a
    evidence: ✓ No complete pipeline has produced a scored prediction file. | ✓ Available model checkpoints or fold outputs have not been tested in the current ensemble or evaluation. | ✓ A rewritten or refactored pipeline has not been verified to reproduce the previous pipeline's outputs before trusting new scores.
    leaderboard score 0.68795 → 0.68865 (+0.00071)
- expert 77386286 (Expert) · equity · v1→v2   Build and submit a complete end-to-end pipeline as quickly as possible to establish a numeric baseline. This anchors all future experiments and reveals whether the task is easy or hard relative to the leaderboard distribution.
    evidence: ✓ No complete pipeline has produced a scored prediction file.
    leaderboard score n/a → 0.69332
- expert 6803050 (Master) · google · v1→v6   After the minimal pipeline produces a syntactically valid submission file, submit it immediately—even if predictions are not yet polished—to confirm the format is accepted and get a baseline score. Then iterate on post-processing. This avoids spending many versions on details that may not matter or 
    evidence: ✓ No complete pipeline has produced a scored prediction file. | ✓ Post-processing or formatting edits have not been externally validated to confirm the submission file is still correctly structured.
    leaderboard score n/a → n/a
- expert 53747598 (Master) · hms · v11→v12   Submit once the full pipeline is functionally complete—before tuning further—to establish a reliable baseline score. This confirms correctness end-to-end and provides a reference point so that subsequent changes (swapping checkpoints, adjusting weights) can be evaluated as improvements or regression
    evidence: ✓ No complete pipeline has produced a scored prediction file. | ✓ A score movement cannot be attributed to a specific change or exceeds no-change variability only slightly. | ✓ Post-processing or formatting edits have not been externally validated to confirm the submission file is still correctly structured.
    leaderboard score n/a → 0.23270
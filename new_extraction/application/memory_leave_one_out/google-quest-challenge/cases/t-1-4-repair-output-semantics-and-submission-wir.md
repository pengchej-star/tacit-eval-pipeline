# Repair output semantics and submission wiring  `T.1.4`   12 edits, 0 experts
4 scored cases (improvement signed by each competition's direction), median +0.00047, 3 improved


- expert 27389424 · amex · v7→v8   Verify that the submission contains properly calibrated probabilities by applying the appropriate inverse-link function (e.g., sigmoid for binary classification) to raw model outputs. Plot histograms of both raw and transformed predictions to confirm the distribution is in [0,1] and has a sensible s
    evidence: ✓ Written predictions have the wrong direction, range, normalization, or source variable. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.78358 (higher is better)
- expert 28984551 · amex · v12→v13   Use the classifier variant of the model and extract class probabilities (not raw predictions) as stacking features. This keeps all base-learner outputs on the same [0,1] probability scale, improving ensemble coherence and typically the final metric.
    evidence: ✓ Written predictions have the wrong direction, range, normalization, or source variable.
    leaderboard score 0.79232 → 0.79279 (higher is better; improved by 0.00047)
- expert 77450317 · equity · v13→v14   Give each model family's predictions a distinct output filename so all intermediate predictions are preserved. This allows flexible re-blending and independent submission of any component without re-running the full pipeline.
    evidence: ✓ Written predictions have the wrong direction, range, normalization, or source variable. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.69597 (higher is better)
- expert 77129691 · equity · v1→v2   Negate the predictions and resubmit. If the score jumps to roughly (1 − old_score), the sign was inverted. Always verify whether the evaluation expects higher predictions to mean higher risk or longer survival, and align accordingly.
    evidence: ✓ Written predictions have the wrong direction, range, normalization, or source variable. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score 0.29019 → 0.69005 (higher is better; improved by 0.39986)
- expert 73671444 · equity · v8→v9   Always write the final predictions to the exact filename the platform expects (typically 'submission.csv'). When refactoring inference code, verify the output filename has not been inadvertently changed.
    evidence: ✓ Written predictions have the wrong direction, range, normalization, or source variable. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.68636 (higher is better)
- expert 75145694 · equity · v20→v21   Before blending, verify that all model outputs share the same monotonic direction with respect to the target. Compute rank correlations between each model's predictions and the others; if one is negatively correlated, negate its outputs. Add an explicit sign-correction step in the blending pipeline 
    evidence: ✓ Written predictions have the wrong direction, range, normalization, or source variable. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score 0.68959 → 0.68978 (higher is better; improved by 0.00020)
- expert 75145694 · equity · v36→v38   Before blending, verify the new model's prediction direction by checking its standalone concordance or correlation with the target. If the metric is sign-sensitive (e.g., concordance index), negate or rank-transform the predictions and compare. Add debug prints of prediction statistics to catch the 
    evidence: ✓ Written predictions have the wrong direction, range, normalization, or source variable. | ✓ Execution stops at an import, file access, device operation, or library call. | ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ The executed ensemble does not match its configured members or weights.
    leaderboard score n/a → 0.69283 (higher is better)
- expert 49524919 · hms · v119→v120   After any refactor, explicitly check that the submission output references the final combined blend variable. Name intermediate and final prediction columns with a clear hierarchy. Treat the submission assignment line as a critical checkpoint and verify it matches the intended aggregation level befo
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✓ Written predictions have the wrong direction, range, normalization, or source variable. | ✗ Execution stops at an import, file access, device operation, or library call. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score n/a → 0.24466 (lower is better)
- expert 52551258 · hms · v3→v4   Always normalize averaged probability predictions to sum to 1 before submission when the metric is a divergence or log-likelihood. However, change only one thing at a time so the effect of normalization can be isolated from other modifications.
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✓ Written predictions have the wrong direction, range, normalization, or source variable. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score 0.37116 → 0.37553 (lower is better; worse by 0.00437)
- expert 55591012 · learning · v49→v50   Always include the file-write step that saves predictions in the required format before submitting. When a run unexpectedly produces no score, check that the output file is actually written with the correct name, columns, and path.
    evidence: ✓ Written predictions have the wrong direction, range, normalization, or source variable.
    leaderboard score n/a → 0.82075 (higher is better)
- expert 15173072 · ranzcr · v11→v12   Check whether the training labels were scaled (e.g., percentages vs. fractions). If so, apply the inverse scaling to predictions before submission. A dramatic score jump after rescaling confirms the mismatch. Always verify that the prediction range matches what the model was trained to output.
    evidence: ✓ Written predictions have the wrong direction, range, normalization, or source variable. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.95987 (higher is better)
- expert 13702907 · ranzcr · v2→v3   Trace the exact variable that is written to the submission file and verify it is the same object that holds the ensemble-averaged predictions, not a leftover single-model output. A quick sanity check is to compare the written array's values against the ensemble array before saving.
    evidence: ✓ Written predictions have the wrong direction, range, normalization, or source variable. | ✗ Execution stops at an import, file access, device operation, or library call. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score n/a → 0.94606 (higher is better)
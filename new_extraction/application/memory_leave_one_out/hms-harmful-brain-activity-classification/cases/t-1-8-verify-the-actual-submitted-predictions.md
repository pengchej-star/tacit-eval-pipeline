# Verify the actual submitted predictions  `T.1.8`   17 edits, 0 experts
8 scored cases (improvement signed by each competition's direction), median +0.29825, 6 improved


- expert 27389424 · amex · v7→v8   Verify that the submission contains properly calibrated probabilities by applying the appropriate inverse-link function (e.g., sigmoid for binary classification) to raw model outputs. Plot histograms of both raw and transformed predictions to confirm the distribution is in [0,1] and has a sensible s
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The output file is missing, constant, stale or produced from the wrong input data.
    leaderboard score n/a → 0.78358 (higher is better)
- expert 73671444 · equity · v8→v9   Always write the final predictions to the exact filename the platform expects (typically 'submission.csv'). When refactoring inference code, verify the output filename has not been inadvertently changed.
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The output file is missing, constant, stale or produced from the wrong input data.
    leaderboard score n/a → 0.68636 (higher is better)
- expert 7823861 · google · v30→v31   Ensure the final submission dataframe is explicitly saved to the expected file path at the end of the notebook. Also check for subtle syntax errors (e.g., bitwise vs. comparison operators) that silently corrupt values without raising exceptions.
    evidence: ✓ The output file is missing, constant, stale or produced from the wrong input data.
    leaderboard score n/a → 0.45136 (higher is better)
- expert 7018718 · google · v37→v45   After discretization, check each column for degeneracy (all values identical). For any degenerate column, revert to the original continuous predictions. Prefer an exact constant-check over a variance threshold, as the threshold can be fragile. Also rescale surviving discretized columns to a standard
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The output file is missing, constant, stale or produced from the wrong input data. | ✓ A code or artifact refactor was intended to preserve predictions but may have changed them.
    leaderboard score n/a → 0.42580 (higher is better)
- expert 7018718 · google · v49→v50   After binning, check whether the result has more than one distinct value. If it has collapsed to a constant, fall back to the original continuous predictions for that column to preserve ranking information.
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The output file is missing, constant, stale or produced from the wrong input data.
    leaderboard score n/a → n/a (higher is better)
- expert 7548275 · google · v12→v13   Wrap each file read inside a try/except block so that missing or corrupt files are skipped. The ensemble then averages over whichever models did produce outputs, ensuring a submission is always generated even if some components fail.
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The selected checkpoint files are missing, ambiguous or different from the intended run. | ✓ The ensemble output cannot be reproduced from its intended component arrays and weights. | ✓ The output file is missing, constant, stale or produced from the wrong input data.
    leaderboard score n/a → n/a (higher is better)
- expert 7548275 · google · v11→v15   Never gate the final output/submission generation behind a debug flag. Keep debug gates only around expensive intermediate steps (training, heavy feature extraction). Ensure the output-writing code runs unconditionally so that a valid submission is always produced.
    evidence: ✓ The output file is missing, constant, stale or produced from the wrong input data. | ✗ Execution fails during import, file access or device initialization.
    leaderboard score n/a → 0.00596 (higher is better)
- expert 7548275 · google · v15→v18   Verify that model weights are actually loaded and predictions contain real signal by checking a few outputs manually. If in-notebook training is infeasible (time/memory), switch to loading precomputed predictions from external scripts or pre-uploaded artifacts. Add try/except fallback to known-good 
    evidence: ✓ The ensemble output cannot be reproduced from its intended component arrays and weights. | ✓ The output file is missing, constant, stale or produced from the wrong input data. | ✗ Execution fails during import, file access or device initialization. | ✓ The selected checkpoint files are missing, ambiguous or different from the intended run.
    leaderboard score 0.00596 → 0.30420 (higher is better; improved by 0.29825)
- expert 7548275 · google · v17→v18   For each model in the ensemble, wrap the file-loading step in a try/except. On failure, fall back to a pre-uploaded set of known-good predictions stored as a separate data asset. After merging all available predictions, fill any remaining NaNs and re-normalize before writing the submission. This gua
    evidence: ✓ The selected checkpoint files are missing, ambiguous or different from the intended run. | ✓ The ensemble output cannot be reproduced from its intended component arrays and weights. | ✓ The output file is missing, constant, stale or produced from the wrong input data.
    leaderboard score -0.00372 → 0.30420 (higher is better; improved by 0.30792)
- expert 7548275 · google · v20→v21   After fixing the upstream issue that originally required the fallback, disable or remove the fallback code path entirely. Verify with a submission that no residual contamination remains. Even small score improvements confirm the fallback was still active.
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The output file is missing, constant, stale or produced from the wrong input data.
    leaderboard score 0.39772 → 0.39778 (higher is better; improved by 0.00006)
- expert 6803050 · google · v1→v6   After the minimal pipeline produces a syntactically valid submission file, submit it immediately—even if predictions are not yet polished—to confirm the format is accepted and get a baseline score. Then iterate on post-processing. This avoids spending many versions on details that may not matter or 
    evidence: ✓ The output file is missing, constant, stale or produced from the wrong input data. | ✗ Execution fails during import, file access or device initialization. | ✓ Rows or feature columns can be reordered or mismatched across pipeline stages.
    leaderboard score n/a → n/a (higher is better)
- expert 6803050 · google · v10→v17   Before iterating on postprocessing or swapping checkpoints, verify that the model produces non-degenerate, varying outputs across test samples (e.g., print summary statistics, check variance per target). A constant or near-constant prediction vector will yield the same rank correlation no matter how
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The output file is missing, constant, stale or produced from the wrong input data. | ✓ The loaded checkpoint disagrees with the model architecture or vocabulary. | ✓ Inference encodings or missing-value treatment differ from those used in training.
    leaderboard score -0.00372 → -0.00372 (higher is better; unchanged by 0.00000)
- expert 6803050 · google · v17→v19   Before iterating on model improvements or post-processing, verify the data pipeline end-to-end: check that the correct test file is loaded, inputs are parsed properly, and predictions vary meaningfully across samples. A constant or garbage output that is invariant to model changes is a strong signal
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The output file is missing, constant, stale or produced from the wrong input data. | ✓ The loaded checkpoint disagrees with the model architecture or vocabulary.
    leaderboard score -0.00372 → -0.00372 (higher is better; unchanged by 0.00000)
- expert 6803050 · google · v19→v21   Suspect the submission is not actually reflecting model outputs on the correct data. Add assertions or guards on the test set size and inspect what data is being read. Verify the pipeline end-to-end: correct file is loaded, predictions flow through to the CSV, and the CSV is actually written. A froz
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The output file is missing, constant, stale or produced from the wrong input data.
    leaderboard score -0.00372 → 0.36763 (higher is better; improved by 0.37135)
- expert 6803050 · google · v19→v21   Insert a size assertion on the loaded test data that would fail if the training set were accidentally loaded (e.g., assert the row count is below the known training set size). Use this as a one-time diagnostic, then remove it once the correct file is confirmed.
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The output file is missing, constant, stale or produced from the wrong input data.
    leaderboard score -0.00372 → 0.36763 (higher is better; improved by 0.37135)
- expert 15173072 · ranzcr · v6→v7   Treat a score near random chance as evidence that model weights are not effectively loaded or applied. Check: (1) the model is set to evaluation mode, (2) the architecture definition matches the checkpoint's layer names, (3) input preprocessing (normalization mean/std, resolution) matches what was u
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The output file is missing, constant, stale or produced from the wrong input data.
    leaderboard score n/a → 0.50990 (higher is better)
- expert 15173072 · ranzcr · v7→v8   Check that (1) the model is set to evaluation mode so dropout and batch-norm behave correctly, and (2) the checkpoint file actually matches the model architecture being constructed. Fix both before investigating other issues.
    evidence: ✗ Execution fails during import, file access or device initialization. | ✓ The loaded checkpoint disagrees with the model architecture or vocabulary. | ✓ The selected checkpoint files are missing, ambiguous or different from the intended run. | ✓ The output file is missing, constant, stale or produced from the wrong input data.
    leaderboard score 0.50990 → 0.55637 (higher is better; improved by 0.04647)
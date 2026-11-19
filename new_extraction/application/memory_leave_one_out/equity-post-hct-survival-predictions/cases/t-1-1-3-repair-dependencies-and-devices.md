# Repair dependencies and devices  `T.1.1.3`   21 edits, 0 experts
4 scored cases (improvement signed by each competition's direction), median -0.00004, 1 improved


- expert 17616127 · commonlitreadabilityprize · v127→v130   First, try different directory paths in sys.path.append to match the actual uploaded dataset folder name. If the import still fails, check whether the specific symbol exists in that version's module hierarchy and fall back to importing the parent module or using a different access pattern (e.g., imp
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer. | ✗ The checkpoint reports missing keys or incompatible layer dimensions. | ✗ The model loads, but tokenization, normalization, feature order, or input shape differs from training. | ✗ A try/except fallback silently swallows model loading or inference failures, causing missing or zero predictions to be averaged into the ensemble.
    leaderboard score n/a → 0.45693 (lower is better)
- expert 18837555 · commonlitreadabilityprize · v8→v10   Before investigating model or data issues, check for trivial syntax or string-escaping errors introduced during editing. Fix them with minimal targeted edits and re-submit to confirm the substantive change works. Separate logic changes from cosmetic fixes to isolate which edit actually caused the im
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score n/a → 0.45825 (lower is better)
- expert 7018718 · google · v1→v2   Use copy commands instead of move commands when transferring files from platform-provided input directories into the writable workspace. Always verify that source paths are writable before using destructive file operations.
    evidence: ✗ The checkpoint reports missing keys or incompatible layer dimensions. | ✗ The model loads, but tokenization, normalization, feature order, or input shape differs from training. | ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score n/a → 0.36973 (higher is better)
- expert 7018718 · google · v5→v7   After changing the artifact reference, verify the actual directory name with a listing command before running the pipeline. Update all copy/mount paths to match the new artifact's actual location, not just the model-selection variable.
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer. | ✗ The checkpoint reports missing keys or incompatible layer dimensions. | ✗ The model loads, but tokenization, normalization, feature order, or input shape differs from training.
    leaderboard score n/a → n/a (higher is better)
- expert 7018718 · google · v16→v18   Keep cleanup commands commented out or gated behind a check until after inference completes. If a large score drop follows a housekeeping-only change, immediately suspect that required model files were removed. Revert the deletion and verify the score recovers before trying other changes.
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer. | ✓ A try/except fallback silently swallows model loading or inference failures, causing missing or zero predictions to be averaged into the ensemble.
    leaderboard score 0.38513 → 0.38508 (higher is better; worse by 0.00004)
- expert 6803050 · google · v37→v39   When a score drops unexpectedly after changing checkpoint paths, verify every path string character-by-character. Load one fold at a time and check that the model produces non-trivial outputs before running the full ensemble. Treat any sudden regression after a path change as a path bug until proven
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer. | ✗ The notebook lacks code to write predictions into the submission dataframe and save submission.csv.
    leaderboard score 0.29940 → 0.38287 (higher is better; improved by 0.08347)
- expert 53747598 · hms · v22→v23   Bundle the required package as a local wheel in the notebook's dataset/input directory and install it with pip at the start of the notebook, before any model code is imported.
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score 0.22817 → n/a (lower is better)
- expert 49576186 · hms · v8→v11   Fix one infrastructure issue per run, starting with the earliest failure in execution order (package installation syntax, then missing imports, then file paths). Keep each fix minimal so the next error is clearly attributable. Avoid bundling large feature changes with environment changes to reduce t
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score n/a → n/a (lower is better)
- expert 55621328 · learning · v2→v3   Explicitly move both the model (.to(device)) and every input tensor (.to(device)) to the target accelerator before the forward pass. Verify by checking that the submission file is non-empty and scores on the leaderboard.
    evidence: ✗ The checkpoint reports missing keys or incompatible layer dimensions. | ✗ The model loads, but tokenization, normalization, feature order, or input shape differs from training. | ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score n/a → 0.78177 (higher is better)
- expert 55621328 · learning · v96→v98   When a submission unexpectedly fails after changing inference settings, check that all CLI arguments (especially list-valued ones) conform to the expected delimiter and format before investigating deeper model issues.
    evidence: ✗ The checkpoint reports missing keys or incompatible layer dimensions. | ✗ The model loads, but tokenization, normalization, feature order, or input shape differs from training. | ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score 0.82129 → 0.82066 (higher is better; worse by 0.00063)
- expert 55621328 · learning · v126→v127   Explicitly move the model to the accelerator device at creation time and move each input batch to the same device before the forward pass. Treat device-placement verification as a mandatory checklist item before the first test submission of any new script.
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score n/a → 0.82594 (higher is better)
- expert 58527792 · learning · v1→v2   Identify and comment out or remove the failing import. Verify the rest of the pipeline does not depend on it. Run again to confirm the notebook completes and produces a valid submission.
    evidence: ✗ The checkpoint reports missing keys or incompatible layer dimensions. | ✗ The model loads, but tokenization, normalization, feature order, or input shape differs from training. | ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score n/a → 0.82214 (higher is better)
- expert 60197293 · learning · v14→v23   Load the raw data separately with the required library rather than converting mid-pipeline. Verify the external package is installed and importable before writing feature code. Consolidate all imports at the top of the script and test the feature-extraction cell in isolation before plugging results 
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer. | ✗ The checkpoint reports missing keys or incompatible layer dimensions. | ✗ The model loads, but tokenization, normalization, feature order, or input shape differs from training.
    leaderboard score n/a → n/a (higher is better)
- expert 60197293 · learning · v58→v62   Before committing a new I/O code path, verify all required imports are present, and double-check every file path string against the actual filesystem (watch for character mismatches like hyphens vs. underscores). If iterating anyway, make one minimal fix per run and re-execute to confirm each fix be
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score n/a → n/a (higher is better)
- expert 60197293 · learning · v94→v95   Verify that every file path points to the cloud input directory where the artifact is actually mounted. After fixing the path, compare the resulting score to the previous run: if performance drops, the newly loaded artifact may be stale or mismatched, and you should regenerate it or disable that ste
    evidence: ✗ The checkpoint reports missing keys or incompatible layer dimensions. | ✗ The model loads, but tokenization, normalization, feature order, or input shape differs from training. | ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score 0.81836 → 0.81593 (higher is better; worse by 0.00243)
- expert 55987255 · learning · v121→v123   After changing a data source, audit all file-path references and cached-artifact loads. Replace relative or variable-based paths with absolute paths valid in the execution environment, and remove or bypass cache-loading branches so features are recomputed from the new source, eliminating stale-cache
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer. | ✗ The checkpoint reports missing keys or incompatible layer dimensions. | ✗ Precomputed prediction files from external scripts are available and can bypass the broken in-notebook model pipeline.
    leaderboard score n/a → n/a (higher is better)
- expert 55591012 · learning · v13→v14   Keep device and algorithm-method parameters separate. Set the device to 'gpu' when a GPU is detected and to 'cpu' otherwise; set the algorithm parameter independently. Test the fallback path before submitting.
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score n/a → n/a (higher is better)
- expert 15082684 · ranzcr · v2→v3   After each round of code removal, search for all variable names that were defined in deleted blocks and verify they are not referenced elsewhere. Check that data-loading statements appear after all required definitions (transforms, configs). Run the notebook sequentially cell-by-cell to catch orderi
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score n/a → 0.96040 (higher is better)
- expert 15372370 · ranzcr · v2→v3   Replace dynamically constructed paths with the actual mount point of the uploaded artifacts in the inference environment. Add a print or bare-variable line to inspect resolved paths before the full run, confirming they exist before proceeding.
    evidence: ✗ The checkpoint reports missing keys or incompatible layer dimensions. | ✗ The model loads, but tokenization, normalization, feature order, or input shape differs from training. | ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score n/a → 0.96342 (higher is better)
- expert 15164527 · ranzcr · v38→v39   Explicitly remove conflicting directories from sys.path before appending the intended one, and place the import statement after the path manipulation. This ensures the correct version is loaded without ambiguity.
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer.
    leaderboard score n/a → 0.96055 (higher is better)
- expert 15173072 · ranzcr · v1→v7   Use map_location in the checkpoint loading call to handle device mismatches. For missing libraries, append a local copy of the library's repository to sys.path rather than relying on pip install, which may fail or install an incompatible version. Verify the pipeline end-to-end by checking that the o
    evidence: ✓ Execution stops at an import, file lookup, API call, or device transfer. | ✗ The notebook lacks code to write predictions into the submission dataframe and save submission.csv. | ✗ The checkpoint reports missing keys or incompatible layer dimensions.
    leaderboard score n/a → 0.50990 (higher is better)
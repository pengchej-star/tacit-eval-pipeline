# Repair API, dependency and device contracts  `T.1.1.4`   37 edits, 0 experts
2 scored cases, median improvement -0.00063, 0 improved


- expert 27502740 (Grandmaster) · amex · v3→v4   At the entry of any custom metric function, flatten the prediction array (e.g., ravel) so it is always 1-D, regardless of the shape the framework supplies. This prevents shape-mismatch errors in downstream sorting and arithmetic.
    evidence: ✗ Predictions or new features no longer match the original sample identifiers or column order. | ✗ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ Individual models produce varying outputs but the saved submission is constant, partial or duplicates a member. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score n/a → n/a
- expert 27502740 (Grandmaster) · amex · v7→v8   At the top of any custom metric function, unconditionally flatten or squeeze the prediction array to 1-D (e.g., ravel). This defensive step costs nothing and prevents recurring shape-mismatch bugs whenever the metric is reused with a different model or framework.
    evidence: ✗ Predictions or new features no longer match the original sample identifiers or column order. | ✗ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ Individual models produce varying outputs but the saved submission is constant, partial or duplicates a member. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.79461
- expert 27799930 (Contributor) · amex · v7→v13   Before committing a training run: (1) validate the parameter dictionary parses correctly in an isolated cell, (2) consult the library's API docs for the exact keyword names (e.g., the scikit-learn-style wrapper may use different argument names than the native API), and (3) do a fast smoke-test with 
    evidence: ✗ Predictions or new features no longer match the original sample identifiers or column order. | ✗ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ Individual models produce varying outputs but the saved submission is constant, partial or duplicates a member. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 27825577 (Expert) · amex · v21→v25   Make exactly one change per run: first fix naming/typos, then fix which helper is called, then fix the return format. Inspect the printed metric name and value after each change. Do not combine multiple fixes in one iteration, because compounding changes obscures which fix resolved which issue.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✗ Predictions or new features no longer match the original sample identifiers or column order.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v12→v15   Check which API was used to train the model. The low-level API's model object typically has only a generic `.predict()` method that returns probabilities when the objective is a classification loss. The scikit-learn wrapper adds `.predict_proba()`. Mixing them causes attribute errors. Match the pred
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v32→v34   Convert to the CPU dataframe library before the groupby, use the transform method to get row-aligned group statistics for fillna, then convert back to the GPU library. This isolates the unsupported operation while keeping GPU acceleration elsewhere.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v31→v32   Replace all inplace mutation calls with explicit reassignment (variable = variable.operation(...)). This is safe across libraries and avoids relying on library-specific inplace behavior.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 27656049 (Expert) · amex · v21→v22   Verify the type of the target object before computing class ratios. If it is already a one-dimensional structure, call value-counting methods directly on it rather than indexing by a column name. This avoids a common bug when refactoring from dataframe-based to series-based target handling.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 77347591 (Expert) · equity · v7→v8   Default new model components to CPU execution first to confirm correctness, then switch to GPU only after verifying the environment supports it. When a submission fails after adding a GPU-configured model, the first fix to try is switching that model to CPU.
    evidence: ✗ Predictions or new features no longer match the original sample identifiers or column order. | ✗ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.69407
- expert 77276039 (Expert) · equity · v1→v5   Systematically disable GPU flags for every model family: comment out or remove device/task-type GPU parameters in tree models, remove explicit tensor .cuda() calls, and switch the deep-learning trainer's accelerator to CPU. Re-run the full notebook to confirm no remaining GPU references cause errors
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.69330 → n/a
- expert 77276039 (Expert) · equity · v19→v20   Separate infrastructure fixes (device compatibility) into their own commit/version and verify the pipeline still reproduces the previous score before layering on functional changes. This ensures any subsequent score change is attributable to the new modeling choices, not to subtle side effects of th
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 7018718 (Expert) · google · v1→v2   Use copy commands instead of move commands when transferring files from platform-provided input directories into the writable workspace. Always verify that source paths are writable before using destructive file operations.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.36973
- expert 7018718 (Expert) · google · v5→v7   After changing the artifact reference, verify the actual directory name with a listing command before running the pipeline. Update all copy/mount paths to match the new artifact's actual location, not just the model-selection variable.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score n/a → n/a
- expert 7548275 (Expert) · google · v8→v11   Import the notebook-specific progress bar class from the library's internal notebook submodule, alias it as the standard name, then call the registration function (e.g., `.pandas()`) so that dataframe apply methods display progress. Test the import path in the target environment, as the public API p
    evidence: ✗ Predictions or new features no longer match the original sample identifiers or column order. | ✗ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ Individual models produce varying outputs but the saved submission is constant, partial or duplicates a member. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score n/a → n/a
- expert 53747598 (Master) · hms · v22→v23   Bundle the required package as a local wheel in the notebook's dataset/input directory and install it with pip at the start of the notebook, before any model code is imported.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.22817 → n/a
- expert 49576186 (Expert) · hms · v140→v149   When porting a CPU signal-processing step to a GPU library, have the CPU fallback ready and test the GPU path in isolation first. If the GPU call requires more than one fix iteration, fall back to the CPU version immediately to avoid wasting submission attempts on infrastructure bugs rather than mod
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.38984 → n/a
- expert 55621328 (Master) · learning · v2→v3   Explicitly move both the model (.to(device)) and every input tensor (.to(device)) to the target accelerator before the forward pass. Verify by checking that the submission file is non-empty and scores on the leaderboard.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.78177
- expert 55621328 (Master) · learning · v96→v98   When a submission unexpectedly fails after changing inference settings, check that all CLI arguments (especially list-valued ones) conform to the expected delimiter and format before investigating deeper model issues.
    evidence: ✗ Predictions or new features no longer match the original sample identifiers or column order. | ✗ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.82129 → 0.82066 (-0.00063)
- expert 55621328 (Master) · learning · v126→v127   Explicitly move the model to the accelerator device at creation time and move each input batch to the same device before the forward pass. Treat device-placement verification as a mandatory checklist item before the first test submission of any new script.
    evidence: ✗ Predictions or new features no longer match the original sample identifiers or column order. | ✗ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ Individual models produce varying outputs but the saved submission is constant, partial or duplicates a member. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.82594
- expert 58130512 (Master) · learning · v30→v32   After any data manipulation step that combines frames, add an immediate assertion or display of shape and dtypes to catch library mismatches before submitting. Standardize on one library per pipeline section, or wrap concat/merge in a helper that checks the input type.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.82190
- expert 58527792 (Contributor) · learning · v1→v2   Identify and comment out or remove the failing import. Verify the rest of the pipeline does not depend on it. Run again to confirm the notebook completes and produces a valid submission.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.82214
- expert 60197293 (Expert) · learning · v7→v8   Write one metric function that inspects the type of its input (e.g., the dataset object) to detect which library is calling it, then branches to extract labels and return the result tuple in the format that library expects. Verify by running training with early stopping for both models.
    evidence: ✗ Predictions or new features no longer match the original sample identifiers or column order. | ✗ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.81867
- expert 60197293 (Expert) · learning · v14→v23   Load the raw data separately with the required library rather than converting mid-pipeline. Verify the external package is installed and importable before writing feature code. Consolidate all imports at the top of the script and test the feature-extraction cell in isolation before plugging results 
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file. | ✗ Predictions or new features no longer match the original sample identifiers or column order. | ✗ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ Individual models produce varying outputs but the saved submission is constant, partial or duplicates a member.
    leaderboard score n/a → n/a
- expert 60197293 (Expert) · learning · v58→v62   Before committing a new I/O code path, verify all required imports are present, and double-check every file path string against the actual filesystem (watch for character mismatches like hyphens vs. underscores). If iterating anyway, make one minimal fix per run and re-execute to confirm each fix be
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 60197293 (Expert) · learning · v94→v95   Verify that every file path points to the cloud input directory where the artifact is actually mounted. After fixing the path, compare the resulting score to the previous run: if performance drops, the newly loaded artifact may be stale or mismatched, and you should regenerate it or disable that ste
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.81836 → 0.81593 (-0.00243)
- expert 55987255 (Master) · learning · v6→v8   After computing embeddings, explicitly delete the neural model objects, run garbage collection, and force the tree-training framework into CPU-only mode. Verify with a no-change re-run that the pipeline completes before adding further code.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file. | ✗ Predictions or new features no longer match the original sample identifiers or column order.
    leaderboard score n/a → n/a
- expert 55987255 (Master) · learning · v11→v12   Revert the infrastructure change (device setting) first while keeping the feature change, then submit. This isolates whether the failure was due to the device or the feature change. Avoid bundling feature engineering changes with infrastructure changes in a single iteration.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.81757
- expert 55987255 (Master) · learning · v59→v69   Test the new function in isolation on a small data sample before integrating. Verify all imports, confirm input/output types match the pipeline's DataFrame library, and check that intermediate variables are not deleted before downstream steps use them. Expect roughly as many debug iterations as ther
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 55987255 (Master) · learning · v81→v87   Before starting, write a minimal standalone cell that installs the package, imports it, and runs a trivial encode/predict call. Resolve all dependency and variable-name issues in that isolated cell first. Only then wire the output into the main pipeline. This avoids spending many full-notebook rerun
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file. | ✓ Predictions or new features no longer match the original sample identifiers or column order.
    leaderboard score n/a → n/a
- expert 55987255 (Master) · learning · v103→v119   Before changing the CV splitter, enumerate all required inputs (feature matrix without target/group columns, integer target array for stratification, aligned group array) and prepare them in a single refactor. Verify each with shape/dtype assertions before the split call. After switching, compare fo
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file. | ✗ Predictions or new features no longer match the original sample identifiers or column order. | ✗ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ Individual models produce varying outputs but the saved submission is constant, partial or duplicates a member.
    leaderboard score n/a → 0.80993
- expert 55987255 (Master) · learning · v117→v118   Before calling a stratified splitter, cast the target to integer (or bin it into a small number of discrete classes). For ordinal targets stored as floats, round or truncate to int. Verify the number of unique values in the cast target is small and matches the expected number of classes.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 55987255 (Master) · learning · v121→v123   After changing a data source, audit all file-path references and cached-artifact loads. Replace relative or variable-based paths with absolute paths valid in the execution environment, and remove or bypass cache-loading branches so features are recomputed from the new source, eliminating stale-cache
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 55591012 (Grandmaster) · learning · v13→v14   Keep device and algorithm-method parameters separate. Set the device to 'gpu' when a GPU is detected and to 'cpu' otherwise; set the algorithm parameter independently. Test the fallback path before submitting.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 55591012 (Grandmaster) · learning · v49→v50   Always include the file-write step that saves predictions in the required format before submitting. When a run unexpectedly produces no score, check that the output file is actually written with the correct name, columns, and path.
    evidence: ✗ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.82075
- expert 15372370 (Expert) · ranzcr · v2→v3   Replace dynamically constructed paths with the actual mount point of the uploaded artifacts in the inference environment. Add a print or bare-variable line to inspect resolved paths before the full run, confirming they exist before proceeding.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.96342
- expert 15164527 (Expert) · ranzcr · v38→v39   Explicitly remove conflicting directories from sys.path before appending the intended one, and place the import statement after the path manipulation. This ensures the correct version is loaded without ambiguity.
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.96055
- expert 15173072 (Contributor) · ranzcr · v1→v7   Use map_location in the checkpoint loading call to handle device mismatches. For missing libraries, append a local copy of the library's repository to sys.path rather than relying on pip install, which may fail or install an incompatible version. Verify the pipeline end-to-end by checking that the o
    evidence: ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file. | ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration.
    leaderboard score n/a → 0.50990
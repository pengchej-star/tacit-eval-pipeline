# Fix API and runtime errors  `T.1.2.1`   21 edits, 0 experts
1 scored cases, median improvement -0.00063, 0 improved


- expert 27836972 (Expert) · amex · v2→v4   Temporarily inline the function body into separate notebook cells, inserting inspection points (display shape, column names, value distributions) after each transformation step. Once the logic is verified correct, re-encapsulate it into a reusable function.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception.
    leaderboard score n/a → n/a
- expert 27825577 (Expert) · amex · v21→v25   Make exactly one change per run: first fix naming/typos, then fix which helper is called, then fix the return format. Inspect the printed metric name and value after each change. Do not combine multiple fixes in one iteration, because compounding changes obscures which fix resolved which issue.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✗ Required files or packages are absent or incompatible in the submission environment.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v32→v34   Convert to the CPU dataframe library before the groupby, use the transform method to get row-aligned group statistics for fillna, then convert back to the GPU library. This isolates the unsupported operation while keeping GPU acceleration elsewhere.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception.
    leaderboard score n/a → n/a
- expert 28093671 (Contributor) · amex · v31→v32   Replace all inplace mutation calls with explicit reassignment (variable = variable.operation(...)). This is safe across libraries and avoids relying on library-specific inplace behavior.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception.
    leaderboard score n/a → n/a
- expert 27656049 (Expert) · amex · v21→v22   Verify the type of the target object before computing class ratios. If it is already a one-dimensional structure, call value-counting methods directly on it rather than indexing by a column name. This avoids a common bug when refactoring from dataframe-based to series-based target handling.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✗ Required files or packages are absent or incompatible in the submission environment.
    leaderboard score n/a → n/a
- expert 18837555 (Expert) · commonlitreadabilityprize · v8→v10   Before investigating model or data issues, check for trivial syntax or string-escaping errors introduced during editing. Fix them with minimal targeted edits and re-submit to confirm the substantive change works. Separate logic changes from cosmetic fixes to isolate which edit actually caused the im
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception.
    leaderboard score n/a → 0.45825
- expert 77129691 (Master) · equity · v11→v12   After adding a new model component, verify that every data-dependent preprocessing step (bin computation, normalization, encoding) references the correct split variable. Check variable names at the boundary between the data pipeline and the new model before running the full training loop.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception.
    leaderboard score n/a → 0.69423
- expert 77129691 (Master) · equity · v15→v16   After label encoding, always filter using the encoded integer codes rather than the original string labels. Verify the filter by checking that the number of matched rows per group equals the expected counts before proceeding.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✗ Required files or packages are absent or incompatible in the submission environment.
    leaderboard score n/a → 0.69457
- expert 7670859 (Contributor) · google · v1→v8   Fix one category of bug per iteration in dependency order: runtime/syntax errors first, then data loading and alignment, then model architecture mismatches (output shape must match saved weights), then graph construction. Submit as soon as the pipeline runs end-to-end to establish a baseline score, 
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✓ The notebook completes but its output is missing, stale, or based on placeholder inputs.
    leaderboard score n/a → n/a
- expert 7573212 (Contributor) · google · v1→v3   Before debugging model logic, trace every variable from its definition to every usage site, checking for name mismatches. Also verify that framework utility calls (session resets, garbage collection) have correct syntax. Fix these first, confirm the pipeline runs end-to-end, then iterate on modeling
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✓ The blended output disagrees with a direct recomputation from saved member arrays. | ✗ Required files or packages are absent or incompatible in the submission environment.
    leaderboard score n/a → 0.38325
- expert 7253130 (Contributor) · google · v2→v3   After any change to string-based configuration parameters, immediately verify the exact spelling. Run a minimal forward pass or check the model summary to confirm the intended activation/layer is actually applied before proceeding to tune other hyperparameters.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✗ Required files or packages are absent or incompatible in the submission environment.
    leaderboard score n/a → n/a
- expert 52200959 (Master) · hms · v6→v7   Remove default values for arguments that reference outer-scope mutable objects (dictionaries, dataframes). Make them required positional parameters so that callers must pass them explicitly, surfacing any naming mismatches as immediate errors rather than silent wrong-data bugs.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception.
    leaderboard score n/a → n/a
- expert 55621328 (Master) · learning · v9→v10   Check the shape and type of the threshold array passed to the rounding function. A common bug is passing a 2D array where a 1D array is expected (or vice versa), which can silently produce wrong bin assignments. Verify with a small example that the rounding output matches expectations before submitt
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✗ Required files or packages are absent or incompatible in the submission environment. | ✗ The traceback identifies incompatible devices or unsupported accelerator settings.
    leaderboard score n/a → 0.80442
- expert 55621328 (Master) · learning · v96→v98   When a submission unexpectedly fails after changing inference settings, check that all CLI arguments (especially list-valued ones) conform to the expected delimiter and format before investigating deeper model issues.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✗ Required files or packages are absent or incompatible in the submission environment. | ✓ The notebook completes but its output is missing, stale, or based on placeholder inputs.
    leaderboard score 0.82129 → 0.82066 (-0.00063)
- expert 59253662 (Contributor) · learning · v2→v7   Fix one bug per commit and re-run after each fix to isolate errors. Prioritize: (1) variable name collisions between pipeline stages, (2) wrong dataframe/array references in train vs. predict calls, (3) type conversion issues at boundaries between libraries, (4) file path portability. Only move to t
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✓ Required files or packages are absent or incompatible in the submission environment. | ✓ The notebook completes but its output is missing, stale, or based on placeholder inputs. | ✗ The traceback identifies incompatible devices or unsupported accelerator settings.
    leaderboard score n/a → n/a
- expert 58130512 (Master) · learning · v30→v32   After any data manipulation step that combines frames, add an immediate assertion or display of shape and dtypes to catch library mismatches before submitting. Standardize on one library per pipeline section, or wrap concat/merge in a helper that checks the input type.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception.
    leaderboard score n/a → 0.82190
- expert 58527792 (Contributor) · learning · v1→v2   Identify and comment out or remove the failing import. Verify the rest of the pipeline does not depend on it. Run again to confirm the notebook completes and produces a valid submission.
    evidence: ✗ A small-batch run raises an API, shape, or variable-reference exception. | ✓ Required files or packages are absent or incompatible in the submission environment.
    leaderboard score n/a → 0.82214
- expert 55987255 (Master) · learning · v46→v47   After changing the number of output components in any feature-generation step, search the entire codebase for every hard-coded reference to the old component count—especially column name lists, loop ranges, and array slices—and update them all to match the new value. Ideally, derive the count from t
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception.
    leaderboard score n/a → 0.81750
- expert 55987255 (Master) · learning · v103→v119   Before changing the CV splitter, enumerate all required inputs (feature matrix without target/group columns, integer target array for stratification, aligned group array) and prepare them in a single refactor. Verify each with shape/dtype assertions before the split call. After switching, compare fo
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✗ Required files or packages are absent or incompatible in the submission environment. | ✗ The traceback identifies incompatible devices or unsupported accelerator settings. | ✗ The blended output disagrees with a direct recomputation from saved member arrays.
    leaderboard score n/a → 0.80993
- expert 55987255 (Master) · learning · v117→v118   Before calling a stratified splitter, cast the target to integer (or bin it into a small number of discrete classes). For ordinal targets stored as floats, round or truncate to int. Verify the number of unique values in the cast target is small and matches the expected number of classes.
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✗ Required files or packages are absent or incompatible in the submission environment.
    leaderboard score n/a → n/a
- expert 50496431 (Grandmaster) · hms · v1→v5   Systematically address three categories: (1) ensure the dataset class returns only inputs (not labels) during inference, matching what the inference loop expects; (2) consolidate imports into one clean block, removing duplicates and unused libraries that may cause import errors in the inference envi
    evidence: ✓ A small-batch run raises an API, shape, or variable-reference exception. | ✓ Required files or packages are absent or incompatible in the submission environment. | ✓ The notebook completes but its output is missing, stale, or based on placeholder inputs.
    leaderboard score n/a → 0.42903
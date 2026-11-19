# Correct feature and tensor computation  `T.1.2.3`   24 edits, 0 experts
12 scored cases (improvement signed by each competition's direction), median +0.00603, 6 improved


- expert 27836972 · amex · v52→v53   Build derived column names programmatically by concatenating the base name with the required suffix in a loop or helper function, rather than listing full names manually. Add an assertion or existence check before computing the derived feature so missing columns surface immediately.
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score n/a → n/a (higher is better)
- expert 28093671 · amex · v31→v32   Replace all inplace mutation calls with explicit reassignment (variable = variable.operation(...)). This is safe across libraries and avoids relying on library-specific inplace behavior.
    evidence: ✓ A framework or library API behaves differently from the expected pandas/numpy semantics (e.g., inplace, indexing), causing silent data corruption.
    leaderboard score n/a → n/a (higher is better)
- expert 27656049 · amex · v21→v22   Verify the type of the target object before computing class ratios. If it is already a one-dimensional structure, call value-counting methods directly on it rather than indexing by a column name. This avoids a common bug when refactoring from dataframe-based to series-based target handling.
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score n/a → n/a (higher is better)
- expert 17616127 · commonlitreadabilityprize · v137→v139   After changing any keyword argument in a function call, verify the exact parameter name in the function definition. Add a sanity-check print or assertion on the function's return shape/value before using it downstream. A large unexpected score drop after a 'minor' change is a strong signal of such a
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass. | ✓ Some enabled models are skipped, repeated, or assigned the wrong fold or weight.
    leaderboard score 0.44975 → 0.46975 (lower is better; worse by 0.02000)
- expert 18757376 · commonlitreadabilityprize · v8→v9   Before attributing a score regression to model changes, verify that each stage receives the correct input by inspecting variable names and shapes at every handoff point. Fix any mismatch before evaluating whether the model changes themselves helped or hurt. A single wrong-variable bug can mask or ne
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass. | ✓ A feature used during training is conditionally excluded or missing at test time due to a flag or path difference.
    leaderboard score n/a → 0.46321 (lower is better)
- expert 17371717 · commonlitreadabilityprize · v1→v2   Replace manual preprocessing with the library's native parameter. Submit or validate to confirm the output is equivalent or better, establishing a clean baseline before making architectural changes.
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score 0.47570 → 0.47570 (lower is better; unchanged by 0.00000)
- expert 7823861 · google · v8→v10   Fit the encoder on training data only. At test time, call transform (not fit_transform) on the test data. Ensure the output array has exactly as many rows as the test set. Set the encoder to handle unknown categories gracefully (e.g., ignore or map to a default) so unseen test categories do not caus
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass. | ✓ The encoder or transformer fitted on training data encounters unseen categories at test time, causing errors or silent misencoding. | ✓ The loaded dataframe is actually the training set (or wrong split) instead of the intended test set, detectable by row count.
    leaderboard score n/a → 0.41495 (higher is better)
- expert 7823861 · google · v10→v15   Use two layers of defense: configure the encoder to ignore unknown categories (producing a zero-vector), and also remap unknown values to the most frequent or most representative training category before encoding. This avoids both crashes and degenerate feature vectors.
    evidence: ✓ The encoder or transformer fitted on training data encounters unseen categories at test time, causing errors or silent misencoding. | ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score 0.41495 → 0.42097 (higher is better; improved by 0.00603)
- expert 6803050 · google · v19→v21   Insert a size assertion on the loaded test data that would fail if the training set were accidentally loaded (e.g., assert the row count is below the known training set size). Use this as a one-time diagnostic, then remove it once the correct file is confirmed.
    evidence: ✓ The loaded dataframe is actually the training set (or wrong split) instead of the intended test set, detectable by row count.
    leaderboard score -0.00372 → 0.36763 (higher is better; improved by 0.37135)
- expert 7253130 · google · v2→v3   After any change to string-based configuration parameters, immediately verify the exact spelling. Run a minimal forward pass or check the model summary to confirm the intended activation/layer is actually applied before proceeding to tune other hyperparameters.
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score n/a → n/a (higher is better)
- expert 49524919 · hms · v29→v34   When introducing a new preprocessing branch, audit every function call and variable reference in the inference loop to ensure it uses the new branch's transforms, normalization, and imputation—not the old ones. Specifically check: (1) the correct transform/augmentation object is called, (2) missing-
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass. | ✓ Duplicate or conflicting code paths load or construct the same data, causing ambiguity about which version is actually used.
    leaderboard score n/a → 0.55426 (lower is better)
- expert 49524919 · hms · v47→v49   After a regression from a combined architecture+checkpoint change, inspect the forward pass carefully for correctness bugs before concluding the architecture or checkpoints are worse. Fix any bugs first, then re-evaluate. Only after confirming correctness should you continue sweeping checkpoints or 
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score 0.41674 → 0.41042 (lower is better; improved by 0.00633)
- expert 49524919 · hms · v90→v92   Focus first on the data preprocessing and augmentation code rather than the model definitions. Check that transform function signatures, tensor shapes, and scaling conventions match what the pretrained models expect. Fix those issues in a minimal follow-up commit and verify recovery before iterating
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score 0.26809 → 0.36298 (lower is better; worse by 0.09489)
- expert 49524919 · hms · v142→v148   First fix obvious data-flow bugs (e.g., wrong input variable fed to feature extraction). Then submit to confirm partial recovery. If the new component still underperforms, remove it and its associated transforms/models entirely rather than continuing to tune it. The cleanup itself can yield a new be
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass. | ✓ Some enabled models are skipped, repeated, or assigned the wrong fold or weight.
    leaderboard score 0.26137 → 0.23482 (lower is better; improved by 0.02655)
- expert 49524919 · hms · v142→v146   Check that the correct intermediate data is being fed into the new feature extraction (e.g., preprocessed vs. raw signals). A single variable name error at the input of the pipeline is the most common cause of catastrophic regression. Fix the input wiring first before evaluating whether the new feat
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass. | ✓ Duplicate or conflicting code paths load or construct the same data, causing ambiguity about which version is actually used.
    leaderboard score 0.26137 → 0.27167 (lower is better; worse by 0.01030)
- expert 49576186 · hms · v4→v6   Audit each preprocessing step for correctness: verify filter design handles edge cases (e.g., different filter types requiring different parameter shapes), relax aggressive clipping thresholds that discard useful dynamic range, and fix spatial alignment (crop/resize/center) of inputs. These bug fixe
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass. | ✓ A framework or library API behaves differently from the expected pandas/numpy semantics (e.g., inplace, indexing), causing silent data corruption.
    leaderboard score 0.40619 → 0.37463 (lower is better; improved by 0.03155)
- expert 49576186 · hms · v48→v49   Before continuing to iterate on features or architecture, audit the tensor shapes and concatenation operations in the model graph for silent shape mismatches. Fix any axis or dimension bugs first, add diagnostic plots (e.g., training loss curves), and re-evaluate. A single shape bug can nullify many
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score 0.38574 → 0.35728 (lower is better; improved by 0.02845)
- expert 52200959 · hms · v6→v7   Remove default values for arguments that reference outer-scope mutable objects (dictionaries, dataframes). Make them required positional parameters so that callers must pass them explicitly, surfacing any naming mismatches as immediate errors rather than silent wrong-data bugs.
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score n/a → n/a (lower is better)
- expert 55621328 · learning · v9→v10   Check the shape and type of the threshold array passed to the rounding function. A common bug is passing a 2D array where a 1D array is expected (or vice versa), which can silently produce wrong bin assignments. Verify with a small example that the rounding output matches expectations before submitt
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score n/a → 0.80442 (higher is better)
- expert 55621328 · learning · v76→v78   After any reordering of the inference dataset, explicitly track the mapping between the new order and the original sample identifiers. Merge predictions back to identifiers using this mapping before writing the submission. Verify by checking that a known sample's prediction is plausible.
    evidence: ✓ Joined features or prediction files have different identifier order or coverage. | ✓ Duplicate or conflicting code paths load or construct the same data, causing ambiguity about which version is actually used.
    leaderboard score 0.82461 → 0.82461 (higher is better; unchanged by 0.00000)
- expert 55431616 · learning · v16→v17   Ensure every aggregation alias is unique by systematically naming them after the statistic and parameter (e.g., 'q50' for the 50th percentile). After adding or changing bucket boundaries, verify the resulting DataFrame columns and spot-check a few rows to confirm no columns were silently dropped or 
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score n/a → n/a (higher is better)
- expert 58130512 · learning · v23→v24   When fixing a suspected bug in data selection or CV logic, isolate the fix from all other changes and compare local validation before and after. A pipeline tuned around a bug may perform worse once the bug is corrected, because other components compensated for it. If the fix hurts, re-tune downstrea
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score 0.81980 → 0.81752 (higher is better; worse by 0.00229)
- expert 58130512 · learning · v30→v32   After any data manipulation step that combines frames, add an immediate assertion or display of shape and dtypes to catch library mismatches before submitting. Standardize on one library per pipeline section, or wrap concat/merge in a helper that checks the input type.
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass. | ✓ A framework or library API behaves differently from the expected pandas/numpy semantics (e.g., inplace, indexing), causing silent data corruption.
    leaderboard score n/a → 0.82190 (higher is better)
- expert 55987255 · learning · v46→v47   After changing the number of output components in any feature-generation step, search the entire codebase for every hard-coded reference to the old component count—especially column name lists, loop ranges, and array slices—and update them all to match the new value. Ideally, derive the count from t
    evidence: ✓ The first divergent value appears inside feature construction or the model forward pass.
    leaderboard score n/a → 0.81750 (higher is better)
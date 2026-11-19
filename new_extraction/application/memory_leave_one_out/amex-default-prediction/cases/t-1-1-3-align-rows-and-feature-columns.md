# Align rows and feature columns  `T.1.1.3`   12 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00000, 1 improved


- expert 18851026 · commonlitreadabilityprize · v13→v15   Before submitting, verify that (1) all prediction dataframes have identical row counts and matching IDs by doing an explicit join/check, and (2) the blending formula references each model's predictions exactly once with correct variable names. Inspect the final blended array shape and a few sample v
    evidence: ✓ Sample keys or ordered feature names disagree across arrays being combined. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.46134 (lower is better)
- expert 75924487 · equity · v11→v13   When updating artifact paths, verify that column names, fold indices, and row counts of the new OOF files match what the ensembler expects. Remove or rename stale path variables immediately. Submit only after a local validation check confirms the new artifacts reproduce or improve the previous CV sc
    evidence: ✓ Sample keys or ordered feature names disagree across arrays being combined. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → n/a (higher is better)
- expert 7670859 · google · v34→v35   Never reorder training or test rows without ensuring that the final predictions are mapped back to the original row IDs before writing the submission file. When a score drops catastrophically (e.g., near zero or negative on a correlation metric), check ID alignment before investigating model quality
    evidence: ✓ Sample keys or ordered feature names disagree across arrays being combined. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.37520 → -0.01424 (higher is better; worse by 0.38945)
- expert 53747598 · hms · v2→v7   Build incrementally: first get one model producing a valid submission, then add models one at a time. Sort all intermediate prediction files by the same unique sample key before blending. Use explicit named weights for each component. Store each model's raw predictions in separate files so component
    evidence: ✓ Sample keys or ordered feature names disagree across arrays being combined. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → n/a (lower is better)
- expert 55621328 · learning · v76→v78   After any reordering of the inference dataset, explicitly track the mapping between the new order and the original sample identifiers. Merge predictions back to identifiers using this mapping before writing the submission. Verify by checking that a known sample's prediction is plausible.
    evidence: ✓ Sample keys or ordered feature names disagree across arrays being combined. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.82461 → 0.82461 (higher is better; unchanged by 0.00000)
- expert 55431616 · learning · v17→v20   Write each model's output to a distinctly named file in the working directory using relative paths. Read both files, merge on the sample identifier, compute a weighted average giving dominant weight to the stronger model, then round/discretize for the required output format. Test the pipeline end-to
    evidence: ✓ Sample keys or ordered feature names disagree across arrays being combined. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → n/a (higher is better)
- expert 58130512 · learning · v59→v62   Always pass exactly the same feature list (same names, same order) at prediction time as was used during training. Store the feature list alongside the model (e.g., from the model's own attribute or a saved artifact) and index the test data with it explicitly. When debugging, verify alignment by com
    evidence: ✓ Sample keys or ordered feature names disagree across arrays being combined. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.82136 (higher is better)
- expert 58130512 · learning · v84→v86   Before concatenation, map the selected feature names to their column indices in the precomputed array and slice columns accordingly. Convert all arrays to a consistent numeric type. Print shapes after slicing to verify alignment. Iterate until shapes match and training runs without error.
    evidence: ✗ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ Sample keys or ordered feature names disagree across arrays being combined. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.82322 (higher is better)
- expert 60197293 · learning · v72→v74   After any column rename or addition, assert that every name in the saved feature-selection list exists in the current DataFrame columns before training or predicting. Print the intersection size and any missing names. Never submit without this check passing. Regenerate the feature-selection list whe
    evidence: ✓ Sample keys or ordered feature names disagree across arrays being combined. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.57175 (higher is better)
- expert 60197293 · learning · v62→v71   Keep all feature sources as DataFrames with a shared index until the final step. Reset indices to ensure alignment, drop any ID/key columns from external predictions before concatenation, use column-aware concat, then assert the expected number of columns and no NaN values. Convert to a numeric arra
    evidence: ✓ Sample keys or ordered feature names disagree across arrays being combined. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✗ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ The same raw example produces different training and inference features.
    leaderboard score n/a → n/a (higher is better)
- expert 60197293 · learning · v74→v80   Always merge auxiliary/external prediction features using an explicit key-based join (on the sample identifier column) rather than positional concatenation. When a catastrophic regression occurs after adding features, first disable the new features to confirm the base pipeline is intact, then re-ena
    evidence: ✓ Sample keys or ordered feature names disagree across arrays being combined. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✗ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score 0.57175 → 0.81692 (higher is better; improved by 0.24517)
- expert 55591012 · learning · v26→v27   Before submitting a blended file, verify that (1) row IDs are aligned between the two files, (2) prediction scales and distributions are compatible, and (3) the blend improves on a local validation set. A catastrophic score drop signals a merge or alignment bug. Always validate locally before submit
    evidence: ✓ Sample keys or ordered feature names disagree across arrays being combined.
    leaderboard score n/a → 0.55086 (higher is better)
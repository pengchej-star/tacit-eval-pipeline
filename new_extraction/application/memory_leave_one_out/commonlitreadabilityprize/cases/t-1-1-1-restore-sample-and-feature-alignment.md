# Restore sample and feature alignment  `T.1.1.1`   9 edits, 0 experts
3 scored cases, median improvement +0.00009, 2 improved


- expert 27836972 (Expert) · amex · v52→v53   Build derived column names programmatically by concatenating the base name with the required suffix in a loop or helper function, rather than listing full names manually. Add an assertion or existence check before computing the derived feature so missing columns surface immediately.
    evidence: ✓ Predictions or new features no longer match the original sample identifiers or column order.
    leaderboard score n/a → n/a
- expert 73937748 (Master) · equity · v13→v15   Before fitting any auxiliary model used to create target labels, explicitly drop identifier and index columns. After writing the fix, verify it is effective by checking that the variable actually used downstream is the cleaned one, not the original dataframe. A quick sanity check: print the column l
    evidence: ✓ Predictions or new features no longer match the original sample identifiers or column order. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.68805 → 0.68814 (+0.00009)
- expert 55621328 (Master) · learning · v76→v78   After any reordering of the inference dataset, explicitly track the mapping between the new order and the original sample identifiers. Merge predictions back to identifiers using this mapping before writing the submission. Verify by checking that a known sample's prediction is plausible.
    evidence: ✓ Predictions or new features no longer match the original sample identifiers or column order. | ✗ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.82461 → 0.82461 (+0.00000)
- expert 58130512 (Master) · learning · v59→v62   Always pass exactly the same feature list (same names, same order) at prediction time as was used during training. Store the feature list alongside the model (e.g., from the model's own attribute or a saved artifact) and index the test data with it explicitly. When debugging, verify alignment by com
    evidence: ✓ Predictions or new features no longer match the original sample identifiers or column order. | ✗ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.82136
- expert 60197293 (Expert) · learning · v72→v74   After any column rename or addition, assert that every name in the saved feature-selection list exists in the current DataFrame columns before training or predicting. Print the intersection size and any missing names. Never submit without this check passing. Regenerate the feature-selection list whe
    evidence: ✓ Predictions or new features no longer match the original sample identifiers or column order.
    leaderboard score n/a → 0.57175
- expert 60197293 (Expert) · learning · v62→v71   Keep all feature sources as DataFrames with a shared index until the final step. Reset indices to ensure alignment, drop any ID/key columns from external predictions before concatenation, use column-aware concat, then assert the expected number of columns and no NaN values. Convert to a numeric arra
    evidence: ✓ Predictions or new features no longer match the original sample identifiers or column order. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a
- expert 60197293 (Expert) · learning · v74→v80   Always merge auxiliary/external prediction features using an explicit key-based join (on the sample identifier column) rather than positional concatenation. When a catastrophic regression occurs after adding features, first disable the new features to confirm the base pipeline is intact, then re-ena
    evidence: ✓ Predictions or new features no longer match the original sample identifiers or column order. | ✓ No end-to-end run has yet produced a verified prediction file. | ✗ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.57175 → 0.81692 (+0.24517)
- expert 60197293 (Expert) · learning · v88→v92   Before appending external columns to the feature list, explicitly drop all non-feature columns (identifiers, raw text, target labels). Print the resulting column names to verify. If a large score regression occurs after adding features, inspect whether identifier or target columns leaked into the fe
    evidence: ✓ Predictions or new features no longer match the original sample identifiers or column order. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.81738
- expert 55987255 (Master) · learning · v46→v47   After changing the number of output components in any feature-generation step, search the entire codebase for every hard-coded reference to the old component count—especially column name lists, loop ranges, and array slices—and update them all to match the new value. Ideally, derive the count from t
    evidence: ✓ Predictions or new features no longer match the original sample identifiers or column order. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.81750
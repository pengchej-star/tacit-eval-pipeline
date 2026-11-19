# Correct aggregation arithmetic  `T.1.3`   15 edits, 0 experts
6 scored cases (improvement signed by each competition's direction), median +0.00075, 6 improved


- expert 28984551 · amex · v7→v9   After each integration step, verify that (1) each model group's predictions are stored under uniquely prefixed columns, (2) the averaging step references exactly the intended column prefixes, and (3) the final accumulation or slicing selects the correct columns/rows. Submit or validate after each fi
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✗ Execution stops at an import, file access, device operation, or library call. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score n/a → 0.79520 (higher is better)
- expert 17616127 · commonlitreadabilityprize · v47→v49   After writing the aggregation code, print or assert the shape and summary statistics (mean, std) of each component array and the final stacked array before submission. If any component is missing or has unexpected values, the bug surfaces immediately without needing a leaderboard probe.
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score n/a → 0.47952 (lower is better)
- expert 17616127 · commonlitreadabilityprize · v71→v72   Always cast prediction vectors to a numeric array type before performing weighted averaging or any element-wise arithmetic. This is a zero-cost defensive step that prevents hard-to-detect bugs where list replication silently replaces element-wise operations.
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.45558 (lower is better)
- expert 17616127 · commonlitreadabilityprize · v82→v85   Before debugging model weights or architecture, verify that all prediction arrays share the same data type (numeric arrays, not lists) so arithmetic broadcasting works correctly, and confirm that averaging weights sum to 1.0 with the correct denominator matching the actual number of components.
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✗ Execution stops at an import, file access, device operation, or library call. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score n/a → 0.45142 (lower is better)
- expert 17616127 · commonlitreadabilityprize · v87→v88   Before computing any weighted combination, explicitly convert every prediction vector to the same array type. Verify the output shape and a few sample values match expectations before writing the submission.
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.45371 (lower is better)
- expert 17616127 · commonlitreadabilityprize · v98→v100   After constructing each ensemble output, print or log summary statistics (mean, std, first few values) of every component. If two supposedly different ensembles produce identical outputs, inspect variable references. Always verify diversity before averaging.
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score 0.45076 → 0.45001 (lower is better; improved by 0.00075)
- expert 18851026 · commonlitreadabilityprize · v19→v20   Always average (divide by N) the predictions within a group before multiplying by the group weight, so the group's total contribution equals exactly the intended fraction regardless of how many members it contains.
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score 1.12557 → 0.45875 (lower is better; improved by 0.66681)
- expert 18851026 · commonlitreadabilityprize · v18→v20   Whenever a member is added or removed from an ensemble group, immediately re-check and re-normalize the combination formula (averages, weight sums) so the total still sums to 1.0 or the intended proportion. Validate on a quick sanity check (e.g., prediction range) before submitting.
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✓ Sample identifiers or feature columns differ between prediction sources or stages. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.45875 (lower is better)
- expert 18851026 · commonlitreadabilityprize · v23→v24   After every change to ensemble membership, audit the averaging formula to ensure the divisor matches the actual number of terms. Be aware that fixing such a bug can worsen the score if the incorrect divisor was accidentally acting as a beneficial shrinkage factor — in that case, the real lever is me
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.45925 (lower is better)
- expert 18423958 · commonlitreadabilityprize · v20→v21   Inspect the arithmetic of the blending expression for syntax or operator errors (missing operators, wrong variable names, incorrect weight sums). A single missing operator in a weighted average can silently produce garbage predictions. Fix and re-run before concluding the new model hurts the ensembl
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.46031 (lower is better)
- expert 75145694 · equity · v11→v14   Add logging inside the fold loop to verify which code paths execute per fold. Ensure the prediction call is scoped to the same block where its required inputs are prepared. Submit or validate after each scoping change to confirm the correct placement, since the error is silent (no crash, just wrong 
    evidence: ✗ Execution stops at an import, file access, device operation, or library call. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation. | ✓ The executed ensemble does not match its configured members or weights.
    leaderboard score 0.69043 → 0.69067 (higher is better; improved by 0.00024)
- expert 75145694 · equity · v30→v31   After any refactor of the inference loop, verify that the prediction call executes for every fold by adding an assertion or log statement that counts predictions per fold. If the same bug pattern has appeared before, add a permanent guard (e.g., assert that the number of prediction batches equals th
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✗ Execution stops at an import, file access, device operation, or library call. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score 0.69145 → 0.69146 (higher is better; improved by 0.00001)
- expert 75145694 · equity · v33→v34   After every code addition that modifies the inference loop, explicitly verify that the prediction call is inside the block where features are prepared. Consider extracting the feature-generation-then-predict pattern into a function to prevent scope/indentation errors from recurring.
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score 0.69296 → 0.69296 (higher is better; improved by 0.00000)
- expert 52860091 · hms · v18→v20   Verify that the append/accumulate step is inside the correct loop scope. A quick sanity check: the number of accumulated arrays should equal the number of models × folds. If the ensemble score equals one member's score, inspect the loop for off-by-one or indentation bugs before concluding the models
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✗ Execution stops at an import, file access, device operation, or library call. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score 0.31220 → 0.28947 (lower is better; improved by 0.02273)
- expert 55621328 · learning · v31→v32   After averaging predictions across checkpoints, assert that the resulting tensor has the expected shape (num_samples × num_classes) before applying argmax. Print or log a few sample rows of the averaged probabilities to verify they sum to 1 and look reasonable before generating the submission.
    evidence: ✓ The executed ensemble does not match its configured members or weights. | ✓ Written predictions have the wrong direction, range, normalization, or source variable. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.79585 (higher is better)
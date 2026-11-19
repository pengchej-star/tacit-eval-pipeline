# Verify checkpoint selection and file discovery  `T.1.3`   3 edits, 0 experts
3 scored cases, median improvement +0.00091, 2 improved


- expert 7613444 (Contributor) · google · v11→v12   Log or print the full resolved file path before loading each checkpoint, and add an explicit existence check or assertion. This catches naming mismatches early and prevents silent omission of fold models from the ensemble.
    evidence: ✓ The selected checkpoint files are missing, ambiguous or different from the intended run.
    leaderboard score 0.39956 → 0.40047 (+0.00091)
- expert 6803050 (Master) · google · v37→v39   When a score drops unexpectedly after changing checkpoint paths, verify every path string character-by-character. Load one fold at a time and check that the model produces non-trivial outputs before running the full ensemble. Treat any sudden regression after a path change as a path bug until proven
    evidence: ✓ The selected checkpoint files are missing, ambiguous or different from the intended run. | ✗ Execution fails during import, file access or device initialization.
    leaderboard score 0.29940 → 0.38287 (+0.08347)
- expert 7606235 (Master) · google · v18→v23   Before submitting, verify that all checkpoint paths resolve correctly and that the ensemble code actually loads and averages the intended models (e.g., print model count and a sample prediction). Use a local validation split to pre-screen checkpoint combinations and only submit the most promising on
    evidence: ✓ The selected checkpoint files are missing, ambiguous or different from the intended run. | ✓ The ensemble output cannot be reproduced from its intended component arrays and weights. | ✗ Execution fails during import, file access or device initialization.
    leaderboard score 0.38871 → 0.38785 (-0.00086)
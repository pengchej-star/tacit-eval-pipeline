# Compare outputs across a refactor  `T.2.2.6`   3 edits, 0 experts
2 scored cases, median improvement +0.00080, 2 improved


- expert 18851026 (Master) · commonlitreadabilityprize · v30→v32   Before refactoring, record the exact submission file or predictions as a reference. After cleanup, compare new predictions element-wise against the reference to confirm numerical equivalence before submitting. Any discrepancy signals that the refactor accidentally changed the pipeline (e.g., dropped
    evidence: ✓ A supposedly behavior-preserving refactor has changed predictions or has not been checked for equivalence. | ✓ The inference code contains a duplicated or residual preprocessing/transform step that was not present during training.
    leaderboard score 0.45835 → 0.45914 (+0.00080)
- expert 77450317 (Grandmaster) · equity · v26→v28   Before and after the refactor, generate predictions on the same data and compare them numerically (e.g., correlation or max absolute difference) to confirm the outputs are identical. Submit the refactored version promptly to catch regressions early, rather than batching further changes on top of an 
    evidence: ✓ A supposedly behavior-preserving refactor has changed predictions or has not been checked for equivalence.
    leaderboard score 0.69702 → n/a
- expert 73937748 (Master) · equity · v15→v20   After loading pretrained models, ensure the predict function returns both out-of-fold and test predictions. Validate the OOF concordance/metric locally before submitting. If the score drops catastrophically, check that all model outputs are actually collected and passed to the ensemble blend, then i
    evidence: ✓ A supposedly behavior-preserving refactor has changed predictions or has not been checked for equivalence. | ✓ Outputs are constant across substantial edits or some configured members never produce predictions. | ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✓ Model or artifact file paths reference an outdated directory that no longer matches the current environment's pretrained-model location.
    leaderboard score 0.68814 → 0.68894 (+0.00080)
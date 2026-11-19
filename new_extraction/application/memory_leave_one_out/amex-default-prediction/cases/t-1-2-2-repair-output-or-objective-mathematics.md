# Repair output or objective mathematics  `T.1.2.2`   3 edits, 0 experts
2 scored cases, median improvement +0.02657, 2 improved


- expert 73937748 (Master) · equity · v46→v48   Always divide the accumulated test predictions by the number of folds to produce a proper average. Verify this by checking that the scale of out-of-fold and test predictions is comparable. A mismatch in aggregation logic is a common silent bug that degrades ensemble scores.
    evidence: ✓ The fold-averaging divisor is applied inside the per-fold loop instead of once after all folds, causing incorrect scaling of predictions. | ✓ A hand-calculated blend disagrees with the implemented blend.
    leaderboard score 0.69140 → 0.69172 (+0.00032)
- expert 55621328 (Master) · learning · v31→v32   After averaging predictions across checkpoints, assert that the resulting tensor has the expected shape (num_samples × num_classes) before applying argmax. Print or log a few sample rows of the averaged probabilities to verify they sum to 1 and look reasonable before generating the submission.
    evidence: ✓ Output axes, activation, or loss derivatives disagree with the target definition. | ✓ The model loading paths point to wrong experiment directories or files, causing incorrect or failed model loads.
    leaderboard score n/a → 0.79585
- expert 58130512 (Master) · learning · v10→v12   Audit the custom objective's gradient and Hessian computation for correctness. Ensure the Hessian is a proper second derivative rather than a placeholder (e.g., all ones). Remove unnecessary complexity like per-class weighting that can destabilize training. Move shared constants out of the function 
    evidence: ✓ Output axes, activation, or loss derivatives disagree with the target definition.
    leaderboard score 0.79271 → 0.81929 (+0.02657)
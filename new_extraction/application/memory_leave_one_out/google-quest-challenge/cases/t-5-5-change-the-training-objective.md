# Change the training objective  `T.5.5`   7 edits, 0 experts
6 scored cases (improvement signed by each competition's direction), median +0.00713, 4 improved


- expert 27389424 · amex · v85→v86   Try alternative built-in loss functions (e.g., cross-entropy variants) one at a time and compare leaderboard scores. If the score drops, revert immediately; the default binary cross-entropy loss is often already well-suited even for custom metrics because it preserves probability calibration and ran
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✗ Training stops before convergence or continues after validation deterioration. | ✓ The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors. | ✗ A lower learning rate was introduced without increasing the iteration budget.
    leaderboard score n/a → 0.79317 (higher is better)
- expert 49576186 · hms · v68→v70   Replace the surrogate loss with the actual evaluation metric (or its differentiable equivalent) as the training objective. When the metric is a divergence between distributions and labels are already soft distributions, train directly with that divergence as the loss function.
    evidence: ✓ The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors.
    leaderboard score 0.37990 → 0.35346 (lower is better; improved by 0.02644)
- expert 59253662 · learning · v34→v36   Try a custom training objective that approximates the evaluation metric, and separately try data-driven threshold optimization on validation folds. Test each change independently. If neither improves validation or leaderboard score, revert to the simpler fixed-threshold approach—custom objectives ca
    evidence: ✓ The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors.
    leaderboard score 0.81851 → 0.81826 (higher is better; worse by 0.00025)
- expert 58130512 · learning · v10→v12   Audit the custom objective's gradient and Hessian computation for correctness. Ensure the Hessian is a proper second derivative rather than a placeholder (e.g., all ones). Remove unnecessary complexity like per-class weighting that can destabilize training. Move shared constants out of the function 
    evidence: ✓ The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors. | ✓ Loss curves indicate slow convergence, oscillation, or sensitivity to a changed objective.
    leaderboard score 0.79271 → 0.81929 (higher is better; improved by 0.02657)
- expert 58130512 · learning · v67→v72   Sweep the scalar in a neighborhood around the current best, testing both large deviations and small perturbations. Expect the response surface to be fairly peaked: large jumps degrade performance noticeably, while small adjustments (a few percent relative change) can yield modest gains. Stop when sc
    evidence: ✓ The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors. | ✓ Loss curves indicate slow convergence, oscillation, or sensitivity to a changed objective.
    leaderboard score 0.82432 → 0.82157 (higher is better; worse by 0.00275)
- expert 58130512 · learning · v69→v71   Try replacing the analytic hessian with a constant vector of ones as a baseline. This simplifies tuning and can stabilize training. Then compare against the true hessian with a well-tuned loss scalar. Use the constant-hessian variant as a stable reference point while sweeping other loss hyperparamet
    evidence: ✓ Loss curves indicate slow convergence, oscillation, or sensitivity to a changed objective. | ✓ The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors.
    leaderboard score 0.82207 → 0.82372 (higher is better; improved by 0.00165)
- expert 13542132 · ranzcr · v13→v14   Switch to a different lever entirely—change the loss function (e.g., from standard cross-entropy to a class-imbalance-aware loss) and simultaneously adjust the learning rate upward to compensate for the new loss landscape. Increase regularization (dropout) to offset the higher learning rate. Simplif
    evidence: ✓ The current loss does not capture ordinal, ranking, soft-label, or other task-specific errors.
    leaderboard score 0.94397 → 0.95109 (higher is better; improved by 0.00713)
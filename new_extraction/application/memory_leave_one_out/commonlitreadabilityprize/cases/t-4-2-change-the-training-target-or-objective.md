# Change the training target or objective  `T.4.2`   12 edits, 0 experts
10 scored cases (improvement signed by each competition's direction), median +0.00101, 7 improved


- expert 27389424 · amex · v85→v86   Try alternative built-in loss functions (e.g., cross-entropy variants) one at a time and compare leaderboard scores. If the score drops, revert immediately; the default binary cross-entropy loss is often already well-suited even for custom metrics because it preserves probability calibration and ran
    evidence: ✓ The loss and output activation optimize a different target structure from the task metric. | ✗ Training stops while validation is still improving or a lower learning rate has not been given enough rounds. | ✗ The dataset is limited and label-preserving transformations represent variation expected at test time.
    leaderboard score n/a → 0.79317 (higher is better)
- expert 75145694 · equity · v32→v33   Implement a pairwise ranking loss (optionally with focal weighting to emphasize hard pairs) for a tabular neural network with categorical embeddings. Add it as a new ensemble member. Expect a small but positive marginal gain from the loss-metric alignment, mainly through diversity in the blend.
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✓ The loss and output activation optimize a different target structure from the task metric.
    leaderboard score 0.69285 → 0.69296 (higher is better; improved by 0.00010)
- expert 73937748 · equity · v3→v5   Attack on multiple fronts simultaneously: (1) engineer domain-informed interaction and ratio features, (2) create several survival-target transforms so each model sees a different view of the label, (3) add a third gradient-boosted tree variant, and (4) use a hyperparameter search tool to optimize b
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✓ Training improves while validation degrades as model complexity or feature count grows. | ✓ The loss and output activation optimize a different target structure from the task metric.
    leaderboard score 0.67907 → 0.68705 (higher is better; improved by 0.00798)
- expert 7253130 · google · v1→v2   Switch the output activation to sigmoid (element-wise) and the loss to binary cross-entropy so each output is independently squashed to [0,1]. This correctly models independent targets without the sum-to-one constraint.
    evidence: ✓ The loss and output activation optimize a different target structure from the task metric.
    leaderboard score 0.25815 → n/a (higher is better)
- expert 49576186 · hms · v68→v70   Replace the surrogate loss with the actual evaluation metric (or its differentiable equivalent) as the training objective. When the metric is a divergence between distributions and labels are already soft distributions, train directly with that divergence as the loss function.
    evidence: ✓ The loss and output activation optimize a different target structure from the task metric.
    leaderboard score 0.37990 → 0.35346 (lower is better; improved by 0.02644)
- expert 55621328 · learning · v30→v33   Implement a classification head that outputs softmax probabilities over ordinal classes and takes argmax. Compare its leaderboard score against the regression + optimized-rounding baseline. If classification underperforms, retain the regression approach—threshold optimization on continuous outputs o
    evidence: ✓ The loss and output activation optimize a different target structure from the task metric. | ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression.
    leaderboard score 0.80353 → 0.79406 (higher is better; worse by 0.00947)
- expert 55621328 · learning · v102→v103   Train or obtain checkpoints using an ordinal prediction formulation and swap them into the inference pipeline. Compare leaderboard scores directly; if the ordinal variant matches or exceeds regression, iterate on checkpoint selection and blend weights within that formulation.
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✓ The loss and output activation optimize a different target structure from the task metric.
    leaderboard score 0.82366 → 0.82467 (higher is better; improved by 0.00101)
- expert 59253662 · learning · v34→v36   Try a custom training objective that approximates the evaluation metric, and separately try data-driven threshold optimization on validation folds. Test each change independently. If neither improves validation or leaderboard score, revert to the simpler fixed-threshold approach—custom objectives ca
    evidence: ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression. | ✓ The loss and output activation optimize a different target structure from the task metric.
    leaderboard score 0.81851 → 0.81826 (higher is better; worse by 0.00025)
- expert 58130512 · learning · v67→v72   Sweep the scalar in a neighborhood around the current best, testing both large deviations and small perturbations. Expect the response surface to be fairly peaked: large jumps degrade performance noticeably, while small adjustments (a few percent relative change) can yield modest gains. Stop when sc
    evidence: ✓ The loss and output activation optimize a different target structure from the task metric. | ✗ Repeated augmentation-strength changes have already failed to improve the fixed baseline.
    leaderboard score 0.82432 → 0.82157 (higher is better; worse by 0.00275)
- expert 58130512 · learning · v69→v71   Try replacing the analytic hessian with a constant vector of ones as a baseline. This simplifies tuning and can stabilize training. Then compare against the true hessian with a well-tuned loss scalar. Use the constant-hessian variant as a stable reference point while sweeping other loss hyperparamet
    evidence: ✓ The loss and output activation optimize a different target structure from the task metric.
    leaderboard score 0.82207 → 0.82372 (higher is better; improved by 0.00165)
- expert 58130512 · learning · v100→v102   Compute the constants once from the full training set (or an oversampled version reflecting the target distribution) and keep them fixed across all folds. This reduces fold-to-fold variance in the learned models and produces a more stable ensemble.
    evidence: ✓ The loss and output activation optimize a different target structure from the task metric. | ✓ Training stops while validation is still improving or a lower learning rate has not been given enough rounds. | ✓ Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression.
    leaderboard score 0.82301 → 0.82313 (higher is better; improved by 0.00012)
- expert 13542132 · ranzcr · v13→v14   Increase the learning rate (e.g., double it) to compensate for the smaller effective gradients, and raise regularization strength proportionally to prevent the larger step size from overfitting. Treat the loss change as requiring a coordinated update of at least learning rate and regularization, not
    evidence: ✓ The loss and output activation optimize a different target structure from the task metric. | ✓ Repeated augmentation-strength changes have already failed to improve the fixed baseline.
    leaderboard score 0.94397 → 0.95109 (higher is better; improved by 0.00713)
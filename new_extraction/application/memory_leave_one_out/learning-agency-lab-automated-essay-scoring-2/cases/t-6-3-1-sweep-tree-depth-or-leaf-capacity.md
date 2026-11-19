# Sweep tree depth or leaf capacity  `T.6.3.1`   11 edits, 0 experts
5 scored cases, median improvement +0.00011, 4 improved


- expert 29588171 (Master) · amex · v34→v35   Increase the leaf count (e.g., roughly double or triple the default) and submit to measure the effect. If the score drops, revert: when the model's weight in the blend is small, overfitting from higher capacity is likely to hurt more than the added expressiveness helps.
    evidence: ✓ Training fit is poor under shallow trees or prior depth changes show a clear capacity effect. | ✓ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble.
    leaderboard score 0.79980 → 0.79963 (-0.00017)
- expert 27389424 (Grandmaster) · amex · v72→v82   Sweep max depth upward from a very shallow value (e.g., 2) in increments of 1, evaluating each on validation. Submit the best-performing depth to the leaderboard. If adding another regularization lever (e.g., minimum samples per leaf), repeat the depth sweep with that lever active to check for inter
    evidence: ✗ Every tree sees all rows and columns and the model overfits after feature selection. | ✓ Training fit is poor under shallow trees or prior depth changes show a clear capacity effect. | ✗ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble. | ✓ Training improves while validation stagnates under the current tree capacity.
    leaderboard score 0.79333 → n/a
- expert 27836972 (Expert) · amex · v33→v36   Try doubling the tree depth and reducing the learning rate by roughly 40%, keeping the old parameters commented out for easy rollback. Evaluate on local validation before submitting. If validation does not clearly improve, revert and pursue other levers (e.g., more features) rather than continuing t
    evidence: ✓ Training fit is poor under shallow trees or prior depth changes show a clear capacity effect. | ✗ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble. | ✓ Lower learning rates reach the round cap or trigger stopping before sustained convergence.
    leaderboard score n/a → n/a
- expert 27836972 (Expert) · amex · v70→v71   Return to hyperparameter tuning: increase tree depth moderately, lower the learning rate, raise regularization (L2 penalty, minimum child weight, row/column subsampling), and optionally adjust the number of CV folds. Combine these changes in one round; the interaction between deeper trees and strong
    evidence: ✓ Every tree sees all rows and columns and the model overfits after feature selection. | ✓ Lower learning rates reach the round cap or trigger stopping before sustained convergence.
    leaderboard score n/a → 0.79637
- expert 27799930 (Contributor) · amex · v3→v11   Try two complementary strategies and compare on the validation metric: (1) reduce the learning rate and increase subsampling to reduce variance, or (2) keep a moderate learning rate but add explicit regularization (L2, minimum leaf weight, pruning threshold) and enable early stopping with a held-out
    evidence: ✓ Every tree sees all rows and columns and the model overfits after feature selection. | ✗ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble. | ✓ Lower learning rates reach the round cap or trigger stopping before sustained convergence.
    leaderboard score n/a → n/a
- expert 27825577 (Expert) · amex · v1→v3   Sweep tree depth in one direction by at least two or three steps even if the first step worsens the score. Evaluate each on a held-out or public leaderboard metric before concluding the direction is harmful. The optimum may be non-adjacent to the starting point.
    evidence: ✓ Training fit is poor under shallow trees or prior depth changes show a clear capacity effect.
    leaderboard score 0.79285 → 0.79384 (+0.00099)
- expert 27825577 (Expert) · amex · v5→v11   Sweep the learning rate across a wide range (e.g., 0.01 to 0.2) while co-adjusting tree depth. Very low rates may underfit if early stopping triggers too soon; very high rates may overfit. After bracketing, narrow in on the best region. Pair lower learning rates with shallower trees and longer early
    evidence: ✓ Lower learning rates reach the round cap or trigger stopping before sustained convergence. | ✗ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble. | ✓ Training fit is poor under shallow trees or prior depth changes show a clear capacity effect.
    leaderboard score n/a → 0.79425
- expert 27656049 (Expert) · amex · v2→v7   Increase tree capacity by raising the number of leaves and maximum depth substantially (e.g., by an order of magnitude), lower the learning rate by roughly half, and increase the maximum number of boosting rounds by several times. Pair these changes with early stopping on a validation set so the mod
    evidence: ✓ Training fit is poor under shallow trees or prior depth changes show a clear capacity effect. | ✗ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble. | ✓ Lower learning rates reach the round cap or trigger stopping before sustained convergence.
    leaderboard score n/a → n/a
- expert 27656049 (Expert) · amex · v9→v10   Increase the number of leaves while adding an explicit depth cap to allow richer but bounded trees. Remove column/row subsampling and L1 penalties to let the model use all information, relying on the depth cap and early stopping for regularization. Evaluate on the leaderboard; if the score improves 
    evidence: ✓ Training fit is poor under shallow trees or prior depth changes show a clear capacity effect. | ✓ Every tree sees all rows and columns and the model overfits after feature selection. | ✗ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble.
    leaderboard score 0.78607 → 0.78731 (+0.00124)
- expert 77347591 (Expert) · equity · v2→v3   Jointly adjust learning rate (lower it), number of boosting rounds (increase correspondingly), regularization strengths, subsampling ratios, and tree growth policies across all tree-based models in the ensemble. Expect only marginal gains (on the order of 0.01–0.02% of the metric) from a single roun
    evidence: ✓ Every tree sees all rows and columns and the model overfits after feature selection. | ✓ Lower learning rates reach the round cap or trigger stopping before sustained convergence.
    leaderboard score 0.69321 → 0.69332 (+0.00011)
- expert 73937748 (Master) · equity · v8→v11   Create dedicated hyperparameter configurations for each model variant (adjusting learning rate, tree count, regularization, depth). Expect diminishing returns: blend-weight optimization can mask individual model weaknesses, so per-model tuning often yields only marginal gains at this stage. Prioriti
    evidence: ✓ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble.
    leaderboard score 0.68946 → 0.68948 (+0.00002)
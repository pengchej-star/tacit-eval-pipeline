# Tune tree capacity  `T.5.1`   19 edits, 0 experts
10 scored cases, median improvement +0.00020, 7 improved


- expert 29588171 (Master) · amex · v34→v35   Increase the leaf count (e.g., roughly double or triple the default) and submit to measure the effect. If the score drops, revert: when the model's weight in the blend is small, overfitting from higher capacity is likely to hurt more than the added expressiveness helps.
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✗ The current boosting procedure has plateaued or its interface blocks required training controls.
    leaderboard score 0.79980 → 0.79963 (-0.00017)
- expert 29588171 (Master) · amex · v40→v41   When multiple successive increases in tree complexity (leaf count, depth) each fail to improve the leaderboard or validation metric, stop increasing capacity. The plateau or decline signals that the model is already at or past the useful complexity frontier for the available data, and further capaci
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count.
    leaderboard score 0.79943 → 0.79940 (-0.00003)
- expert 27389424 (Grandmaster) · amex · v72→v82   Sweep max depth upward from a very shallow value (e.g., 2) in increments of 1, evaluating each on validation. Submit the best-performing depth to the leaderboard. If adding another regularization lever (e.g., minimum samples per leaf), repeat the depth sweep with that lever active to check for inter
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score 0.79333 → n/a
- expert 27389424 (Grandmaster) · amex · v92→v95   Plot or track the marginal gain per increment. When the gain drops to a small fraction of the initial step's gain, try one more increment without committing. If it shows no meaningful improvement, revert to the last clearly beneficial value rather than the absolute maximum tested.
    evidence: ✓ Training stops before convergence or continues after validation deterioration. | ✓ Tree models show underfitting or overfitting associated with depth or leaf count.
    leaderboard score 0.79585 → n/a
- expert 27836972 (Expert) · amex · v70→v71   Return to hyperparameter tuning: increase tree depth moderately, lower the learning rate, raise regularization (L2 penalty, minimum child weight, row/column subsampling), and optionally adjust the number of CV folds. Combine these changes in one round; the interaction between deeper trees and strong
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✓ Training fit exceeds validation fit or newly added features increase instability. | ✓ Loss curves indicate slow convergence, oscillation, or sensitivity to a changed objective.
    leaderboard score n/a → 0.79637
- expert 27799930 (Contributor) · amex · v3→v11   Try two complementary strategies and compare on the validation metric: (1) reduce the learning rate and increase subsampling to reduce variance, or (2) keep a moderate learning rate but add explicit regularization (L2, minimum leaf weight, pruning threshold) and enable early stopping with a held-out
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability. | ✓ Loss curves indicate slow convergence, oscillation, or sensitivity to a changed objective. | ✓ A lower learning rate was introduced without increasing the iteration budget. | ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✓ Training stops before convergence or continues after validation deterioration.
    leaderboard score n/a → n/a
- expert 27825577 (Expert) · amex · v1→v3   Sweep tree depth in one direction by at least two or three steps even if the first step worsens the score. Evaluate each on a held-out or public leaderboard metric before concluding the direction is harmful. The optimum may be non-adjacent to the starting point.
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count.
    leaderboard score 0.79285 → 0.79384 (+0.00099)
- expert 27656049 (Expert) · amex · v2→v7   Increase tree capacity by raising the number of leaves and maximum depth substantially (e.g., by an order of magnitude), lower the learning rate by roughly half, and increase the maximum number of boosting rounds by several times. Pair these changes with early stopping on a validation set so the mod
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✓ Training stops before convergence or continues after validation deterioration. | ✓ A lower learning rate was introduced without increasing the iteration budget.
    leaderboard score n/a → n/a
- expert 27656049 (Expert) · amex · v9→v10   Increase the number of leaves while adding an explicit depth cap to allow richer but bounded trees. Remove column/row subsampling and L1 penalties to let the model use all information, relying on the depth cap and early stopping for regularization. Evaluate on the leaderboard; if the score improves 
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score 0.78607 → 0.78731 (+0.00124)
- expert 77347591 (Expert) · equity · v2→v3   Jointly adjust learning rate (lower it), number of boosting rounds (increase correspondingly), regularization strengths, subsampling ratios, and tree growth policies across all tree-based models in the ensemble. Expect only marginal gains (on the order of 0.01–0.02% of the metric) from a single roun
    evidence: ✓ A lower learning rate was introduced without increasing the iteration budget.
    leaderboard score 0.69321 → 0.69332 (+0.00011)
- expert 73937748 (Master) · equity · v4→v5   Reduce each model's number of boosting rounds substantially (e.g., to roughly one-sixth of the standalone value) when ensembling multiple models, because the ensemble itself provides capacity. Reinvest the saved compute into more thorough blend-weight optimization (increase search trials proportiona
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score n/a → 0.68705
- expert 73937748 (Master) · equity · v8→v11   Create dedicated hyperparameter configurations for each model variant (adjusting learning rate, tree count, regularization, depth). Expect diminishing returns: blend-weight optimization can mask individual model weaknesses, so per-model tuning often yields only marginal gains at this stage. Prioriti
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✓ A lower learning rate was introduced without increasing the iteration budget.
    leaderboard score 0.68946 → 0.68948 (+0.00002)
- expert 53762022 (Contributor) · hms · v12→v13   Revert the specific hyperparameter that caused the initial regression to its previous value, then simultaneously adjust the other coupled settings (checkpoint selection, ensemble weights) that were tuned around the bad value. Bundling the revert with fresh tuning of dependent settings avoids interme
    evidence: none recorded
    leaderboard score n/a → 0.28438
- expert 60759531 (Expert) · learning · v4→v8   When increasing max_depth, simultaneously reduce num_leaves to constrain effective tree complexity and prevent overfitting. Avoid compensating a lower learning rate with a much larger number of boosting rounds without early stopping, as this often overfits. Change one complexity axis at a time and v
    evidence: ✓ A lower learning rate was introduced without increasing the iteration budget. | ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✓ Loss curves indicate slow convergence, oscillation, or sensitivity to a changed objective.
    leaderboard score 0.81909 → 0.82029 (+0.00121)
- expert 58130512 (Master) · learning · v54→v56   Change at most one or two regularization-related hyperparameters at a time rather than reducing depth, number of estimators, feature fraction, and regularization penalty all at once. Simultaneous large reductions risk underfitting and make it impossible to attribute the score change to any single fa
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score n/a → 0.81732
- expert 58527792 (Contributor) · learning · v2→v4   Make one small change at a time and submit. If the score drops, revert immediately rather than continuing to search in the worse direction. Treat the prior configuration as a strong default and only keep changes that show measurable improvement.
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count.
    leaderboard score 0.82214 → 0.82214 (+0.00000)
- expert 55987255 (Master) · learning · v166→v172   Reduce tree depth and number of boosting rounds in a coordinated sweep: halve the number of estimators and reduce max depth by 1-2 per step. After each reduction, check validation performance. Continue reducing until validation stops improving. Typical effective reductions can be 2-4x fewer trees an
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count. | ✓ Training stops before convergence or continues after validation deterioration. | ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score n/a → 0.80932
- expert 55987255 (Master) · learning · v172→v174   Sweep tree depth by ±1 from the current value, submit each variant to the leaderboard, and keep the depth that scores best. If the original value wins, revert. Do not change other hyperparameters simultaneously so the effect is isolated.
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count.
    leaderboard score 0.80932 → 0.81014 (+0.00082)
- expert 55591012 (Grandmaster) · learning · v50→v52   Increase the maximum tree depth moderately (e.g., from the default to roughly 1.5–2× deeper). Evaluate on the leaderboard or a held-out set. If the score improves, keep the deeper setting; if it drops, revert. Change only one structural hyperparameter at a time to isolate its effect.
    evidence: ✓ Tree models show underfitting or overfitting associated with depth or leaf count.
    leaderboard score 0.82075 → 0.82094 (+0.00020)
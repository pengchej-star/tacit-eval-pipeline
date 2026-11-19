# Tune training duration  `T.5.4`   6 edits, 0 experts
2 scored cases, median improvement +0.00226, 1 improved


- expert 27389424 (Grandmaster) · amex · v89→v95   Sweep the number of iterations upward in fixed increments, submitting or evaluating at each step. Track the metric gain per increment; when the marginal gain drops to near zero or turns negative, stop and select the value with the best trade-off between score and training cost. Be prepared to step b
    evidence: ✓ Training stops before convergence or continues after validation deterioration. | ✓ The current boosting procedure has plateaued or its interface blocks required training controls. | ✗ A lower learning rate was introduced without increasing the iteration budget.
    leaderboard score n/a → n/a
- expert 27799930 (Contributor) · amex · v27→v29   When adding many new features, slightly tighten early stopping patience (e.g., reduce by ~20%) to guard against overfitting on noise. Re-evaluate after pruning unhelpful features; the combination of a cleaner feature set and appropriate patience often yields a larger gain than either change alone.
    evidence: ✓ Training fit exceeds validation fit or newly added features increase instability. | ✓ Training stops before convergence or continues after validation deterioration. | ✗ A lower learning rate was introduced without increasing the iteration budget.
    leaderboard score n/a → 0.79350
- expert 27825577 (Expert) · amex · v11→v14   Sweep the early-stopping patience parameter across a range (e.g., halving and doubling the current value). When a lower learning rate is used, prefer a larger patience value to avoid premature stopping. If reducing patience degrades the score, revert to the larger value.
    evidence: ✓ Training stops before convergence or continues after validation deterioration. | ✓ A lower learning rate was introduced without increasing the iteration budget.
    leaderboard score 0.79425 → 0.79425 (+0.00000)
- expert 73937748 (Master) · equity · v47→v48   Increase the number of training epochs moderately (e.g., by 50-70%) and check whether the ensemble score improves. If it does, the network was under-trained. Monitor for overfitting by comparing validation metrics across epoch counts before committing.
    evidence: ✓ Training stops before convergence or continues after validation deterioration.
    leaderboard score 0.68945 → 0.69172 (+0.00226)
- expert 60197293 (Expert) · learning · v99→v101   Test early stopping in a validation-only run. If removing early stopping and instead reducing the regularization penalty yields a better validation or leaderboard score, prefer the fixed-iteration approach with lighter regularization. Avoid changing both early stopping and regularization simultaneou
    evidence: ✓ Training stops before convergence or continues after validation deterioration. | ✓ Training fit exceeds validation fit or newly added features increase instability.
    leaderboard score n/a → 0.82142
- expert 55987255 (Master) · learning · v47→v56   Sweep the number of boosting rounds in one direction (e.g., halving repeatedly: 900→400→200→100) while monitoring the validation metric. If validation improves as rounds decrease, the model was overfitting; stop when validation starts degrading. This is faster than grid search when the direction of 
    evidence: ✓ Training stops before convergence or continues after validation deterioration. | ✓ Training fit exceeds validation fit or newly added features increase instability. | ✓ Tree models show underfitting or overfitting associated with depth or leaf count.
    leaderboard score 0.81750 → n/a
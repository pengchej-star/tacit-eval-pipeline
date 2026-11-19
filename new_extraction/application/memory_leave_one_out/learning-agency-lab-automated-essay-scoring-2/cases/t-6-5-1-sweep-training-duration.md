# Sweep training duration  `T.6.5.1`   4 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00273, 2 improved


- expert 27389424 · amex · v89→v95   Sweep the number of iterations upward in fixed increments, submitting or evaluating at each step. Track the metric gain per increment; when the marginal gain drops to near zero or turns negative, stop and select the value with the best trade-off between score and training cost. Be prepared to step b
    evidence: ✓ The metric is still improving at the training cap or extra epochs have started to overfit. | ✓ Stopping occurs during noisy short plateaus, especially with a reduced learning rate.
    leaderboard score n/a → n/a (higher is better)
- expert 73937748 · equity · v47→v48   Increase the number of training epochs moderately (e.g., by 50-70%) and check whether the ensemble score improves. If it does, the network was under-trained. Monitor for overfitting by comparing validation metrics across epoch counts before committing.
    evidence: ✓ The metric is still improving at the training cap or extra epochs have started to overfit. | ✗ Several compatible trained states already exist with different validation results.
    leaderboard score 0.68945 → 0.69172 (higher is better; improved by 0.00226)
- expert 7613444 · google · v3→v5   Start with a small number of epochs (2–4) and compare adjacent values. Prefer fewer epochs when the dataset is small; even a single extra epoch can cause overfitting. Submit or validate both to confirm, and keep the shorter schedule if scores are close or the longer one is worse.
    evidence: ✗ Several compatible trained states already exist with different validation results. | ✓ The metric is still improving at the training cap or extra epochs have started to overfit.
    leaderboard score n/a → 0.39802 (higher is better)
- expert 7573212 · google · v4→v5   When expanding a fine-tuned model with new feature branches, increase the number of training epochs modestly and consider reducing batch size to provide more gradient updates per epoch. Validate that the combined change improves the metric before attributing gains to features vs. training schedule s
    evidence: ✓ The metric is still improving at the training cap or extra epochs have started to overfit.
    leaderboard score 0.38324 → 0.38598 (higher is better; improved by 0.00273)
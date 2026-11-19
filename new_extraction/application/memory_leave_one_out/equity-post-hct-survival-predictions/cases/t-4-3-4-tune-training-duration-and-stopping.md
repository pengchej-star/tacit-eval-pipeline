# Tune training duration and stopping  `T.4.3.4`   10 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00201, 2 improved


- expert 27389424 · amex · v66→v70   When using early stopping, test learning rates across at least one order of magnitude. If a lower rate degrades the score, it likely means the model is stopping before it has converged. Increase the rate (or increase patience/max iterations) and verify with a leaderboard or validation check.
    evidence: ✓ Loss is unstable or learning is too slow at the current step size. | ✓ Training hits its round limit or stops while the monitored metric is still improving. | ✗ Several compatible snapshots already exist but have not been compared under one inference configuration.
    leaderboard score 0.79083 → 0.79285 (higher is better; improved by 0.00201)
- expert 27389424 · amex · v89→v95   Sweep the number of iterations upward in fixed increments, submitting or evaluating at each step. Track the metric gain per increment; when the marginal gain drops to near zero or turns negative, stop and select the value with the best trade-off between score and training cost. Be prepared to step b
    evidence: ✓ Training hits its round limit or stops while the monitored metric is still improving. | ✗ Loss is unstable or learning is too slow at the current step size. | ✗ Several compatible snapshots already exist but have not been compared under one inference configuration. | ✗ Training fits well but validation worsens as depth or leaf count increases. | ✗ Generalization degrades despite adequate convergence and a fixed feature set.
    leaderboard score n/a → n/a (higher is better)
- expert 27799930 · amex · v13→v16   First set the number of rounds much higher than needed (e.g., 10–20× the current value) and rely on early stopping to find the effective count. Then halve the learning rate and proportionally adjust the round budget; the early-stopping callback will still protect against overfitting while the smalle
    evidence: ✓ Training hits its round limit or stops while the monitored metric is still improving. | ✓ Generalization degrades despite adequate convergence and a fixed feature set. | ✓ Loss is unstable or learning is too slow at the current step size.
    leaderboard score n/a → n/a (higher is better)
- expert 27799930 · amex · v27→v29   When adding many new features, slightly tighten early stopping patience (e.g., reduce by ~20%) to guard against overfitting on noise. Re-evaluate after pruning unhelpful features; the combination of a cleaner feature set and appropriate patience often yields a larger gain than either change alone.
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set. | ✗ Training hits its round limit or stops while the monitored metric is still improving.
    leaderboard score n/a → 0.79350 (higher is better)
- expert 27825577 · amex · v11→v14   Sweep the early-stopping patience parameter across a range (e.g., halving and doubling the current value). When a lower learning rate is used, prefer a larger patience value to avoid premature stopping. If reducing patience degrades the score, revert to the larger value.
    evidence: ✗ Loss is unstable or learning is too slow at the current step size. | ✓ Training hits its round limit or stops while the monitored metric is still improving.
    leaderboard score 0.79425 → 0.79425 (higher is better; unchanged by 0.00000)
- expert 28093671 · amex · v34→v37   When expanding features, switch the evaluation metric to a standard smooth proxy (e.g., AUC or log-loss) for more stable early stopping. Increase the learning rate moderately to speed up convergence, set a generous boosting-round budget, and rely on early stopping to find the right number of rounds.
    evidence: ✓ Training hits its round limit or stops while the monitored metric is still improving. | ✓ Loss is unstable or learning is too slow at the current step size.
    leaderboard score n/a → 0.79304 (higher is better)
- expert 7613444 · google · v3→v5   Start with a small number of epochs (2–4) and compare adjacent values. Prefer fewer epochs when the dataset is small; even a single extra epoch can cause overfitting. Submit or validate both to confirm, and keep the shorter schedule if scores are close or the longer one is worse.
    evidence: ✓ Training hits its round limit or stops while the monitored metric is still improving. | ✓ Generalization degrades despite adequate convergence and a fixed feature set.
    leaderboard score n/a → 0.39802 (higher is better)
- expert 7573212 · google · v4→v5   When expanding a fine-tuned model with new feature branches, increase the number of training epochs modestly and consider reducing batch size to provide more gradient updates per epoch. Validate that the combined change improves the metric before attributing gains to features vs. training schedule s
    evidence: ✓ Training hits its round limit or stops while the monitored metric is still improving.
    leaderboard score 0.38324 → 0.38598 (higher is better; improved by 0.00273)
- expert 60197293 · learning · v99→v101   Test early stopping in a validation-only run. If removing early stopping and instead reducing the regularization penalty yields a better validation or leaderboard score, prefer the fixed-iteration approach with lighter regularization. Avoid changing both early stopping and regularization simultaneou
    evidence: ✓ Training hits its round limit or stops while the monitored metric is still improving. | ✓ Generalization degrades despite adequate convergence and a fixed feature set.
    leaderboard score n/a → 0.82142 (higher is better)
- expert 55987255 · learning · v47→v56   Sweep the number of boosting rounds in one direction (e.g., halving repeatedly: 900→400→200→100) while monitoring the validation metric. If validation improves as rounds decrease, the model was overfitting; stop when validation starts degrading. This is faster than grid search when the direction of 
    evidence: ✓ Generalization degrades despite adequate convergence and a fixed feature set. | ✗ Training hits its round limit or stops while the monitored metric is still improving. | ✗ Loss is unstable or learning is too slow at the current step size.
    leaderboard score 0.81750 → n/a (higher is better)
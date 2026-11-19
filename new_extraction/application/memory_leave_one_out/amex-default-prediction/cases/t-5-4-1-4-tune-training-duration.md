# Tune training duration  `T.5.4.1.4`   3 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00273, 2 improved


- expert 73937748 · equity · v47→v48   Increase the number of training epochs moderately (e.g., by 50-70%) and check whether the ensemble score improves. If it does, the network was under-trained. Monitor for overfitting by comparing validation metrics across epoch counts before committing.
    evidence: ✓ Validation is still improving at the final epoch or worsens well before it. | ✗ The proposed edit changes only one hyperparameter at a time, consistent with controlled experimentation.
    leaderboard score 0.68945 → 0.69172 (higher is better; improved by 0.00226)
- expert 7613444 · google · v3→v5   Start with a small number of epochs (2–4) and compare adjacent values. Prefer fewer epochs when the dataset is small; even a single extra epoch can cause overfitting. Submit or validate both to confirm, and keep the shorter schedule if scores are close or the longer one is worse.
    evidence: ✓ Validation is still improving at the final epoch or worsens well before it. | ✓ The proposed edit changes only one hyperparameter at a time, consistent with controlled experimentation.
    leaderboard score n/a → 0.39802 (higher is better)
- expert 7573212 · google · v4→v5   When expanding a fine-tuned model with new feature branches, increase the number of training epochs modestly and consider reducing batch size to provide more gradient updates per epoch. Validate that the combined change improves the metric before attributing gains to features vs. training schedule s
    evidence: ✗ The proposed edit changes only one hyperparameter at a time, consistent with controlled experimentation. | ✓ Newly added randomly-initialized parameters require more total gradient steps than the current training duration provides.
    leaderboard score 0.38324 → 0.38598 (higher is better; improved by 0.00273)
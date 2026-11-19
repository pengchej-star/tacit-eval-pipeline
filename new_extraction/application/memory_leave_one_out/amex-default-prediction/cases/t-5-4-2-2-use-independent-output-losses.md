# Use independent output losses  `T.5.4.2.2`   2 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00713, 1 improved


- expert 7253130 · google · v1→v2   Switch the output activation to sigmoid (element-wise) and the loss to binary cross-entropy so each output is independently squashed to [0,1]. This correctly models independent targets without the sum-to-one constraint.
    evidence: ✗ Targets are probability distributions and the evaluation uses distributional divergence. | ✓ Outputs are independent labels or bounded independent targets rather than mutually exclusive classes.
    leaderboard score 0.25815 → n/a (higher is better)
- expert 13542132 · ranzcr · v13→v14   Switch to a different lever entirely—change the loss function (e.g., from standard cross-entropy to a class-imbalance-aware loss) and simultaneously adjust the learning rate upward to compensate for the new loss landscape. Increase regularization (dropout) to offset the higher learning rate. Simplif
    evidence: ✗ Targets are probability distributions and the evaluation uses distributional divergence. | ✓ Outputs are independent labels or bounded independent targets rather than mutually exclusive classes.
    leaderboard score 0.94397 → 0.95109 (higher is better; improved by 0.00713)
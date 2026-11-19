# Compare regression, classification and ordinal outputs  `T.4.1.4`   4 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00101, 2 improved


- expert 7253130 · google · v1→v2   Switch the output activation to sigmoid (element-wise) and the loss to binary cross-entropy so each output is independently squashed to [0,1]. This correctly models independent targets without the sum-to-one constraint.
    evidence: ✓ The present output activation or label formulation mismatches the target structure.
    leaderboard score 0.25815 → n/a (higher is better)
- expert 55621328 · learning · v30→v33   Implement a classification head that outputs softmax probabilities over ordinal classes and takes argmax. Compare its leaderboard score against the regression + optimized-rounding baseline. If classification underperforms, retain the regression approach—threshold optimization on continuous outputs o
    evidence: ✓ The present output activation or label formulation mismatches the target structure. | ✓ Available backbones differ in capacity or domain pretraining relevant to the task.
    leaderboard score 0.80353 → 0.79406 (higher is better; worse by 0.00947)
- expert 55621328 · learning · v89→v92   Implement ordinal regression inference: treat each output unit as a cumulative threshold probability, apply sigmoid, and sum across thresholds to produce a continuous score. Add an offset (+1) if the label scale starts above zero. Then apply the same optimized rounding post-processing. This preserve
    evidence: ✓ The present output activation or label formulation mismatches the target structure. | ✓ Available backbones differ in capacity or domain pretraining relevant to the task. | ✗ The tuned current tree method has plateaued and another boosting implementation is available. | ✓ A minimal or poorly matched prediction head limits an otherwise useful representation.
    leaderboard score 0.81590 → 0.82736 (higher is better; improved by 0.01146)
- expert 55621328 · learning · v102→v103   Train or obtain checkpoints using an ordinal prediction formulation and swap them into the inference pipeline. Compare leaderboard scores directly; if the ordinal variant matches or exceeds regression, iterate on checkpoint selection and blend weights within that formulation.
    evidence: ✓ Available backbones differ in capacity or domain pretraining relevant to the task. | ✗ The tuned current tree method has plateaued and another boosting implementation is available. | ✓ The present output activation or label formulation mismatches the target structure. | ✗ A generative model could score the text but its output reliability is unverified.
    leaderboard score 0.82366 → 0.82467 (higher is better; improved by 0.00101)
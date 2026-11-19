# Use an ordinal formulation  `T.5.4.2.4`   4 edits, 0 experts
3 scored cases, median improvement +0.00101, 2 improved


- expert 55621328 (Master) · learning · v30→v33   Implement a classification head that outputs softmax probabilities over ordinal classes and takes argmax. Compare its leaderboard score against the regression + optimized-rounding baseline. If classification underperforms, retain the regression approach—threshold optimization on continuous outputs o
    evidence: ✗ Targets are probability distributions and the evaluation uses distributional divergence. | ✗ Outputs are independent labels or bounded independent targets rather than mutually exclusive classes. | ✓ Labels occupy an ordered finite scale. | ✓ The metric rewards pair ordering while training uses only pointwise errors.
    leaderboard score 0.80353 → 0.79406 (-0.00947)
- expert 55621328 (Master) · learning · v89→v92   Implement ordinal regression inference: treat each output unit as a cumulative threshold probability, apply sigmoid, and sum across thresholds to produce a continuous score. Add an offset (+1) if the label scale starts above zero. Then apply the same optimized rounding post-processing. This preserve
    evidence: ✗ Targets are probability distributions and the evaluation uses distributional divergence. | ✓ Labels occupy an ordered finite scale. | ✗ Outputs are independent labels or bounded independent targets rather than mutually exclusive classes. | ✓ The metric rewards pair ordering while training uses only pointwise errors.
    leaderboard score 0.81590 → 0.82736 (+0.01146)
- expert 55621328 (Master) · learning · v90→v91   After summing the sigmoid outputs, add the minimum label value as an offset so the predicted range matches the target range. Verify this alignment before applying any rounding or threshold optimization, as a mismatch will silently degrade the metric.
    evidence: ✗ Targets are probability distributions and the evaluation uses distributional divergence. | ✓ Labels occupy an ordered finite scale.
    leaderboard score n/a → n/a
- expert 55621328 (Master) · learning · v102→v103   Train or obtain checkpoints using an ordinal prediction formulation and swap them into the inference pipeline. Compare leaderboard scores directly; if the ordinal variant matches or exceeds regression, iterate on checkpoint selection and blend weights within that formulation.
    evidence: ✗ Targets are probability distributions and the evaluation uses distributional divergence. | ✗ Outputs are independent labels or bounded independent targets rather than mutually exclusive classes. | ✓ Labels occupy an ordered finite scale.
    leaderboard score 0.82366 → 0.82467 (+0.00101)
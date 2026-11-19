# Choose probability-space or logit-space averaging  `T.5.2.4`   7 edits, 0 experts
6 scored cases (improvement signed by each competition's direction), median +0.00044, 5 improved


- expert 53747598 · hms · v15→v21   Export pre-softmax logits from each model, compute the weighted average in logit space, then apply softmax to obtain the final distribution. Compare this against probability-space averaging on the leaderboard. Logit-space averaging often yields a better-calibrated blend for log-based or divergence m
    evidence: ✓ The metric evaluates class distributions and logits or calibrated probabilities are available.
    leaderboard score 0.22838 → 0.22689 (lower is better; improved by 0.00149)
- expert 50376011 · hms · v112→v113   Apply the softmax (or other normalization) to each individual model's output before averaging across ensemble members, so that the ensemble operates in probability space. Verify by comparing leaderboard or validation scores against the alternative order, and keep whichever is better.
    evidence: ✓ The metric evaluates class distributions and logits or calibrated probabilities are available.
    leaderboard score 0.30121 → 0.30077 (lower is better; improved by 0.00044)
- expert 52551258 · hms · v3→v4   Always normalize averaged probability predictions to sum to 1 before submission when the metric is a divergence or log-likelihood. However, change only one thing at a time so the effect of normalization can be isolated from other modifications.
    evidence: ✓ The metric evaluates class distributions and logits or calibrated probabilities are available.
    leaderboard score 0.37116 → 0.37553 (lower is better; worse by 0.00437)
- expert 15164527 · ranzcr · v4→v5   Apply a concave power transform (exponent < 1, e.g., square root) to each model's predicted probabilities before the weighted blend. This spreads predictions away from 0/1, which can improve discrimination under AUC. Submit and compare; the gain is typically small, so verify it is consistent and not
    evidence: ✓ The metric uses ordering and members have incompatible score scales or outliers. | ✓ The metric evaluates class distributions and logits or calibrated probabilities are available.
    leaderboard score 0.96642 → 0.96679 (higher is better; improved by 0.00037)
- expert 15164527 · ranzcr · v6→v13   Try a concave power transform (exponent between 0.3 and 0.7) on each model's predictions before weighted averaging. If it helps, consider switching to rank-based averaging instead, which achieves a similar effect without needing to choose the exponent.
    evidence: ✓ Weight estimates are unstable or no independent out-of-fold predictions support fitting them. | ✓ The metric uses ordering and members have incompatible score scales or outliers. | ✓ The metric evaluates class distributions and logits or calibrated probabilities are available. | ✗ Sufficient cross-fitted predictions exist to learn a stable combination without leakage.
    leaderboard score 0.96755 → 0.96772 (higher is better; improved by 0.00018)
- expert 15203842 · ranzcr · v12→v13   Try a power-mean blend: raise each model's predictions to a fractional exponent (e.g., 0.5, i.e., square root) before averaging. This compresses high probabilities less and can better separate classes. Compare the leaderboard score against the simple average to decide whether to keep it.
    evidence: ✓ Weight estimates are unstable or no independent out-of-fold predictions support fitting them. | ✓ The metric uses ordering and members have incompatible score scales or outliers. | ✓ The metric evaluates class distributions and logits or calibrated probabilities are available. | ✗ Sufficient cross-fitted predictions exist to learn a stable combination without leakage.
    leaderboard score n/a → 0.96772 (higher is better)
- expert 50496431 · hms · v16→v17   Move TTA duplication, softmax, and averaging into the model's forward pass so that every inference call returns fully normalized, TTA-averaged probabilities. This ensures softmax is applied before averaging (averaging probabilities rather than logits) and eliminates mismatches between training and i
    evidence: ✓ The metric evaluates class distributions and logits or calibrated probabilities are available.
    leaderboard score 0.34815 → 0.34713 (lower is better; improved by 0.00102)
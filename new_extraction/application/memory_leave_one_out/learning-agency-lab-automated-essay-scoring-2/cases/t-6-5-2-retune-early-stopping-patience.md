# Retune early-stopping patience  `T.6.5.2`   2 edits, 0 experts
1 scored cases, median improvement +0.00000, 0 improved


- expert 27799930 (Contributor) · amex · v27→v29   When adding many new features, slightly tighten early stopping patience (e.g., reduce by ~20%) to guard against overfitting on noise. Re-evaluate after pruning unhelpful features; the combination of a cleaner feature set and appropriate patience often yields a larger gain than either change alone.
    evidence: none recorded
    leaderboard score n/a → 0.79350
- expert 27825577 (Expert) · amex · v11→v14   Sweep the early-stopping patience parameter across a range (e.g., halving and doubling the current value). When a lower learning rate is used, prefer a larger patience value to avoid premature stopping. If reducing patience degrades the score, revert to the larger value.
    evidence: ✓ Stopping occurs during noisy short plateaus, especially with a reduced learning rate.
    leaderboard score 0.79425 → 0.79425 (+0.00000)
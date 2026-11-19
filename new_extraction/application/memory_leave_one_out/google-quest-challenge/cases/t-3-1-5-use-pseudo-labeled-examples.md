# Use pseudo-labeled examples  `T.3.1.5`   3 edits, 0 experts
3 scored cases, median improvement -0.00304, 1 improved


- expert 49524919 (Grandmaster) · hms · v139→v142   First evaluate the pseudo-labeled model in isolation (disable other ensemble members) to measure its standalone quality. If it underperforms the existing ensemble substantially, sweeping checkpoint variants is unlikely to close the gap. Avoid blending it in until its standalone quality is competitiv
    evidence: ✓ Unlabeled in-domain data and a sufficiently reliable teacher are available.
    leaderboard score 0.23959 → 0.26137 (+0.02178)
- expert 52860091 (Grandmaster) · hms · v26→v27   Swap in the enhanced-training checkpoints for the second architecture and measure the ensemble score. Techniques that leverage unlabeled data or soft labels tend to generalize across architectures on the same task, so the upgrade is usually beneficial and worth testing early.
    evidence: ✓ Unlabeled in-domain data and a sufficiently reliable teacher are available.
    leaderboard score 0.26613 → 0.26010 (-0.00603)
- expert 52860091 (Grandmaster) · hms · v38→v43   Retrain the weak member using the same semi-supervised (pseudo-labeling) pipeline that benefited existing members. If pseudo-labeling consistently helped other architectures in the same competition, it is likely to help the new architecture as well, making it a viable ensemble component.
    evidence: ✓ Unlabeled in-domain data and a sufficiently reliable teacher are available.
    leaderboard score 0.25910 → 0.25606 (-0.00304)
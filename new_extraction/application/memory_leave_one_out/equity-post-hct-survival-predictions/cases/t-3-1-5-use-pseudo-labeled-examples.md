# Use pseudo-labeled examples  `T.3.1.5`   4 edits, 0 experts
4 scored cases (improvement signed by each competition's direction), median +0.00304, 2 improved


- expert 17616127 · commonlitreadabilityprize · v45→v49   First sanity-check a single fold/checkpoint to get a rough quality signal. Then average all available folds. Compare the averaged result against the current best. If the new checkpoints underperform even after fold-averaging, they are unlikely to help as a standalone replacement—consider blending th
    evidence: ✓ Unlabeled examples and a validated teacher are available. | ✗ Previous augmentation attempts beyond the current minimal setup degraded performance.
    leaderboard score 0.46489 → 0.47952 (lower is better; worse by 0.01463)
- expert 49524919 · hms · v139→v142   First evaluate the pseudo-labeled model in isolation (disable other ensemble members) to measure its standalone quality. If it underperforms the existing ensemble substantially, sweeping checkpoint variants is unlikely to close the gap. Avoid blending it in until its standalone quality is competitiv
    evidence: ✓ Unlabeled examples and a validated teacher are available.
    leaderboard score 0.23959 → 0.26137 (lower is better; worse by 0.02178)
- expert 52860091 · hms · v26→v27   Swap in the enhanced-training checkpoints for the second architecture and measure the ensemble score. Techniques that leverage unlabeled data or soft labels tend to generalize across architectures on the same task, so the upgrade is usually beneficial and worth testing early.
    evidence: ✓ Unlabeled examples and a validated teacher are available.
    leaderboard score 0.26613 → 0.26010 (lower is better; improved by 0.00603)
- expert 52860091 · hms · v38→v43   Retrain the weak member using the same semi-supervised (pseudo-labeling) pipeline that benefited existing members. If pseudo-labeling consistently helped other architectures in the same competition, it is likely to help the new architecture as well, making it a viable ensemble component.
    evidence: ✓ Unlabeled examples and a validated teacher are available. | ✓ Training overfits and label-preserving perturbations are supported by the input semantics.
    leaderboard score 0.25910 → 0.25606 (lower is better; improved by 0.00304)
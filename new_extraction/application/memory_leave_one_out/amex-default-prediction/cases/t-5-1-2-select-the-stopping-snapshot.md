# Select the stopping snapshot  `T.5.1.2`   4 edits, 0 experts
4 scored cases (improvement signed by each competition's direction), median +0.00501, 3 improved


- expert 52551258 · hms · v5→v7   Try checkpoints selected on the high-confidence validation subset (e.g., best score on samples with many annotator votes) rather than final-epoch or full-validation-best checkpoints. Ensure the output conversion (e.g., exponentiating log-probabilities) matches what the checkpoint was trained to prod
    evidence: ✓ Final-epoch and best-validation snapshots differ and late training may overfit. | ✓ Several nearby snapshots from the same parameterization are available. | ✓ The candidate snapshots come from different architectures or unrelated initializations.
    leaderboard score 0.37494 → 0.32513 (lower is better; improved by 0.04982)
- expert 55621328 · learning · v46→v47   Swap in last-epoch snapshots while keeping everything else fixed. If the score drops, prefer best-validation checkpoints; the gap indicates how much the model overfits in later epochs and whether early stopping is essential for this task.
    evidence: ✓ Final-epoch and best-validation snapshots differ and late training may overfit. | ✓ Several nearby snapshots from the same parameterization are available. | ✗ The candidate snapshots come from different architectures or unrelated initializations.
    leaderboard score 0.81880 → 0.81727 (higher is better; worse by 0.00153)
- expert 55621328 · learning · v103→v104   Try both checkpoint variants in the inference ensemble and compare scores. Final-epoch checkpoints can sometimes generalize better when the validation set distribution differs from the test set, so do not assume early stopping is always superior.
    evidence: ✓ Final-epoch and best-validation snapshots differ and late training may overfit. | ✗ The candidate snapshots come from different architectures or unrelated initializations.
    leaderboard score 0.82467 → 0.82726 (higher is better; improved by 0.00259)
- expert 50496431 · hms · v7→v8   Systematically try alternative checkpoint selections—varying which epoch or run is chosen per fold—and evaluate on the leaderboard or a held-out set. Even without changing the model or augmentation, checkpoint selection alone can yield a larger gain than adding TTA.
    evidence: ✓ Final-epoch and best-validation snapshots differ and late training may overfit. | ✓ Several nearby snapshots from the same parameterization are available. | ✗ The candidate snapshots come from different architectures or unrelated initializations.
    leaderboard score 0.42697 → 0.42196 (lower is better; improved by 0.00501)
# Train remaining folds across sessions  `T.7.8`   2 edits, 0 experts

- expert 7613444 (Contributor) · google · v7→v11   Train folds incrementally across separate runs by gating the CV loop to execute only untrained fold indices, saving model weights after each fold. In a final inference-only run, load all saved fold checkpoints, generate predictions from each, and average them. This decouples training cost from ensem
    evidence: ✓ The required fold training cannot finish within one session but completed checkpoints can be persisted.
    leaderboard score n/a → 0.39956
- expert 7613444 (Contributor) · google · v12→v14   Use a fold-index conditional inside the CV loop to skip already-completed folds and train only the remaining ones each session. Save each fold's weights to persistent storage. Across successive runs, widen the conditional to cover additional folds until all are trained, then switch to inference mode
    evidence: ✓ The required fold training cannot finish within one session but completed checkpoints can be persisted.
    leaderboard score 0.40047 → n/a
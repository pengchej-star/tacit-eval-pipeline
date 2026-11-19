# Train unfinished folds across sessions  `T.3.2.3`   2 edits, 0 experts

- expert 7613444 (Contributor) · google · v7→v11   Train folds incrementally across separate runs by gating the CV loop to execute only untrained fold indices, saving model weights after each fold. In a final inference-only run, load all saved fold checkpoints, generate predictions from each, and average them. This decouples training cost from ensem
    evidence: ✓ A session cannot finish all folds but completed fold checkpoints can be reused. | ✗ A reduced fold count was used as a temporary speed compromise for a slower algorithm and should be restored now that a faster algorithm is in use. | ✓ Memory is not being reclaimed between heavy stages, causing accumulation that could force restarts or OOM failures during iteration.
    leaderboard score n/a → 0.39956
- expert 7613444 (Contributor) · google · v12→v14   Use a fold-index conditional inside the CV loop to skip already-completed folds and train only the remaining ones each session. Save each fold's weights to persistent storage. Across successive runs, widen the conditional to cover additional folds until all are trained, then switch to inference mode
    evidence: ✓ A session cannot finish all folds but completed fold checkpoints can be reused.
    leaderboard score 0.40047 → n/a
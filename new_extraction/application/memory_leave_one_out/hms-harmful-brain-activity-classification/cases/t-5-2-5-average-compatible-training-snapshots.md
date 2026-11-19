# Average compatible training snapshots  `T.5.2.5`   1 edits, 0 experts

- expert 7573212 (Contributor) · google · v11→v13   Rather than selecting a single checkpoint, load both variants per fold, generate predictions from each, and average them into the ensemble. This exploits the diversity between checkpoints and often outperforms either alone.
    evidence: ✓ Several stopping-rule or training-stage snapshots have complementary errors.
    leaderboard score n/a → 0.39071
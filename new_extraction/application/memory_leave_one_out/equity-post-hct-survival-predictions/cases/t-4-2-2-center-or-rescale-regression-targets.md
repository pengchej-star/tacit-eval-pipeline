# Center or rescale regression targets  `T.4.2.2`   1 edits, 0 experts

- expert 58130512 (Master) · learning · v103→v105   Try per-fold target centering (subtract each fold's training mean, then average the fold means to reconstruct the global offset at inference). Compare validation metrics against the fixed global shift. If per-fold centering shows no improvement or adds instability, revert to the simpler fixed shift 
    evidence: ✓ Regression target location or scale varies across folds or poorly matches the model output range.
    leaderboard score 0.82432 → n/a
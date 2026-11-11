# Tune compressed text representations  `T.4.2.4`   1 edits, 0 experts

- expert 59253662 (Contributor) · learning · v10→v11   Fix the number of topics to a small explicit value rather than using automatic selection, so features are stable across train and test. Use locally cached embedding checkpoints to avoid download failures and ensure reproducibility. Adjust clustering granularity to roughly match the number of target 
    evidence: ✓ Sparse representations are large and latent topics or low-dimensional summaries are available.
    leaderboard score n/a → 0.78393
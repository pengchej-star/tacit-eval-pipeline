# Reduce per-member boosting duration  `T.6.3.5`   1 edits, 0 experts

- expert 73937748 · equity · v4→v5   Reduce each model's number of boosting rounds substantially (e.g., to roughly one-sixth of the standalone value) when ensembling multiple models, because the ensemble itself provides capacity. Reinvest the saved compute into more thorough blend-weight optimization (increase search trials proportiona
    evidence: ✓ Tree duration was tuned for a standalone model but it now contributes to a multi-model ensemble.
    leaderboard score n/a → 0.68705 (higher is better)
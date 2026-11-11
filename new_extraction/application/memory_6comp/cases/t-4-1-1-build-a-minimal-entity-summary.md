# Build a minimal entity summary  `T.4.1.1`   2 edits, 0 experts

- expert 27836972 (Expert) · amex · v2→v5   Start with the simplest possible aggregation (e.g., just the mean for numeric columns and count for categorical columns) to get an end-to-end working pipeline and a baseline score. Once that succeeds, incrementally add richer statistics (std, min, max, last value, nunique) one or two at a time, veri
    evidence: ✓ The current model uses raw repeated rows without an entity-level baseline. | ✓ Multiple observations exist but only one record per entity reaches the model. | ✗ Global summaries discard recency or the order of meaningful changes.
    leaderboard score n/a → 0.76283
- expert 27799930 (Contributor) · amex · v1→v11   Aggregate numeric columns with last/mean/std and categorical columns with last/count/nunique per entity. Drop columns with very high missingness, fill remaining NaNs, implement the competition metric as a custom evaluation function, and run stratified k-fold CV. Collect out-of-fold predicted probabi
    evidence: ✗ The current model uses raw repeated rows without an entity-level baseline. | ✗ Multiple observations exist but only one record per entity reaches the model. | ✓ Global summaries discard recency or the order of meaningful changes.
    leaderboard score n/a → n/a
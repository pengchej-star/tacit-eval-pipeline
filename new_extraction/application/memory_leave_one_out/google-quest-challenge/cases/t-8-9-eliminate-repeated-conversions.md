# Eliminate repeated conversions  `T.8.9`   1 edits, 0 experts

- expert 27836972 · amex · v64→v67   Convert the entire dataframe to CPU once before the loop rather than per group. Within each group, precompute the minimal slice needed (e.g., last N rows) and apply the transformation once, then extract per-column values from the precomputed result instead of recomputing per column.
    evidence: ✓ Profiling or loop inspection shows the same conversion or transformation repeats for each group or column.
    leaderboard score n/a → 0.79497 (higher is better)
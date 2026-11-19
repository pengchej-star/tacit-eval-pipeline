# Replace a slow computation with an equivalent implementation  `T.7.5`   2 edits, 0 experts

- expert 27836972 (Expert) · amex · v64→v67   Convert the entire dataframe to CPU once before the loop rather than per group. Within each group, precompute the minimal slice needed (e.g., last N rows) and apply the transformation once, then extract per-column values from the precomputed result instead of recomputing per column.
    evidence: ✓ Profiling identifies a computational kernel whose output can be checked independently.
    leaderboard score n/a → 0.79497
- expert 49576186 (Expert) · hms · v140→v149   When porting a CPU signal-processing step to a GPU library, have the CPU fallback ready and test the GPU path in isolation first. If the GPU call requires more than one fix iteration, fall back to the CPU version immediately to avoid wasting submission attempts on infrastructure bugs rather than mod
    evidence: ✓ Profiling identifies a computational kernel whose output can be checked independently. | ✓ Repeated manual path, flag, or member-list edits cause configuration drift.
    leaderboard score 0.38984 → n/a
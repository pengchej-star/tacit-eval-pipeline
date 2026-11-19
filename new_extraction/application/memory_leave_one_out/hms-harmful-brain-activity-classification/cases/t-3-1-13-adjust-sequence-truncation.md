# Adjust sequence truncation  `T.3.1.13`   1 edits, 0 experts

- expert 17616127 · commonlitreadabilityprize · v9→v10   Test changing the random seed and increasing the maximum token length at inference. Expect minimal impact: seed affects only stochastic elements (e.g., dropout if left on), and longer tokens help only if inputs were being truncated. If the gap to the ensemble persists, return to ensembling rather th
    evidence: ✓ A meaningful fraction of task-relevant text is truncated.
    leaderboard score n/a → 0.48130 (lower is better)
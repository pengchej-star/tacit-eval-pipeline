# Adjust sequence truncation  `T.4.2.3`   1 edits, 0 experts

- expert 17616127 · commonlitreadabilityprize · v9→v10   Test changing the random seed and increasing the maximum token length at inference. Expect minimal impact: seed affects only stochastic elements (e.g., dropout if left on), and longer tokens help only if inputs were being truncated. If the gap to the ensemble persists, return to ensembling rather th
    evidence: ✓ A meaningful fraction of inputs loses potentially relevant content to truncation. | ✓ The model is fixed and no checkpoint was trained for the proposed new prompt or vocabulary. | ✓ The text-input modification has only been tested with one checkpoint and its effect may be checkpoint-dependent.
    leaderboard score n/a → 0.48130 (lower is better)
# Change retained text context  `T.4.4.1`   2 edits, 0 experts

- expert 17616127 · commonlitreadabilityprize · v9→v10   Test changing the random seed and increasing the maximum token length at inference. Expect minimal impact: seed affects only stochastic elements (e.g., dropout if left on), and longer tokens help only if inputs were being truncated. If the gap to the ensemble persists, return to ensembling rather th
    evidence: ✓ Relevant text lies outside the retained token range or is diluted by unrelated spans.
    leaderboard score n/a → 0.48130 (lower is better)
- expert 7018718 · google · v20→v25   Toggle the preprocessing feature on and off across multiple saved checkpoints and compare leaderboard scores. If the effect is inconsistent across checkpoints (sometimes positive, sometimes negative), the preprocessing is likely interacting with training-time conditions and should only be used with 
    evidence: ✓ Relevant text lies outside the retained token range or is diluted by unrelated spans. | ✓ The pretrained checkpoint was trained on single-sequence input, so switching to paired encoding at inference creates a train/inference mismatch.
    leaderboard score n/a → 0.38272 (higher is better)
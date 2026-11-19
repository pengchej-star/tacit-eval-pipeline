# Test class-specific blend weights  `T.7.3.6`   1 edits, 0 experts

- expert 49524919 (Grandmaster) · hms · v58→v60   Start with a global blend that heavily favors the stronger model (e.g., 80/20). Then try per-class weight adjustments, shifting weight toward whichever model is relatively better for each class. Evaluate each change on the leaderboard or a reliable validation set. If per-class tuning shows no clear 
    evidence: ✓ Component quality differs reproducibly or a member’s predictions have changed since weights were tuned. | ✗ Members have comparable quality and tuned weights have not reliably improved the simple average.
    leaderboard score 0.29199 → n/a
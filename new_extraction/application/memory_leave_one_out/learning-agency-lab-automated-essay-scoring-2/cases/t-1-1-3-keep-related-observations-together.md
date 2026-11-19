# Keep related observations together  `T.1.1.3`   2 edits, 0 experts
1 scored cases, median improvement -0.01026, 0 improved


- expert 27656049 (Expert) · amex · v7→v8   Aggregate to one row per entity before entering the CV loop. This ensures stratified splits operate on the correct unit, prevents data leakage from the same entity appearing in both train and validation folds, and reduces memory and compute inside the loop.
    evidence: ✓ Several rows or overlapping windows belong to the same prediction entity. | ✗ Local and public scores have ranked existing checkpoints differently. | ✓ The expert lacks local cross-validation infrastructure to rank checkpoints without relying on the noisy public leaderboard.
    leaderboard score n/a → 0.78584
- expert 49576186 (Expert) · hms · v123→v125   Try pure group-based splitting (without stratification) alongside the stratified variant and compare leaderboard or held-out scores. When labels are noisy or soft, pure grouping may generalize better because it avoids artificially balancing uncertain labels.
    evidence: ✓ Several rows or overlapping windows belong to the same prediction entity. | ✓ Multiple recent versions have not been submitted to the leaderboard, making submission budget conservation relevant.
    leaderboard score 0.27887 → 0.26861 (-0.01026)
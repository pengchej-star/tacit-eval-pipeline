# Coarsen continuous features  `T.4.4.6`   2 edits, 0 experts
1 scored cases, median improvement +0.00083, 1 improved


- expert 27836972 (Expert) · amex · v21→v25   Round continuous features to a small number of decimal places, replace the originals, and evaluate on the leaderboard or validation set. Expect only a marginal gain; treat it as a low-effort addition rather than a major lever.
    evidence: ✓ Fine numerical variation appears noisy relative to meaningful feature resolution. | ✓ One recently added or removed feature block has uncertain marginal value.
    leaderboard score n/a → 0.79366
- expert 27502740 (Grandmaster) · amex · v5→v6   Before training, upcast low-precision float columns to a higher-precision type, round to a fixed number of decimal places that preserves meaningful variation, then cast back. Apply identically to train and test. Verify on the leaderboard that the rounding level chosen does not discard useful signal.
    evidence: ✓ The learner supports missing values and is insensitive to feature scaling. | ✓ Fine numerical variation appears noisy relative to meaningful feature resolution.
    leaderboard score 0.79418 → 0.79501 (+0.00083)
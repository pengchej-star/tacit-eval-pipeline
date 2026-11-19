# Adjust numeric representation  `T.3.4.4.2`   3 edits, 0 experts
1 scored cases, median improvement +0.00083, 1 improved


- expert 27836972 (Expert) · amex · v21→v25   Round continuous features to a small number of decimal places, replace the originals, and evaluate on the leaderboard or validation set. Expect only a marginal gain; treat it as a low-effort addition rather than a major lever.
    evidence: ✓ Numeric range, resolution, or precision may suppress useful distinctions.
    leaderboard score n/a → 0.79366
- expert 27502740 (Grandmaster) · amex · v5→v6   Before training, upcast low-precision float columns to a higher-precision type, round to a fixed number of decimal places that preserves meaningful variation, then cast back. Apply identically to train and test. Verify on the leaderboard that the rounding level chosen does not discard useful signal.
    evidence: ✓ Numeric range, resolution, or precision may suppress useful distinctions.
    leaderboard score 0.79418 → 0.79501 (+0.00083)
- expert 28093671 (Contributor) · amex · v34→v37   Try disabling scaling, outlier filtering, and manual imputation for tree-based models. Validate on the leaderboard or holdout. If the score improves or stays the same, keep the simpler pipeline. Only re-add such steps if there is clear evidence they help.
    evidence: ✓ Missing or non-finite values reach a learner with a known missing-value policy. | ✓ Numeric range, resolution, or precision may suppress useful distinctions.
    leaderboard score n/a → 0.79304
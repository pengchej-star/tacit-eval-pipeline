# Test numeric preprocessing against native handling  `T.3.1.10`   9 edits, 0 experts
5 scored cases, median improvement +0.00016, 4 improved


- expert 27836972 (Expert) · amex · v12→v16   Start by leaving NaNs for the tree model to handle natively. Only add explicit imputation if validation shows it helps. Aggregation-induced NaNs (e.g., std with one row) often carry information (small group size), so preserving them as missing is a reasonable default.
    evidence: ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score n/a → n/a
- expert 27836972 (Expert) · amex · v21→v25   Round continuous features to a small number of decimal places, replace the originals, and evaluate on the leaderboard or validation set. Expect only a marginal gain; treat it as a low-effort addition rather than a major lever.
    evidence: ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score n/a → 0.79366
- expert 27502740 (Grandmaster) · amex · v5→v6   Before training, upcast low-precision float columns to a higher-precision type, round to a fixed number of decimal places that preserves meaningful variation, then cast back. Apply identically to train and test. Verify on the leaderboard that the rounding level chosen does not discard useful signal.
    evidence: ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score 0.79418 → 0.79501 (+0.00083)
- expert 28093671 (Contributor) · amex · v26→v28   Rewrite the full pipeline from scratch in one pass: proper missing-value imputation (e.g., median), systematic per-entity aggregation features (last, mean, std), standard scaling, cross-validated training with the competition metric, and correct fold-averaged inference. A clean rebuild can yield a l
    evidence: ✓ Several observations belong to one prediction entity and only a small summary is currently used. | ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score n/a → 0.70811
- expert 28093671 (Contributor) · amex · v34→v37   Try disabling scaling, outlier filtering, and manual imputation for tree-based models. Validate on the leaderboard or holdout. If the score improves or stays the same, keep the simpler pipeline. Only re-add such steps if there is clear evidence they help.
    evidence: ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score n/a → 0.79304
- expert 28093671 (Contributor) · amex · v39→v40   When using a tree-based model that handles NaNs natively, try leaving NaNs as-is rather than imputing with a constant. Compare validation or leaderboard scores with and without imputation; if removing imputation improves the score, keep NaNs for the model to handle.
    evidence: ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score 0.78971 → 0.79361 (+0.00391)
- expert 17371717 (Master) · commonlitreadabilityprize · v1→v2   Replace manual preprocessing with the library's native parameter. Submit or validate to confirm the output is equivalent or better, establishing a clean baseline before making architectural changes.
    evidence: ✓ A cleaning or tokenization rule changes information relevant to the target or checkpoint. | ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score 0.47570 → 0.47570 (+0.00000)
- expert 75145694 (Expert) · equity · v34→v35   Make the feature-generation function model-aware by accepting a model identifier and branching on it: apply the imputation strategy each model family expects (e.g., sentinel value for tree models that lack native NaN support, median/mean for others). This ensures every ensemble member receives corre
    evidence: ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score 0.69296 → 0.69312 (+0.00016)
- expert 73937748 (Master) · equity · v12→v13   Try disabling standard scaling of numeric features when the pipeline uses only tree-based models. If the score stays the same or improves, remove scaling permanently to simplify the pipeline.
    evidence: ✓ Current numeric preprocessing may erase missingness or impose transformations the learner does not need.
    leaderboard score 0.68793 → 0.68805 (+0.00012)
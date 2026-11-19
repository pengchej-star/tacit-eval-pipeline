# Normalize member scales before blending  `T.5.3.5`   3 edits, 0 experts
1 scored cases, median improvement +0.00023, 1 improved


- expert 75584724 (Master) · equity · v8→v11   Test with and without standardization of the meta-features (fit scaler on out-of-fold predictions, apply to test). Compare leaderboard or validation scores for both settings. If the difference is negligible or negative, keep raw predictions—ranking-based metrics are invariant to monotone transforms 
    evidence: ✓ Member scales or outliers distort their intended relative contributions. | ✓ Enough OOF examples exist to learn stable complementary relationships among base outputs. | ✓ Member scales differ or raw versus rank aggregation has changed preference across configurations.
    leaderboard score n/a → 0.69408
- expert 75584724 (Master) · equity · v12→v13   Try a median-and-IQR-based scaler (robust to outliers) instead of a mean-and-variance scaler for normalizing individual model predictions before weight optimization. Compare leaderboard or validation scores to confirm the benefit.
    evidence: ✓ Member scales or outliers distort their intended relative contributions.
    leaderboard score 0.69376 → 0.69399 (+0.00023)
- expert 73671444 (Grandmaster) · equity · v16→v18   Do not submit immediately after adding a new model family. First ensure consistent preprocessing, prediction ranking, and postprocessing across all families. An initial score drop from naïve integration often reverses once the blending pipeline is standardized, as the diversity benefit only material
    evidence: ✓ Member scales differ or raw versus rank aggregation has changed preference across configurations. | ✓ Member scales or outliers distort their intended relative contributions.
    leaderboard score 0.68639 → n/a
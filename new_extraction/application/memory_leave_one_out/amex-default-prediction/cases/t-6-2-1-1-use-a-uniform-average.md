# Use a uniform average  `T.6.2.1.1`   11 edits, 0 experts
5 scored cases, median improvement -0.00038, 2 improved


- expert 17616127 (Contributor) · commonlitreadabilityprize · v17→v18   Start with equal-weight averaging for fold-based members (similar expected quality). If members vary in validation performance, optimize weights on a held-out set or use a meta-learner. Always compare the chosen aggregation against the previous best before finalizing.
    evidence: ✓ Members have comparable held-out quality and weight tweaks have not generalized. | ✗ Members differ consistently in quality and aligned held-out predictions are available. | ✓ The dataset is small and fitted coefficients vary sharply across folds.
    leaderboard score n/a → 0.48999
- expert 17616127 (Contributor) · commonlitreadabilityprize · v64→v65   Test equal-weight averaging as a baseline. If it underperforms the tuned blend by a meaningful margin relative to the leaderboard granularity, invest in weight optimization (e.g., grid search or CV-based optimization) rather than defaulting to uniform weights.
    evidence: ✓ Members have comparable held-out quality and weight tweaks have not generalized. | ✓ The dataset is small and fitted coefficients vary sharply across folds.
    leaderboard score n/a → 0.45576
- expert 17616127 (Contributor) · commonlitreadabilityprize · v67→v68   Fall back to a simple equal-weight average of the strongest individual base models. When a complex stacking approach degrades performance, simplify first to re-establish a strong baseline, then add complexity incrementally.
    evidence: ✓ Members have comparable held-out quality and weight tweaks have not generalized. | ✓ The dataset is small and fitted coefficients vary sharply across folds.
    leaderboard score 0.46804 → n/a
- expert 18837555 (Expert) · commonlitreadabilityprize · v5→v6   Reset to a simple equal-weight average when adding new members, then re-optimize weights if needed. Equal averaging is a robust default that avoids overfitting blend weights on a small validation set.
    evidence: ✓ The dataset is small and fitted coefficients vary sharply across folds.
    leaderboard score 0.46041 → n/a
- expert 18837555 (Expert) · commonlitreadabilityprize · v12→v13   Start with equal-weight (simple mean) averaging when adding a new member. Only deviate from equal weights if cross-validation on a sufficiently large held-out set clearly supports it; on small or noisy data, equal weighting is a robust default that avoids overfitting the blend coefficients.
    evidence: ✓ Members have comparable held-out quality and weight tweaks have not generalized. | ✓ The dataset is small and fitted coefficients vary sharply across folds.
    leaderboard score 0.45714 → 0.45676 (-0.00038)
- expert 18350823 (Expert) · commonlitreadabilityprize · v30→v31   Test equal weights as a baseline, but expect that when component models differ in quality, asymmetric weights favoring stronger components will outperform. If equal weighting hurts, revert to the tuned weights and only adjust incrementally around the best-known values.
    evidence: ✓ Members have comparable held-out quality and weight tweaks have not generalized. | ✓ The dataset is small and fitted coefficients vary sharply across folds.
    leaderboard score 0.45931 → 0.45968 (+0.00036)
- expert 7573212 (Contributor) · google · v7→v8   Revert to equal-weight averaging and redirect effort to a different improvement lever (e.g., output post-processing or model diversity) rather than continuing to search over blend weights without reliable validation signal.
    evidence: ✓ Members have comparable held-out quality and weight tweaks have not generalized.
    leaderboard score 0.37898 → n/a
- expert 53747598 (Master) · hms · v28→v30   Start with equal weighting between the old and new components rather than keeping extreme weights. Equal weighting is a safer default when relative quality is unknown, and can be refined afterward based on leaderboard or validation feedback.
    evidence: ✗ Members differ consistently in quality and aligned held-out predictions are available. | ✓ The dataset is small and fitted coefficients vary sharply across folds. | ✓ Members have comparable held-out quality and weight tweaks have not generalized.
    leaderboard score n/a → 0.22587
- expert 15372370 (Expert) · ranzcr · v5→v6   Start with equal weights and keep test-time augmentation on. Only shift to non-uniform weights when per-model validation scores clearly justify it; arbitrary weighting and removing augmentation can hurt. If the weighted version scores worse on the leaderboard, revert to uniform averaging.
    evidence: ✗ Members differ consistently in quality and aligned held-out predictions are available.
    leaderboard score 0.96726 → 0.96670 (-0.00056)
- expert 15372370 (Expert) · ranzcr · v6→v7   Switch to simple (equal-weight) averaging of predictions across all folds of a single cross-validation run. Fold-averaging is more stable because the models share the same architecture and training recipe, reducing the risk of miscalibrated blend weights.
    evidence: ✓ Members have comparable held-out quality and weight tweaks have not generalized.
    leaderboard score 0.96670 → 0.96804 (+0.00135)
- expert 50496431 (Grandmaster) · hms · v101→v104   Reset to a simple equal-weight (mean) ensemble as a stable baseline. Then upgrade or swap individual members one at a time, re-adding each only after confirming it improves the mean blend. This isolates each member's contribution without introducing fragile weight tuning.
    evidence: ✓ Members have comparable held-out quality and weight tweaks have not generalized. | ✓ The dataset is small and fitted coefficients vary sharply across folds.
    leaderboard score 0.27434 → 0.27115 (-0.00318)
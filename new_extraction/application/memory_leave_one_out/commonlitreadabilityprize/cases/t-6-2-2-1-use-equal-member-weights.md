# Use equal member weights  `T.6.2.2.1`   3 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00318, 2 improved


- expert 7573212 · google · v7→v8   Revert to equal-weight averaging and redirect effort to a different improvement lever (e.g., output post-processing or model diversity) rather than continuing to search over blend weights without reliable validation signal.
    evidence: ✓ Tuned weights fail to beat equal averaging beyond repeated-evaluation uncertainty. | ✓ Only a small public score sample supports highly specific member or class weights.
    leaderboard score 0.37898 → n/a (higher is better)
- expert 15372370 · ranzcr · v6→v7   Switch to simple (equal-weight) averaging of predictions across all folds of a single cross-validation run. Fold-averaging is more stable because the models share the same architecture and training recipe, reducing the risk of miscalibrated blend weights.
    evidence: ✓ Tuned weights fail to beat equal averaging beyond repeated-evaluation uncertainty. | ✓ A member was upgraded or its prediction scale changed after weights were selected. | ✓ Only a small public score sample supports highly specific member or class weights.
    leaderboard score 0.96670 → 0.96804 (higher is better; improved by 0.00135)
- expert 50496431 · hms · v101→v104   Reset to a simple equal-weight (mean) ensemble as a stable baseline. Then upgrade or swap individual members one at a time, re-adding each only after confirming it improves the mean blend. This isolates each member's contribution without introducing fragile weight tuning.
    evidence: ✓ Members differ substantially in quality and a small contribution from a complementary weaker member helps. | ✓ Tuned weights fail to beat equal averaging beyond repeated-evaluation uncertainty. | ✓ Only a small public score sample supports highly specific member or class weights. | ✓ A member was upgraded or its prediction scale changed after weights were selected.
    leaderboard score 0.27434 → 0.27115 (lower is better; improved by 0.00318)
# Bound blend-search effort  `T.6.5`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00007, 1 improved


- expert 73937748 · equity · v21→v23   Start with a moderate trial budget and double it once. If the leaderboard score does not improve or drops, the original budget is sufficient and further search is overfitting to the OOF metric. Keep the smaller budget and consider regularized alternatives (e.g., ridge stacking) that are less prone t
    evidence: ✓ A blend optimizer is the dominant iteration cost and its gains plateau as trials increase. | ✓ Members have not been ablated or unused complementary checkpoints exist.
    leaderboard score 0.69032 → 0.68864 (higher is better; worse by 0.00168)
- expert 73937748 · equity · v63→v64   Double the trial budget and check whether the leaderboard or validation score improves meaningfully. If the gain is negligible (order of noise), revert or freeze the budget to save compute; consider skipping the tuning step entirely and using a fixed default.
    evidence: ✓ A blend optimizer is the dominant iteration cost and its gains plateau as trials increase.
    leaderboard score 0.69305 → 0.69312 (higher is better; improved by 0.00007)
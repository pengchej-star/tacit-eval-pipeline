# Compare feature-ranking methods  `T.3.2.3`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00071, 1 improved


- expert 27656049 · amex · v17→v18   Test both importance sources on the same pipeline and compare leaderboard or validation scores. If the more expensive attribution method yields a better feature subset, keep it despite the extra computation cost. Change only the selection method in isolation to avoid confounding with other hyperpara
    evidence: ✓ Available importance methods disagree about which features to retain.
    leaderboard score 0.79071 → 0.79056 (higher is better; worse by 0.00015)
- expert 27656049 · amex · v18→v19   Revert to the previously validated feature-selection method. When two approaches have been compared across multiple submissions and one consistently scores higher, treat it as the default and only revisit the alternative if the pipeline changes substantially.
    evidence: ✓ Available importance methods disagree about which features to retain.
    leaderboard score 0.79056 → 0.79127 (higher is better; improved by 0.00071)
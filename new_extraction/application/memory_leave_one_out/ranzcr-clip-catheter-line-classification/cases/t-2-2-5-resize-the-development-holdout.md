# Resize the development holdout  `T.2.2.5`   1 edits, 0 experts
1 scored cases, median improvement -0.00018, 0 improved


- expert 29588171 (Master) · amex · v37→v40   Try a small holdout (e.g., 10%) versus a large one (e.g., 40%). If the leaderboard score improves with the smaller holdout, keep it: the extra training data outweighs the value of a more precise local validation estimate when the model is only a minor blend component.
    evidence: ✓ A large fixed holdout removes training examples without changing model selection decisions. | ✓ Examples are approximately independent and no source shift or target-stratum imbalance requires a specialized split.
    leaderboard score 0.79961 → 0.79943 (-0.00018)
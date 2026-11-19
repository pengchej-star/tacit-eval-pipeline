# Tune neural regularization  `T.6.2.3`   2 edits, 0 experts
2 scored cases, median improvement +0.00030, 1 improved


- expert 18350823 (Expert) · commonlitreadabilityprize · v1→v2   Apply multisample dropout: run several independent dropout masks on the head's output and average them during both training and inference. Combine this with proper weight initialization (e.g., Xavier/normal) and layer normalization on the added head layers. Reduce inference batch size if memory allo
    evidence: ✓ Training improves while held-out performance degrades on a small labeled dataset. | ✓ Multiple hyperparameters were changed simultaneously in a previous edit, so individual effects are confounded and need isolated testing.
    leaderboard score 0.46275 → 0.46275 (-0.00000)
- expert 7613444 (Contributor) · google · v5→v6   Add dropout layers to each branch's classification head between the pooled representation and the output layer. Expect a small but consistent improvement; verify on the held-out metric before combining with other changes.
    evidence: ✓ Training improves while held-out performance degrades on a small labeled dataset. | ✗ Multiple hyperparameters were changed simultaneously in a previous edit, so individual effects are confounded and need isolated testing.
    leaderboard score 0.39802 → 0.39832 (+0.00030)
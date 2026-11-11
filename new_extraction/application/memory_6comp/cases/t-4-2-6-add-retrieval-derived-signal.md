# Add retrieval-derived signal  `T.4.2.6`   2 edits, 0 experts
2 scored cases, median improvement +0.04445, 2 improved


- expert 17616127 (Contributor) · commonlitreadabilityprize · v125→v130   Implement a retrieval feature generator that encodes texts with a pretrained bi-encoder, finds top-k nearest training examples, and uses their labels as features for the meta-learner. Compare the new ensemble score against the baseline. If the retrieval-augmented version scores worse, keep the origi
    evidence: ✓ Related labeled texts or auxiliary predictions can provide information absent from current features. | ✗ The current representation has lexical features but little contextual semantic information.
    leaderboard score 0.44825 → 0.45693 (+0.00868)
- expert 52551258 (Expert) · hms · v7→v9   Test the complex variant on the leaderboard. If it scores worse, revert promptly. Do not assume added complexity helps; treat it as a probe and keep the simpler model as the default unless the complex one clearly wins.
    evidence: ✓ Related labeled texts or auxiliary predictions can provide information absent from current features.
    leaderboard score 0.32513 → 0.36957 (+0.04445)
# Replace a weak baseline with a coherent pipeline  `T.2.1.8`   1 edits, 0 experts
1 scored cases, median improvement -0.28680, 0 improved


- expert 52551258 (Expert) · hms · v2→v3   When the gap to competitive performance is large and multiple improvements are each strongly motivated by domain knowledge or known solutions, bundle them into a single refactor. Verify the combined effect on the leaderboard. Reserve incremental ablation for later fine-tuning once the score is in a 
    evidence: ✓ Several factors changed in the same scored run. | ✗ A recent change caused a large regression and a verified earlier configuration is recoverable. | ✗ Repeated nearby settings fail to improve beyond the measured noise level. | ✗ No complete and scored end-to-end baseline exists. | ✓ The current baseline is far behind existing evidence and several coupled improvements form a compatible replacement.
    leaderboard score 0.65796 → 0.37116 (-0.28680)
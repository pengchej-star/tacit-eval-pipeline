# Bracket a bounded search  `T.1.3.4`   2 edits, 0 experts
1 scored cases, median improvement +0.00790, 1 improved


- expert 27389424 (Grandmaster) · amex · v37→v42   Start from the current value, step in one direction until validation worsens, then reverse and step past the starting point in the other direction. Keep step sizes moderate (e.g., halving or doubling the parameter). Change only the one parameter per run to isolate its effect. Be prepared to re-sweep
    evidence: ✗ The last score change followed several simultaneous functional edits. | ✓ A reproducible parameter trend exists but the optimum has not been bracketed. | ✗ No complete pipeline has yet produced a scored prediction file.
    leaderboard score n/a → n/a
- expert 17371717 (Master) · commonlitreadabilityprize · v33→v36   Run a small factorial sweep changing one or two factors per submission. Track the leaderboard score for each combination and select the configuration that yields the best metric. Keep the number of changes per submission small enough to attribute score movements to specific factors.
    evidence: ✗ No complete pipeline has yet produced a scored prediction file. | ✓ The last score change followed several simultaneous functional edits. | ✓ A reproducible parameter trend exists but the optimum has not been bracketed. | ✗ The latest configuration is substantially worse than a reproducible saved baseline. | ✗ The first baseline is far below existing scored alternatives and several compatible missing components are already evidenced.
    leaderboard score 0.46357 → 0.47147 (+0.00790)
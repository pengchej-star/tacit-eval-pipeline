# Replace unstable adaptive weights  `T.7.3.5`   1 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00033, 1 improved


- expert 18350823 · commonlitreadabilityprize · v9→v12   Prefer simple fixed blend weights over adaptive/conditional schemes. Test the adaptive approach, but if it does not clearly improve the score, revert to fixed weights. On tiny evaluation sets, the noise from adaptive selection typically outweighs any benefit.
    evidence: ✓ Current weights depend on statistics of a very small or varying inference sample.
    leaderboard score 0.46308 → 0.46275 (lower is better; improved by 0.00033)
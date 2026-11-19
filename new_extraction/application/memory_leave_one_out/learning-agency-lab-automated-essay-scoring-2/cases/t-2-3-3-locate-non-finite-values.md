# Locate non-finite values  `T.2.3.3`   1 edits, 0 experts
1 scored cases, median improvement +0.00010, 1 improved


- expert 75145694 (Expert) · equity · v66→v67   Add explicit NaN/Inf checks on both inputs and intermediate outputs at each pipeline stage. Replace missing values with a safe sentinel before feeding data to the network. Use stable weight initialization schemes. Insert runtime warnings that fire when any tensor contains non-finite values, so probl
    evidence: ✓ Inputs or intermediate network outputs contain non-finite values.
    leaderboard score 0.69348 → 0.69358 (+0.00010)
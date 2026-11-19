# Choose model-aware imputation  `T.4.1.1`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00016, 2 improved


- expert 75145694 · equity · v34→v35   Make the feature-generation function model-aware by accepting a model identifier and branching on it: apply the imputation strategy each model family expects (e.g., sentinel value for tree models that lack native NaN support, median/mean for others). This ensures every ensemble member receives corre
    evidence: ✓ A selected learner receives NaN or infinite values it cannot handle natively. | ✗ All downstream learners are trees and standardization adds no demonstrated signal.
    leaderboard score 0.69296 → 0.69312 (higher is better; improved by 0.00016)
- expert 75145694 · equity · v66→v67   Add explicit NaN/Inf checks on both inputs and intermediate outputs at each pipeline stage. Replace missing values with a safe sentinel before feeding data to the network. Use stable weight initialization schemes. Insert runtime warnings that fire when any tensor contains non-finite values, so probl
    evidence: ✓ A selected learner receives NaN or infinite values it cannot handle natively. | ✗ All downstream learners are trees and standardization adds no demonstrated signal.
    leaderboard score 0.69348 → 0.69358 (higher is better; improved by 0.00010)
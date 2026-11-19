# Blend different target encodings  `T.6.1.3.4`   6 edits, 0 experts
4 scored cases (improvement signed by each competition's direction), median +0.00022, 2 improved


- expert 75584724 · equity · v2→v3   Introduce additional target-transformation variants (e.g., rank-based or nonlinear monotone transforms of the survival target) into the pipeline configuration for each model family. Run each new variant through the same cross-validation and include its predictions in the ensemble candidate pool.
    evidence: ✓ The outcome admits distinct valid target encodings with different residual patterns.
    leaderboard score n/a → n/a (higher is better)
- expert 73671444 · equity · v11→v16   Test each target-transformation variant solo to rank them, then blend the top variants together. Even a variant that is weaker solo can improve the ensemble if its target transformation captures different aspects of the outcome. Include two or three diverse transformations rather than duplicating th
    evidence: ✓ The outcome admits distinct valid target encodings with different residual patterns.
    leaderboard score 0.68643 → 0.68639 (higher is better; worse by 0.00004)
- expert 73671444 · equity · v27→v30   Prioritize adding models trained on a different transformation of the survival target (e.g., cumulative hazard vs. log-probability vs. log-time) rather than adding another model of the same family on the same target. After each addition, rebalance blend weights and submit; keep the member only if th
    evidence: ✓ The outcome admits distinct valid target encodings with different residual patterns. | ✓ Current members use similar algorithms and have strongly correlated held-out residuals.
    leaderboard score 0.69303 → 0.69413 (higher is better; improved by 0.00110)
- expert 75924487 · equity · v5→v6   Train the same model type multiple times, each with a different target transformation, generate out-of-fold and test predictions from each, and add all as candidate columns for a stacking or blending ensembler. This increases diversity cheaply because only the label encoding changes, not the feature
    evidence: ✓ The outcome admits distinct valid target encodings with different residual patterns.
    leaderboard score n/a → 0.69331 (higher is better)
- expert 75145694 · equity · v3→v4   Create multiple regression targets from the same survival data using distinct statistical transforms of the censored outcome. Train separate base models on each target variant and blend their predictions. Even small per-model gains compound when the transforms are sufficiently decorrelated.
    evidence: ✓ The outcome admits distinct valid target encodings with different residual patterns.
    leaderboard score 0.68865 → 0.68888 (higher is better; improved by 0.00022)
- expert 73937748 · equity · v11→v12   When multiplying ensemble members by crossing model families with target transformations, monitor the blended score carefully. A large jump in member count can dilute strong models with mediocre ones, lowering the overall score. Add variants incrementally and validate each addition's marginal contri
    evidence: ✓ Current members use similar algorithms and have strongly correlated held-out residuals. | ✓ The outcome admits distinct valid target encodings with different residual patterns.
    leaderboard score 0.68948 → 0.68793 (higher is better; worse by 0.00155)
# Add a different target encoding  `T.7.2.3`   9 edits, 0 experts
5 scored cases, median improvement +0.00022, 3 improved


- expert 75584724 (Master) · equity · v2→v3   Introduce additional target-transformation variants (e.g., rank-based or nonlinear monotone transforms of the survival target) into the pipeline configuration for each model family. Run each new variant through the same cross-validation and include its predictions in the ensemble candidate pool.
    evidence: ✓ Different valid outcome transforms produce complementary residuals for the same task.
    leaderboard score n/a → n/a
- expert 75584724 (Master) · equity · v3→v6   Expand the pool by varying three axes independently: (1) the model family (different gradient-boosting implementations, neural networks), (2) the target transformation applied before training, and (3) the feature-engineering pipeline (with/without). Collect out-of-fold predictions from each variant 
    evidence: ✓ Different valid outcome transforms produce complementary residuals for the same task. | ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ An available modality, feature set, or preprocessing variant is absent from current members.
    leaderboard score n/a → 0.69427
- expert 73671444 (Grandmaster) · equity · v11→v16   Test each target-transformation variant solo to rank them, then blend the top variants together. Even a variant that is weaker solo can improve the ensemble if its target transformation captures different aspects of the outcome. Include two or three diverse transformations rather than duplicating th
    evidence: ✓ Different valid outcome transforms produce complementary residuals for the same task. | ✗ Most active members share one architecture or algorithm and their residuals are highly correlated.
    leaderboard score 0.68643 → 0.68639 (-0.00004)
- expert 73671444 (Grandmaster) · equity · v27→v30   Prioritize adding models trained on a different transformation of the survival target (e.g., cumulative hazard vs. log-probability vs. log-time) rather than adding another model of the same family on the same target. After each addition, rebalance blend weights and submit; keep the member only if th
    evidence: ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Different valid outcome transforms produce complementary residuals for the same task.
    leaderboard score 0.69303 → 0.69413 (+0.00110)
- expert 75924487 (Master) · equity · v5→v6   Train the same model type multiple times, each with a different target transformation, generate out-of-fold and test predictions from each, and add all as candidate columns for a stacking or blending ensembler. This increases diversity cheaply because only the label encoding changes, not the feature
    evidence: ✓ Different valid outcome transforms produce complementary residuals for the same task.
    leaderboard score n/a → 0.69331
- expert 75145694 (Expert) · equity · v3→v4   Create multiple regression targets from the same survival data using distinct statistical transforms of the censored outcome. Train separate base models on each target variant and blend their predictions. Even small per-model gains compound when the transforms are sufficiently decorrelated.
    evidence: ✓ Different valid outcome transforms produce complementary residuals for the same task.
    leaderboard score 0.68865 → 0.68888 (+0.00022)
- expert 77276039 (Expert) · equity · v10→v12   Train the new model independently with cross-validation, produce out-of-fold and test predictions, then rank-transform all members' predictions before averaging. This makes the combination scale-invariant and avoids destabilizing the ensemble when adding members with different output distributions.
    evidence: ✓ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Different valid outcome transforms produce complementary residuals for the same task.
    leaderboard score 0.69330 → n/a
- expert 73937748 (Master) · equity · v11→v12   When multiplying ensemble members by crossing model families with target transformations, monitor the blended score carefully. A large jump in member count can dilute strong models with mediocre ones, lowering the overall score. Add variants incrementally and validate each addition's marginal contri
    evidence: ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Different valid outcome transforms produce complementary residuals for the same task.
    leaderboard score 0.68948 → 0.68793 (-0.00155)
- expert 73937748 (Master) · equity · v51→v52   Design a new target transformation (e.g., an exponential or power transform of ranks) that preserves ordering but reshapes the target distribution, train the same model families on this new target, and include their predictions in the ensemble blend. Verify that the blended validation metric improve
    evidence: ✗ Most active members share one architecture or algorithm and their residuals are highly correlated. | ✓ Different valid outcome transforms produce complementary residuals for the same task.
    leaderboard score 0.69100 → 0.69155 (+0.00055)
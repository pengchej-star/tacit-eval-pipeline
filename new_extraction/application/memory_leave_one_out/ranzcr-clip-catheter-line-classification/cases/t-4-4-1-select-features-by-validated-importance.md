# Select features by validated importance  `T.4.4.1`   29 edits, 0 experts
13 scored cases, median improvement +0.00019, 7 improved


- expert 27389424 (Grandmaster) · amex · v25→v32   Start with a moderate retention ratio (e.g., one quarter), then try an aggressive cut (e.g., one tenth). If validation drops, walk the ratio back up in small increments (roughly 5–10 percentage points per trial) until the validation metric plateaus or declines. Use median importance across CV folds 
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score n/a → n/a
- expert 27389424 (Grandmaster) · amex · v37→v42   Re-sweep the feature-selection cutoff after any significant regularization change. Start from the previous best, try both more aggressive and more lenient thresholds, and use validation scores to find the new optimum. Expect the optimal cutoff to shift.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions.
    leaderboard score n/a → n/a
- expert 27389424 (Grandmaster) · amex · v43→v54   After making a meaningful pipeline change (e.g., switching the evaluation metric), re-sweep the feature-selection ratio from scratch rather than assuming the old optimum still holds. Use a coarse grid first (e.g., 10%, 25%, 50%, 75%, 100%) and refine around the best. Ensure each run's validation sco
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ The learner supports missing values and is insensitive to feature scaling. | ✗ A model requires finite inputs or the test set contains unseen categories.
    leaderboard score n/a → n/a
- expert 27389424 (Grandmaster) · amex · v57→v62   Sweep the retention fraction in a monotonic sequence (e.g., 10%, 20%, 25%, 33%, 50%, 75%, 100%), submitting or validating at each step. Stop expanding when the metric drops from the previous step; the optimum is at or near the last improvement. Expect a broad plateau rather than a sharp peak.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ The learner supports missing values and is insensitive to feature scaling. | ✗ A model requires finite inputs or the test set contains unseen categories.
    leaderboard score n/a → 0.78861
- expert 27799930 (Contributor) · amex · v13→v14   Extract the built-in feature importance vector from each fold's model, store them in a structured format, average across folds to get a stable ranking, and visualize the top contributors. Use this to identify candidates for removal or deeper engineering.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score n/a → n/a
- expert 27799930 (Contributor) · amex · v63→v65   Start by dropping the full set of low-importance features and submit/validate. If the score drops, iteratively restore subsets of the removed features (shrink the drop list) and re-evaluate until the score recovers or improves. Treat the initial large drop as an upper bound on what can be removed, t
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ The learner supports missing values and is insensitive to feature scaling. | ✓ One recently added or removed feature block has uncertain marginal value.
    leaderboard score 0.79472 → 0.79462 (-0.00010)
- expert 27799930 (Contributor) · amex · v63→v65   Expect that removing all flagged features at once will likely degrade the score because importance estimates are noisy and miss feature interactions. Use the leaderboard or validation metric as the ground truth: if the score drops, restore features in batches rather than trusting the importance rank
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.79472 → 0.79462 (-0.00010)
- expert 28093671 (Contributor) · amex · v25→v26   Extract and average feature importances across all fold models, rank them, and use the top features as the canonical feature set for the new pipeline. This avoids re-discovering feature relevance from scratch and focuses engineering effort on proven signals.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.66422 → n/a
- expert 27656049 (Expert) · amex · v12→v16   Try a modest increase (e.g., +10%) in the number of selected features alongside regularization. If the score does not improve, revert to the smaller set. Prefer the tighter cutoff when gains are absent, because fewer features reduce memory, training time, and overfitting risk.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ The learner supports missing values and is insensitive to feature scaling. | ✓ One recently added or removed feature block has uncertain marginal value. | ✗ Some columns are nearly empty or arbitrary identifiers treated as meaningful measurements.
    leaderboard score 0.79152 → 0.79171 (+0.00019)
- expert 27656049 (Expert) · amex · v17→v18   Test both importance sources on the same pipeline and compare leaderboard or validation scores. If the more expensive attribution method yields a better feature subset, keep it despite the extra computation cost. Change only the selection method in isolation to avoid confounding with other hyperpara
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✗ Some columns are nearly empty or arbitrary identifiers treated as meaningful measurements. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.79071 → 0.79056 (-0.00015)
- expert 60197293 (Expert) · learning · v43→v44   Keep an importance-based feature-selection step in the pipeline and enable it whenever a large batch of new features is introduced. This lets the model automatically discard features that add noise, serving as a safety net that can recover the previous score even if some new features are harmful.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score n/a → 0.81754
- expert 58130512 (Master) · learning · v63→v67   Reduce embedding dimensionality and the number of source models, and simultaneously lower tree complexity (fewer leaves, shallower depth) to match the effective signal-to-noise ratio. High-dimensional embeddings can introduce noise that gradient-boosted trees overfit to; a smaller, curated embedding
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score n/a → 0.82432
- expert 59253662 (Contributor) · learning · v25→v26   Re-run feature selection from scratch whenever the candidate feature set changes, rather than loading a previously saved selection. Save the new result for future runs only after confirming it includes and fairly evaluates all new candidates.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value.
    leaderboard score 0.81799 → 0.81897 (+0.00098)
- expert 55431616 (Grandmaster) · learning · v13→v16   Sweep the feature count in both directions (increase and decrease) around the current value, submitting each to the evaluation metric. If both directions degrade performance, keep the original count and stop searching. Typically try ±5–10% steps.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.81762 → n/a
- expert 59253662 (Contributor) · learning · v16→v17   Pair feature expansion with explicit feature selection (e.g., importance-based pruning) and re-tune key hyperparameters (learning rate, regularization, number of leaves) in the same iteration. Evaluate the combined effect on the leaderboard or a robust validation split before committing.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.80920 → 0.81596 (+0.00676)
- expert 59253662 (Contributor) · learning · v33→v34   Remove the hard feature-count cap and let the feature selection algorithm alone determine how many features to keep. Tree-based models are robust to extra features, so the cap is more likely to hurt than help when the selection method is already filtering.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.81614 → 0.81851 (+0.00237)
- expert 59253662 (Contributor) · learning · v38→v39   After adding new candidate features, re-run the feature-selection procedure on the expanded set rather than simply appending all new columns to the already-selected list. This prevents noisy or redundant features from degrading the model.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score n/a → 0.81519
- expert 58130512 (Master) · learning · v1→v3   First reduce features aggressively (e.g., by 10×) to get a fast baseline, then co-tune the feature count upward alongside model hyperparameters (tree depth, number of leaves, regularization). Evaluate on CV after each joint change to find the right balance between underfitting from too few features 
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.81807 → n/a
- expert 58130512 (Master) · learning · v17→v18   After adding a new feature block, re-tune the feature-selection threshold by testing at least two or three values and comparing leaderboard or validation scores. If performance is highly sensitive to small changes in the cutoff, the new features may not be robustly useful and should be reconsidered 
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.81845 → 0.81755 (-0.00090)
- expert 58130512 (Master) · learning · v24→v27   Always re-run feature selection after changing the feature space. A stale selection list can either exclude the new features entirely or keep a suboptimal mix of old features, making the effect of the new features appear inconsistent across experiments.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling. | ✗ Some columns are nearly empty or arbitrary identifiers treated as meaningful measurements.
    leaderboard score 0.81752 → 0.82049 (+0.00298)
- expert 58130512 (Master) · learning · v27→v28   Replace the embedding features with a CV-based feature-selection wrapper that trains the downstream model per fold, evaluates on held-out data, and selects features by importance. If the score drops, keep the wrapper infrastructure but consider restoring embeddings or adding threshold optimization o
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.82049 → 0.81971 (-0.00078)
- expert 58130512 (Master) · learning · v50→v51   Maintain separate precomputed feature-selection files for different feature configurations. When new features are added, switch to (or regenerate) the selection file that covers the expanded feature set, rather than relying on the old file.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score n/a → n/a
- expert 58130512 (Master) · learning · v57→v58   Try truncating the feature list to a smaller fixed size. If the score drops, the truncation threshold is too aggressive or the ranking does not reliably place the best features first. In that case, revert and instead try importance-based pruning with a validated cutoff rather than an arbitrary cap.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.81922 → 0.81821 (-0.00101)
- expert 58130512 (Master) · learning · v77→v80   Sweep the feature-selection file and the truncation limit together. Test the full list first; if truncating, try a generous limit rather than a very small one. Revert quickly when a combination hurts the score, and keep the file that recovers or exceeds the previous best.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.82224 → 0.82432 (+0.00208)
- expert 60197293 (Expert) · learning · v8→v10   Train the same model type across cross-validation folds, aggregate feature importances across folds, and retain only the top-ranked features. Persist the selected feature list so subsequent runs can skip recomputation. Use a toggle flag to switch between recomputing and loading the saved list.
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score 0.81867 → n/a
- expert 60197293 (Expert) · learning · v14→v17   Run a cross-validated gradient-boosted model, accumulate feature-importance scores across folds, rank features, and keep only the top-N. Cache the selected feature list to disk so subsequent runs can skip recomputation. Rebuild the training matrix from only the selected columns immediately after sel
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling.
    leaderboard score n/a → n/a
- expert 60197293 (Expert) · learning · v124→v130   When introducing new features that were absent from a previously saved feature-selection list, disable the old selection filter so the new features are included. Simultaneously re-tune the number of top features and the ensemble blend weight. Submit several combinations (selection on/off, feature co
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling. | ✓ A model requires finite inputs or the test set contains unseen categories.
    leaderboard score 0.81847 → 0.82153 (+0.00307)
- expert 55987255 (Master) · learning · v41→v46   Start with several candidate models, then prune to the smallest set that fits within resource limits. Reduce topic-model dimensionality proportionally. When changing dimensionality parameters, ensure all downstream references (column name lists, feature selection lists) are updated consistently to a
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value. | ✓ The learner supports missing values and is insensitive to feature scaling. | ✓ A model requires finite inputs or the test set contains unseen categories.
    leaderboard score n/a → n/a
- expert 55987255 (Master) · learning · v89→v92   After observing that expanding the model list hurts, prune back to fewer, higher-quality backbones and replace expensive extracted features with lightweight dimensionality-reduced representations (e.g., latent factors from matrix decomposition). Verify the recovery on the leaderboard before adding c
    evidence: ✓ A large engineered feature matrix contains low-importance or redundant dimensions. | ✓ One recently added or removed feature block has uncertain marginal value.
    leaderboard score n/a → 0.81822
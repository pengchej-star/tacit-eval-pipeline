# Regenerate selection artifacts after input changes  `T.3.2.4`   6 edits, 0 experts
4 scored cases (improvement signed by each competition's direction), median +0.00298, 3 improved


- expert 59253662 · learning · v25→v26   Re-run feature selection from scratch whenever the candidate feature set changes, rather than loading a previously saved selection. Save the new result for future runs only after confirming it includes and fairly evaluates all new candidates.
    evidence: ✓ A saved feature list was built for a different feature schema.
    leaderboard score 0.81799 → 0.81897 (higher is better; improved by 0.00098)
- expert 59253662 · learning · v38→v39   After adding new candidate features, re-run the feature-selection procedure on the expanded set rather than simply appending all new columns to the already-selected list. This prevents noisy or redundant features from degrading the model.
    evidence: ✓ A saved feature list was built for a different feature schema.
    leaderboard score n/a → 0.81519 (higher is better)
- expert 58130512 · learning · v24→v27   Always re-run feature selection after changing the feature space. A stale selection list can either exclude the new features entirely or keep a suboptimal mix of old features, making the effect of the new features appear inconsistent across experiments.
    evidence: ✓ A saved feature list was built for a different feature schema.
    leaderboard score 0.81752 → 0.82049 (higher is better; improved by 0.00298)
- expert 58130512 · learning · v50→v51   Maintain separate precomputed feature-selection files for different feature configurations. When new features are added, switch to (or regenerate) the selection file that covers the expanded feature set, rather than relying on the old file.
    evidence: ✓ A saved feature list was built for a different feature schema.
    leaderboard score n/a → n/a (higher is better)
- expert 60197293 · learning · v94→v95   After fixing the artifact's loading, run the pipeline and compare the metric to a run without the artifact. If performance degrades, disable or regenerate the artifact to match the current pipeline state rather than assuming it is still optimal.
    evidence: ✓ A saved feature list was built for a different feature schema.
    leaderboard score 0.81836 → 0.81593 (higher is better; worse by 0.00243)
- expert 60197293 · learning · v124→v130   When introducing new features that were absent from a previously saved feature-selection list, disable the old selection filter so the new features are included. Simultaneously re-tune the number of top features and the ensemble blend weight. Submit several combinations (selection on/off, feature co
    evidence: ✓ A saved feature list was built for a different feature schema.
    leaderboard score 0.81847 → 0.82153 (higher is better; improved by 0.00307)
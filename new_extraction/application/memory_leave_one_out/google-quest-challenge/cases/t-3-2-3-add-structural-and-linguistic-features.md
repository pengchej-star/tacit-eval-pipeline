# Add structural and linguistic features  `T.3.2.3`   14 edits, 0 experts
10 scored cases (improvement signed by each competition's direction), median +0.00158, 6 improved


- expert 18757376 · commonlitreadabilityprize · v3→v4   Treat this as a probe: add the handcrafted features and an additional meta-learner in one step, then check the leaderboard. If the score worsens, the extra features likely add noise or cause overfitting in the meta-learner on the small dataset, and should be reverted. Avoid bundling too many changes
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations.
    leaderboard score 0.46300 → 0.46496 (lower is better; worse by 0.00196)
- expert 55431616 · learning · v15→v16   Engineer new aggregation-based features (e.g., additional quantiles, new binning thresholds for structural text properties) and add them to the pool before re-running feature selection at the previously best cutoff. This changes what is available to select rather than how many are selected.
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations.
    leaderboard score 0.81503 → n/a (higher is better)
- expert 59253662 · learning · v16→v17   Split documents into logical sections (e.g., introduction, body, conclusion) and compute the same feature set independently for each section. This lets the model capture section-level quality signals (e.g., weak conclusion) that whole-document averages obscure. Combine with stopword removal and aggr
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations.
    leaderboard score 0.80920 → 0.81596 (higher is better; improved by 0.00676)
- expert 59253662 · learning · v17→v23   Extract token-level linguistic features (POS tag distributions, named entity counts, verb tense ratios, spelling error rates) and document-level readability scores using an NLP pipeline. Process in batches to manage memory. Temporarily disable automatic feature selection so all new features are incl
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations.
    leaderboard score 0.81596 → 0.81799 (higher is better; improved by 0.00203)
- expert 59253662 · learning · v25→v26   Compute the same readability and syntactic metrics at the sentence level, then aggregate (mean, std, min, max) across sentences to create new features. Re-run feature selection from scratch after adding the new features so the selector can evaluate them fairly alongside existing ones. Expect a modes
    evidence: ✓ Multiple observations describe each prediction entity but only a narrow summary is used. | ✓ Text structure or metadata relevant to the target is absent from current representations.
    leaderboard score 0.81799 → 0.81897 (higher is better; improved by 0.00098)
- expert 58130512 · learning · v4→v10   Test the new features by adding them to the existing pipeline and comparing leaderboard or validation scores. If the score does not improve or drops, remove them promptly rather than continuing to tune around them. Sparse n-gram features often already encode sentiment and topic signals, so redundant
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations. | ✓ Sparse text features are noisy, overly narrow, or too high-dimensional for the downstream learner. | ✓ Multiple observations describe each prediction entity but only a narrow summary is used. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.81774 → 0.79271 (higher is better; worse by 0.02503)
- expert 58130512 · learning · v12→v16   Add the candidate features, evaluate on local validation, and if no improvement appears, prune them back incrementally. Submit only after pruning to confirm. If the leaderboard score drops, abandon the feature family entirely rather than continuing to tune it.
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations. | ✓ Multiple observations describe each prediction entity but only a narrow summary is used.
    leaderboard score 0.81929 → 0.81644 (higher is better; worse by 0.00284)
- expert 58130512 · learning · v97→v99   Merge external metadata as categorical or binary features. Evaluate whether the added features help by submitting with and without them. If a secondary model type (added alongside the primary) doesn't improve results, remove it but keep the useful features.
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations.
    leaderboard score 0.82179 → 0.82337 (higher is better; improved by 0.00158)
- expert 58130512 · learning · v105→v108   Probe by adding the handcrafted features and comparing the leaderboard score. If the score drops or stays flat, the features add noise or redundancy; remove them promptly rather than continuing to tune around them. Treat a score drop after adding many correlated features as evidence of overfitting o
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations. | ✓ Sparse text features are noisy, overly narrow, or too high-dimensional for the downstream learner. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score n/a → 0.82140 (higher is better)
- expert 60197293 · learning · v10→v14   Add the feature to the training set, run cross-validation, then comment it out and re-run to compare. If it helps, re-enable it and ensure it is computed identically for both train and test to maintain feature parity. This add-disable-re-enable cycle across a few versions isolates the feature's cont
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations. | ✓ Sparse text features are noisy, overly narrow, or too high-dimensional for the downstream learner.
    leaderboard score n/a → n/a (higher is better)
- expert 60197293 · learning · v27→v28   Toggle the hand-crafted features off and compare leaderboard or validation performance. If removing them improves or matches the score, drop them—the n-gram features likely already encode the same signal with less noise.
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score n/a → 0.81799 (higher is better)
- expert 55987255 · learning · v12→v28   Expect diminishing or zero returns from simple count-based text features when rich vectorized representations are already present. Limit exploration to a few iterations; if the first submission shows less than ~0.1% relative improvement, move on to qualitatively different feature families (e.g., rea
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations. | ✓ Available pretrained representations encode information missing from the current tabular features. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.81757 → 0.81715 (higher is better; worse by 0.00042)
- expert 55987255 · learning · v28→v37   Add complementary feature families one batch at a time: topic-model components for thematic signal, sentiment scores for tone, and readability indices for writing complexity. After adding each batch, test for errors and prune individual features that are unstable, redundant, or cause runtime issues 
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations. | ✓ Sparse text features are noisy, overly narrow, or too high-dimensional for the downstream learner.
    leaderboard score 0.81715 → 0.81943 (higher is better; improved by 0.00228)
- expert 55987255 · learning · v58→v80   Add features in small, testable batches rather than all at once. When a large batch is added and the score does not improve, prune features iteratively by removing groups (ratios, sentiment, paragraph stats) and submitting after each removal. If the pruned version still underperforms the pre-feature
    evidence: ✓ Text structure or metadata relevant to the target is absent from current representations. | ✗ Available pretrained representations encode information missing from the current tabular features. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score 0.81777 → 0.82029 (higher is better; improved by 0.00252)
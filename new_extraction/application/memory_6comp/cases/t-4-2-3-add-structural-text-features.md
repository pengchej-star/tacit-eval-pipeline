# Add structural text features  `T.4.2.3`   17 edits, 0 experts
11 scored cases, median improvement +0.00158, 7 improved


- expert 7573212 (Contributor) · google · v4→v5   Compute surface-level text features (word counts, sentence counts, categorical indicators), standardize them, and concatenate them with the language model's pooled output before the prediction head. Retrain with these additional inputs and verify improvement on the leaderboard or validation metric.
    evidence: ✗ The current representation has lexical features but little contextual semantic information. | ✓ Text length, structure, or linguistic quality is relevant but absent from current features.
    leaderboard score 0.38324 → 0.38598 (+0.00273)
- expert 55431616 (Grandmaster) · learning · v15→v16   Engineer new aggregation-based features (e.g., additional quantiles, new binning thresholds for structural text properties) and add them to the pool before re-running feature selection at the previously best cutoff. This changes what is available to select rather than how many are selected.
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features.
    leaderboard score 0.81503 → n/a
- expert 58527792 (Contributor) · learning · v4→v13   Layer three feature families: (1) handcrafted text statistics (readability, error counts, length distributions, paragraph/sentence aggregates), (2) pretrained transformer embeddings or logits, (3) bag-of-words/TF-IDF. Apply feature selection to keep the top-k most informative features. Train two dif
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features. | ✓ The current representation has lexical features but little contextual semantic information. | ✓ Sparse representations are large and latent topics or low-dimensional summaries are available.
    leaderboard score 0.82214 → n/a
- expert 59253662 (Contributor) · learning · v16→v17   Split documents into logical sections (e.g., introduction, body, conclusion) and compute the same feature set independently for each section. This lets the model capture section-level quality signals (e.g., weak conclusion) that whole-document averages obscure. Combine with stopword removal and aggr
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features.
    leaderboard score 0.80920 → 0.81596 (+0.00676)
- expert 59253662 (Contributor) · learning · v17→v23   Extract token-level linguistic features (POS tag distributions, named entity counts, verb tense ratios, spelling error rates) and document-level readability scores using an NLP pipeline. Process in batches to manage memory. Temporarily disable automatic feature selection so all new features are incl
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features.
    leaderboard score 0.81596 → 0.81799 (+0.00203)
- expert 59253662 (Contributor) · learning · v25→v26   Compute the same readability and syntactic metrics at the sentence level, then aggregate (mean, std, min, max) across sentences to create new features. Re-run feature selection from scratch after adding the new features so the selector can evaluate them fairly alongside existing ones. Expect a modes
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features.
    leaderboard score 0.81799 → 0.81897 (+0.00098)
- expert 59253662 (Contributor) · learning · v37→v39   Do not change multiple things at once (new features and hyperparameter adjustments) in a single submission. When a large batch of new features is added, keep the previously validated hyperparameters fixed first to isolate the effect of the features. If the combined change hurts, you cannot tell whic
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features.
    leaderboard score 0.82433 → 0.81519 (-0.00914)
- expert 58130512 (Master) · learning · v4→v10   Test the new features by adding them to the existing pipeline and comparing leaderboard or validation scores. If the score does not improve or drops, remove them promptly rather than continuing to tune around them. Sparse n-gram features often already encode sentiment and topic signals, so redundant
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features. | ✓ Sparse representations are large and latent topics or low-dimensional summaries are available. | ✓ Useful lexical patterns are excluded or rare n-grams dominate the feature space.
    leaderboard score 0.81774 → 0.79271 (-0.02503)
- expert 58130512 (Master) · learning · v12→v16   Add the candidate features, evaluate on local validation, and if no improvement appears, prune them back incrementally. Submit only after pruning to confirm. If the leaderboard score drops, abandon the feature family entirely rather than continuing to tune it.
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features.
    leaderboard score 0.81929 → 0.81644 (-0.00284)
- expert 58130512 (Master) · learning · v97→v99   Merge external metadata as categorical or binary features. Evaluate whether the added features help by submitting with and without them. If a secondary model type (added alongside the primary) doesn't improve results, remove it but keep the useful features.
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features. | ✓ Related labeled texts or auxiliary predictions can provide information absent from current features. | ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score 0.82179 → 0.82337 (+0.00158)
- expert 58130512 (Master) · learning · v105→v108   Probe by adding the handcrafted features and comparing the leaderboard score. If the score drops or stays flat, the features add noise or redundancy; remove them promptly rather than continuing to tune around them. Treat a score drop after adding many correlated features as evidence of overfitting o
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features. | ✗ The current representation has lexical features but little contextual semantic information.
    leaderboard score n/a → 0.82140
- expert 60197293 (Expert) · learning · v10→v14   Add the feature to the training set, run cross-validation, then comment it out and re-run to compare. If it helps, re-enable it and ensure it is computed identically for both train and test to maintain feature parity. This add-disable-re-enable cycle across a few versions isolates the feature's cont
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features. | ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score n/a → n/a
- expert 60197293 (Expert) · learning · v27→v28   Toggle the hand-crafted features off and compare leaderboard or validation performance. If removing them improves or matches the score, drop them—the n-gram features likely already encode the same signal with less noise.
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features.
    leaderboard score n/a → 0.81799
- expert 55987255 (Master) · learning · v12→v28   Expect diminishing or zero returns from simple count-based text features when rich vectorized representations are already present. Limit exploration to a few iterations; if the first submission shows less than ~0.1% relative improvement, move on to qualitatively different feature families (e.g., rea
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features. | ✗ The current representation has lexical features but little contextual semantic information. | ✗ Sparse representations are large and latent topics or low-dimensional summaries are available. | ✓ Formatting, metadata, or input truncation may obscure task-relevant content. | ✓ Related labeled texts or auxiliary predictions can provide information absent from current features.
    leaderboard score 0.81757 → 0.81715 (-0.00042)
- expert 55987255 (Master) · learning · v22→v25   Pick one canonical preprocessing pipeline — typically the most thorough one — and compute features only from that variant. Drop the rest to avoid multicollinearity and feature bloat. Verify with a single submission that the reduced set matches or exceeds the full set before iterating further.
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features. | ✓ Formatting, metadata, or input truncation may obscure task-relevant content.
    leaderboard score n/a → n/a
- expert 55987255 (Master) · learning · v28→v37   Add complementary feature families one batch at a time: topic-model components for thematic signal, sentiment scores for tone, and readability indices for writing complexity. After adding each batch, test for errors and prune individual features that are unstable, redundant, or cause runtime issues 
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features. | ✓ Sparse representations are large and latent topics or low-dimensional summaries are available.
    leaderboard score 0.81715 → 0.81943 (+0.00228)
- expert 55987255 (Master) · learning · v58→v80   Add features in small, testable batches rather than all at once. When a large batch is added and the score does not improve, prune features iteratively by removing groups (ratios, sentiment, paragraph stats) and submitting after each removal. If the pruned version still underperforms the pre-feature
    evidence: ✓ Text length, structure, or linguistic quality is relevant but absent from current features. | ✗ The current representation has lexical features but little contextual semantic information. | ✗ Sparse representations are large and latent topics or low-dimensional summaries are available.
    leaderboard score 0.81777 → 0.82029 (+0.00252)
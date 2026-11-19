# Use structural and linguistic features  `T.3.2.2.3`   18 edits, 0 experts
12 scored cases (improvement signed by each competition's direction), median +0.00203, 8 improved


- expert 18757376 · commonlitreadabilityprize · v3→v4   Treat this as a probe: add the handcrafted features and an additional meta-learner in one step, then check the leaderboard. If the score worsens, the extra features likely add noise or cause overfitting in the meta-learner on the small dataset, and should be reverted. Avoid bundling too many changes
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.46300 → 0.46496 (lower is better; worse by 0.00196)
- expert 7613444 · google · v6→v7   Remove the sparse categorical input branch and rely on a small set of dense engineered numeric features as auxiliary inputs. Evaluate whether the simpler model matches or exceeds the previous score; if so, keep the simpler version to reduce overfitting risk.
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.39832 → n/a (higher is better)
- expert 7573212 · google · v4→v5   Compute surface-level text features (word counts, sentence counts, categorical indicators), standardize them, and concatenate them with the language model's pooled output before the prediction head. Retrain with these additional inputs and verify improvement on the leaderboard or validation metric.
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.38324 → 0.38598 (higher is better; improved by 0.00273)
- expert 7240226 · google · v6→v7   One-hot encode the categorical metadata, concatenate it with the text encoder's pooled output, and feed the combined vector into the prediction head. Evaluate on the leaderboard or validation to confirm the gain.
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.38126 → 0.38697 (higher is better; improved by 0.00571)
- expert 55431616 · learning · v15→v16   Engineer new aggregation-based features (e.g., additional quantiles, new binning thresholds for structural text properties) and add them to the pool before re-running feature selection at the previously best cutoff. This changes what is available to select rather than how many are selected.
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.81503 → n/a (higher is better)
- expert 59253662 · learning · v16→v17   Split documents into logical sections (e.g., introduction, body, conclusion) and compute the same feature set independently for each section. This lets the model capture section-level quality signals (e.g., weak conclusion) that whole-document averages obscure. Combine with stopword removal and aggr
    evidence: ✗ Lexical frequency or topic information is absent or dominated by very rare n-grams. | ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.80920 → 0.81596 (higher is better; improved by 0.00676)
- expert 59253662 · learning · v17→v23   Extract token-level linguistic features (POS tag distributions, named entity counts, verb tense ratios, spelling error rates) and document-level readability scores using an NLP pipeline. Process in batches to manage memory. Temporarily disable automatic feature selection so all new features are incl
    evidence: ✓ The target depends on document structure or language quality not explicitly represented. | ✗ Lexical frequency or topic information is absent or dominated by very rare n-grams. | ✗ The current features lack contextual semantics and suitable pretrained encoders are available.
    leaderboard score 0.81596 → 0.81799 (higher is better; improved by 0.00203)
- expert 59253662 · learning · v25→v26   Compute the same readability and syntactic metrics at the sentence level, then aggregate (mean, std, min, max) across sentences to create new features. Re-run feature selection from scratch after adding the new features so the selector can evaluate them fairly alongside existing ones. Expect a modes
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.81799 → 0.81897 (higher is better; improved by 0.00098)
- expert 58130512 · learning · v4→v10   Test the new features by adding them to the existing pipeline and comparing leaderboard or validation scores. If the score does not improve or drops, remove them promptly rather than continuing to tune around them. Sparse n-gram features often already encode sentiment and topic signals, so redundant
    evidence: ✓ The target depends on document structure or language quality not explicitly represented. | ✓ Lexical frequency or topic information is absent or dominated by very rare n-grams.
    leaderboard score 0.81774 → 0.79271 (higher is better; worse by 0.02503)
- expert 58130512 · learning · v12→v16   Add the candidate features, evaluate on local validation, and if no improvement appears, prune them back incrementally. Submit only after pruning to confirm. If the leaderboard score drops, abandon the feature family entirely rather than continuing to tune it.
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.81929 → 0.81644 (higher is better; worse by 0.00284)
- expert 58130512 · learning · v97→v99   Merge external metadata as categorical or binary features. Evaluate whether the added features help by submitting with and without them. If a secondary model type (added alongside the primary) doesn't improve results, remove it but keep the useful features.
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.82179 → 0.82337 (higher is better; improved by 0.00158)
- expert 58130512 · learning · v105→v108   Probe by adding the handcrafted features and comparing the leaderboard score. If the score drops or stays flat, the features add noise or redundancy; remove them promptly rather than continuing to tune around them. Treat a score drop after adding many correlated features as evidence of overfitting o
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score n/a → 0.82140 (higher is better)
- expert 58527792 · learning · v4→v13   Layer three feature families: (1) handcrafted text statistics (readability, error counts, length distributions, paragraph/sentence aggregates), (2) pretrained transformer embeddings or logits, (3) bag-of-words/TF-IDF. Apply feature selection to keep the top-k most informative features. Train two dif
    evidence: ✓ The target depends on document structure or language quality not explicitly represented. | ✓ The current features lack contextual semantics and suitable pretrained encoders are available. | ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata. | ✓ Lexical frequency or topic information is absent or dominated by very rare n-grams.
    leaderboard score 0.82214 → n/a (higher is better)
- expert 60197293 · learning · v10→v14   Add the feature to the training set, run cross-validation, then comment it out and re-run to compare. If it helps, re-enable it and ensure it is computed identically for both train and test to maintain feature parity. This add-disable-re-enable cycle across a few versions isolates the feature's cont
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score n/a → n/a (higher is better)
- expert 60197293 · learning · v27→v28   Toggle the hand-crafted features off and compare leaderboard or validation performance. If removing them improves or matches the score, drop them—the n-gram features likely already encode the same signal with less noise.
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score n/a → 0.81799 (higher is better)
- expert 55987255 · learning · v12→v28   Expect diminishing or zero returns from simple count-based text features when rich vectorized representations are already present. Limit exploration to a few iterations; if the first submission shows less than ~0.1% relative improvement, move on to qualitatively different feature families (e.g., rea
    evidence: ✓ The target depends on document structure or language quality not explicitly represented. | ✗ Lexical frequency or topic information is absent or dominated by very rare n-grams. | ✗ The current features lack contextual semantics and suitable pretrained encoders are available. | ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist. | ✓ Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.
    leaderboard score 0.81757 → 0.81715 (higher is better; worse by 0.00042)
- expert 55987255 · learning · v28→v37   Add complementary feature families one batch at a time: topic-model components for thematic signal, sentiment scores for tone, and readability indices for writing complexity. After adding each batch, test for errors and prune individual features that are unstable, redundant, or cause runtime issues 
    evidence: ✓ The target depends on document structure or language quality not explicitly represented. | ✓ Lexical frequency or topic information is absent or dominated by very rare n-grams.
    leaderboard score 0.81715 → 0.81943 (higher is better; improved by 0.00228)
- expert 55987255 · learning · v58→v80   Add features in small, testable batches rather than all at once. When a large batch is added and the score does not improve, prune features iteratively by removing groups (ratios, sentiment, paragraph stats) and submitting after each removal. If the pruned version still underperforms the pre-feature
    evidence: ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.81777 → 0.82029 (higher is better; improved by 0.00252)
# Compare concatenation with averaging  `T.4.6.4`   5 edits, 0 experts
3 scored cases, median improvement -0.00510, 0 improved


- expert 53424936 (Master) · hms · v5→v6   Strip the classifier heads from all branches so each outputs only its feature vector. Concatenate the new branch's features with existing ones and add a new combined head. For ensembling, load each fold's checkpoint into a list and average their probability outputs with equal weights at inference ti
    evidence: ✓ A different modality or representation carries information the current branch cannot see. | ✓ Equal-width branch embeddings are averaged before classification, potentially discarding distinct information. | ✓ A full-modality baseline score exists to compare the ablation against.
    leaderboard score 0.22872 → n/a
- expert 53424936 (Master) · hms · v13→v14   Concatenate features from several backbone variants and retrain/load corresponding checkpoints. Expect partial but not full recovery compared to a truly heterogeneous ensemble (different architecture families, different input views, test-time augmentation). Track the gap to decide whether to also re
    evidence: none recorded
    leaderboard score 0.23094 → 0.22969 (-0.00125)
- expert 50496431 (Grandmaster) · hms · v99→v101   Try both concatenation and element-wise averaging of branch embeddings. Evaluate each not only in isolation but within the full ensemble, since a simpler fusion (averaging) may generalize better and contribute more stably to a blended prediction even if its standalone score is similar or slightly wo
    evidence: ✓ Equal-width branch embeddings are averaged before classification, potentially discarding distinct information. | ✓ A full-modality baseline score exists to compare the ablation against. | ✓ The pretrained weights were trained with a specific fusion method, so changing the fusion strategy at inference creates a train/inference mismatch. | ✓ A different modality or representation carries information the current branch cannot see.
    leaderboard score 0.29399 → 0.27434 (-0.01965)
- expert 50496431 (Grandmaster) · hms · v140→v141   Replace element-wise averaging with concatenation along the feature dimension and double the input size of the subsequent linear layer. This lets the classifier learn modality-specific and cross-modality patterns. Verify with a submission or validation that the richer representation improves the met
    evidence: ✓ Equal-width branch embeddings are averaged before classification, potentially discarding distinct information. | ✓ A full-modality baseline score exists to compare the ablation against. | ✓ The pretrained weights were trained with a specific fusion method, so changing the fusion strategy at inference creates a train/inference mismatch.
    leaderboard score 0.24785 → 0.24275 (-0.00510)
- expert 50496431 (Grandmaster) · hms · v146→v148   Try concatenation (doubling the classifier input dimension) versus element-wise averaging (keeping the original dimension). Concatenation preserves distinct information from each branch and typically scores better when the classifier has enough capacity, at the cost of doubling the final layer's par
    evidence: ✓ Equal-width branch embeddings are averaged before classification, potentially discarding distinct information. | ✓ A full-modality baseline score exists to compare the ablation against. | ✓ The pretrained weights were trained with a specific fusion method, so changing the fusion strategy at inference creates a train/inference mismatch.
    leaderboard score n/a → 0.23064
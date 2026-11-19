# Fuse complementary branch embeddings  `T.4.4.4`   5 edits, 0 experts
3 scored cases (improvement signed by each competition's direction), median +0.00510, 2 improved


- expert 53424936 · hms · v5→v6   Strip the classifier heads from all branches so each outputs only its feature vector. Concatenate the new branch's features with existing ones and add a new combined head. For ensembling, load each fold's checkpoint into a list and average their probability outputs with equal weights at inference ti
    evidence: ✓ Multiple aligned input branches provide complementary representations.
    leaderboard score 0.22872 → n/a (lower is better)
- expert 53424936 · hms · v28→v30   Test by temporarily replacing the fusion model with a single-backbone ensemble using the same checkpoints and preprocessing. If the score degrades, restore the fusion architecture. This A/B comparison isolates whether the fusion structure itself contributes to performance or just adds complexity.
    evidence: ✓ Multiple aligned input branches provide complementary representations. | ✓ The checkpoints being loaded were trained with a different head architecture than the current inference model, causing dimension or weight mismatches. | ✗ Extra heads or layers have failed controlled comparisons or overfit.
    leaderboard score 0.22621 → 0.22629 (lower is better; worse by 0.00008)
- expert 50496431 · hms · v99→v101   Try both concatenation and element-wise averaging of branch embeddings. Evaluate each not only in isolation but within the full ensemble, since a simpler fusion (averaging) may generalize better and contribute more stably to a blended prediction even if its standalone score is similar or slightly wo
    evidence: ✓ Multiple aligned input branches provide complementary representations. | ✓ The checkpoints being loaded were trained with a different head architecture than the current inference model, causing dimension or weight mismatches.
    leaderboard score 0.29399 → 0.27434 (lower is better; improved by 0.01965)
- expert 50496431 · hms · v140→v141   Replace element-wise averaging with concatenation along the feature dimension and double the input size of the subsequent linear layer. This lets the classifier learn modality-specific and cross-modality patterns. Verify with a submission or validation that the richer representation improves the met
    evidence: ✓ Multiple aligned input branches provide complementary representations. | ✓ The checkpoints being loaded were trained with a different head architecture than the current inference model, causing dimension or weight mismatches.
    leaderboard score 0.24785 → 0.24275 (lower is better; improved by 0.00510)
- expert 50496431 · hms · v146→v148   Try concatenation (doubling the classifier input dimension) versus element-wise averaging (keeping the original dimension). Concatenation preserves distinct information from each branch and typically scores better when the classifier has enough capacity, at the cost of doubling the final layer's par
    evidence: ✓ Multiple aligned input branches provide complementary representations. | ✓ The checkpoints being loaded were trained with a different head architecture than the current inference model, causing dimension or weight mismatches.
    leaderboard score n/a → 0.23064 (lower is better)
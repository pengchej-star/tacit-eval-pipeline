# Change feature fusion  `T.4.1.4`   4 edits, 0 experts
2 scored cases, median improvement -0.00510, 0 improved


- expert 53424936 (Master) · hms · v17→v20   When a complex model underperforms expectations at inference, systematically check for data-processing bugs (e.g., features computed using training-only metadata like label offsets that are unavailable at test time). Fix such leaks by using test-compatible defaults, then scale up the fold ensemble a
    evidence: ✓ Multiple aligned feature branches are already available but fusion collapses their information. | ✓ A suitable alternative pretrained family or size is available and current representation quality has plateaued.
    leaderboard score n/a → 0.22756
- expert 50496431 (Grandmaster) · hms · v99→v101   Try both concatenation and element-wise averaging of branch embeddings. Evaluate each not only in isolation but within the full ensemble, since a simpler fusion (averaging) may generalize better and contribute more stably to a blended prediction even if its standalone score is similar or slightly wo
    evidence: ✓ Multiple aligned feature branches are already available but fusion collapses their information.
    leaderboard score 0.29399 → 0.27434 (-0.01965)
- expert 50496431 (Grandmaster) · hms · v140→v141   Replace element-wise averaging with concatenation along the feature dimension and double the input size of the subsequent linear layer. This lets the classifier learn modality-specific and cross-modality patterns. Verify with a submission or validation that the richer representation improves the met
    evidence: ✓ Multiple aligned feature branches are already available but fusion collapses their information.
    leaderboard score 0.24785 → 0.24275 (-0.00510)
- expert 50496431 (Grandmaster) · hms · v146→v148   Try concatenation (doubling the classifier input dimension) versus element-wise averaging (keeping the original dimension). Concatenation preserves distinct information from each branch and typically scores better when the classifier has enough capacity, at the cost of doubling the final layer's par
    evidence: ✓ Multiple aligned feature branches are already available but fusion collapses their information.
    leaderboard score n/a → 0.23064
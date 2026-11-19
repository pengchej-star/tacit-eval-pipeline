# Add structured metadata features  `T.4.3.4`   3 edits, 0 experts
2 scored cases, median improvement +0.00571, 2 improved


- expert 7613444 (Contributor) · google · v6→v7   Remove the sparse categorical input branch and rely on a small set of dense engineered numeric features as auxiliary inputs. Evaluate whether the simpler model matches or exceeds the previous score; if so, keep the simpler version to reduce overfitting risk.
    evidence: ✓ Structured metadata is present at both training and inference and varies with residual errors. | ✓ Recent feature additions increased dimension without a reliable validation gain.
    leaderboard score 0.39832 → n/a
- expert 7240226 (Contributor) · google · v6→v7   One-hot encode the categorical metadata, concatenate it with the text encoder's pooled output, and feed the combined vector into the prediction head. Evaluate on the leaderboard or validation to confirm the gain.
    evidence: ✓ Structured metadata is present at both training and inference and varies with residual errors. | ✗ Recent feature additions increased dimension without a reliable validation gain.
    leaderboard score 0.38126 → 0.38697 (+0.00571)
- expert 58130512 (Master) · learning · v97→v99   Merge external metadata as categorical or binary features. Evaluate whether the added features help by submitting with and without them. If a secondary model type (added alongside the primary) doesn't improve results, remove it but keep the useful features.
    evidence: ✓ Structured metadata is present at both training and inference and varies with residual errors. | ✓ Recent feature additions increased dimension without a reliable validation gain. | ✓ The saved feature-selection list predates the current feature matrix.
    leaderboard score 0.82179 → 0.82337 (+0.00158)
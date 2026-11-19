# Reuse fitted categorical mappings  `T.4.1.2`   2 edits, 0 experts
1 scored cases, median improvement +0.00603, 1 improved


- expert 7823861 (nan) · google · v8→v10   Fit the encoder on training data only. At test time, call transform (not fit_transform) on the test data. Ensure the output array has exactly as many rows as the test set. Set the encoder to handle unknown categories gracefully (e.g., ignore or map to a default) so unseen test categories do not caus
    evidence: ✓ Test categories are unseen or encoded differently from training categories. | ✓ The encoding transform produces an output with mismatched row counts between train and test sets.
    leaderboard score n/a → 0.41495
- expert 7823861 (nan) · google · v10→v15   Use two layers of defense: configure the encoder to ignore unknown categories (producing a zero-vector), and also remap unknown values to the most frequent or most representative training category before encoding. This avoids both crashes and degenerate feature vectors.
    evidence: ✓ Test categories are unseen or encoded differently from training categories. | ✓ The encoding transform produces an output with mismatched row counts between train and test sets.
    leaderboard score 0.41495 → 0.42097 (+0.00603)
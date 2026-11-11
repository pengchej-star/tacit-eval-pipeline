# Tune sparse lexical features  `T.4.2.1`   2 edits, 0 experts

- expert 58130512 (Master) · learning · v15→v16   Avoid removing the lowest-order n-grams (e.g., unigrams) from word-level features, as they often carry the most discriminative signal. If a score drop follows tightening, restore the original range before attributing the loss to other simultaneous changes. Change n-gram ranges independently from oth
    evidence: ✓ Useful lexical patterns are excluded or rare n-grams dominate the feature space. | ✓ Sparse representations are large and latent topics or low-dimensional summaries are available.
    leaderboard score n/a → 0.81644
- expert 55987255 (Master) · learning · v124→v136   Sweep minimum document frequency upward in multiplicative steps (e.g., doubling) while watching validation; simultaneously lower maximum document frequency to remove ubiquitous tokens. Vary the n-gram range endpoints one at a time. After each change, check CV; if no improvement after several steps i
    evidence: ✓ Useful lexical patterns are excluded or rare n-grams dominate the feature space. | ✓ Sparse representations are large and latent topics or low-dimensional summaries are available. | ✓ Text length, structure, or linguistic quality is relevant but absent from current features.
    leaderboard score n/a → n/a
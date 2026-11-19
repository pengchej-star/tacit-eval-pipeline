# Tune sparse text representations  `T.3.1.5`   5 edits, 0 experts
2 scored cases, median improvement +0.02527, 2 improved


- expert 59253662 (Contributor) · learning · v10→v11   Fix the number of topics to a small explicit value rather than using automatic selection, so features are stable across train and test. Use locally cached embedding checkpoints to avoid download failures and ensure reproducibility. Adjust clustering granularity to roughly match the number of target 
    evidence: ✓ Lexical frequency or local word patterns are absent or poorly covered by current features. | ✓ Semantic embeddings are absent, or existing embedding sources have uncertain marginal value.
    leaderboard score n/a → 0.78393
- expert 59253662 (Contributor) · learning · v11→v16   Extract character-level and word-level n-gram features via sparse vectorizers, convert to dense, and concatenate with existing features. Generate out-of-fold predictions from the deep model for training rows and averaged ensemble predictions for test rows, appending these as additional numeric featu
    evidence: ✓ Lexical frequency or local word patterns are absent or poorly covered by current features. | ✓ Another model or related labeled source provides predictive information absent from current inputs.
    leaderboard score 0.78393 → 0.80920 (+0.02527)
- expert 58130512 (Master) · learning · v15→v16   Avoid removing the lowest-order n-grams (e.g., unigrams) from word-level features, as they often carry the most discriminative signal. If a score drop follows tightening, restore the original range before attributing the loss to other simultaneous changes. Change n-gram ranges independently from oth
    evidence: ✓ Lexical frequency or local word patterns are absent or poorly covered by current features.
    leaderboard score n/a → 0.81644
- expert 55987255 (Master) · learning · v1→v5   Test each dense representation (topic-model components, averaged word embeddings) individually by adding/removing it and checking the validation or leaderboard metric. Then combine the ones that each helped individually; complementary representations often stack well because they capture different a
    evidence: ✓ Lexical frequency or local word patterns are absent or poorly covered by current features. | ✓ Semantic embeddings are absent, or existing embedding sources have uncertain marginal value.
    leaderboard score 0.81691 → 0.81791 (+0.00100)
- expert 55987255 (Master) · learning · v124→v136   Sweep minimum document frequency upward in multiplicative steps (e.g., doubling) while watching validation; simultaneously lower maximum document frequency to remove ubiquitous tokens. Vary the n-gram range endpoints one at a time. After each change, check CV; if no improvement after several steps i
    evidence: ✓ Lexical frequency or local word patterns are absent or poorly covered by current features. | ✓ Text structure or error patterns vary with the target beyond the current representation.
    leaderboard score n/a → n/a
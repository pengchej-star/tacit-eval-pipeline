# Use lexical or latent text features  `T.3.2.2.2`   5 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.02527, 2 improved


- expert 59253662 · learning · v10→v11   Fix the number of topics to a small explicit value rather than using automatic selection, so features are stable across train and test. Use locally cached embedding checkpoints to avoid download failures and ensure reproducibility. Adjust clustering granularity to roughly match the number of target 
    evidence: ✓ Lexical frequency or topic information is absent or dominated by very rare n-grams. | ✓ The current features lack contextual semantics and suitable pretrained encoders are available.
    leaderboard score n/a → 0.78393 (higher is better)
- expert 59253662 · learning · v11→v16   Extract character-level and word-level n-gram features via sparse vectorizers, convert to dense, and concatenate with existing features. Generate out-of-fold predictions from the deep model for training rows and averaged ensemble predictions for test rows, appending these as additional numeric featu
    evidence: ✓ Lexical frequency or topic information is absent or dominated by very rare n-grams. | ✓ Compatible out-of-fold predictions or leakage-safe auxiliary labels exist. | ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score 0.78393 → 0.80920 (higher is better; improved by 0.02527)
- expert 58130512 · learning · v15→v16   Avoid removing the lowest-order n-grams (e.g., unigrams) from word-level features, as they often carry the most discriminative signal. If a score drop follows tightening, restore the original range before attributing the loss to other simultaneous changes. Change n-gram ranges independently from oth
    evidence: ✓ Lexical frequency or topic information is absent or dominated by very rare n-grams.
    leaderboard score n/a → 0.81644 (higher is better)
- expert 55987255 · learning · v1→v5   Test each dense representation (topic-model components, averaged word embeddings) individually by adding/removing it and checking the validation or leaderboard metric. Then combine the ones that each helped individually; complementary representations often stack well because they capture different a
    evidence: ✓ Lexical frequency or topic information is absent or dominated by very rare n-grams. | ✓ The current features lack contextual semantics and suitable pretrained encoders are available.
    leaderboard score 0.81691 → 0.81791 (higher is better; improved by 0.00100)
- expert 55987255 · learning · v124→v136   Sweep minimum document frequency upward in multiplicative steps (e.g., doubling) while watching validation; simultaneously lower maximum document frequency to remove ubiquitous tokens. Vary the n-gram range endpoints one at a time. After each change, check CV; if no improvement after several steps i
    evidence: ✓ Lexical frequency or topic information is absent or dominated by very rare n-grams. | ✓ The target depends on document structure or language quality not explicitly represented.
    leaderboard score n/a → n/a (higher is better)
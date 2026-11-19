# Tune sparse and latent text representations  `T.3.1.4`   4 edits, 0 experts
1 scored cases (improvement signed by each competition's direction), median +0.00100, 1 improved


- expert 59253662 · learning · v10→v11   Fix the number of topics to a small explicit value rather than using automatic selection, so features are stable across train and test. Use locally cached embedding checkpoints to avoid download failures and ensure reproducibility. Adjust clustering granularity to roughly match the number of target 
    evidence: ✗ The task predicts entities with repeated time-ordered records but uses only one record or a narrow summary. | ✓ Useful text variation is lexical or topical and the current vocabulary filters discard it. | ✓ A pretrained encoder is available and existing lexical features miss semantic similarity.
    leaderboard score n/a → 0.78393 (higher is better)
- expert 58130512 · learning · v15→v16   Avoid removing the lowest-order n-grams (e.g., unigrams) from word-level features, as they often carry the most discriminative signal. If a score drop follows tightening, restore the original range before attributing the loss to other simultaneous changes. Change n-gram ranges independently from oth
    evidence: ✗ The task predicts entities with repeated time-ordered records but uses only one record or a narrow summary. | ✓ Useful text variation is lexical or topical and the current vocabulary filters discard it.
    leaderboard score n/a → 0.81644 (higher is better)
- expert 55987255 · learning · v1→v5   Test each dense representation (topic-model components, averaged word embeddings) individually by adding/removing it and checking the validation or leaderboard metric. Then combine the ones that each helped individually; complementary representations often stack well because they capture different a
    evidence: ✓ Useful text variation is lexical or topical and the current vocabulary filters discard it. | ✗ The task predicts entities with repeated time-ordered records but uses only one record or a narrow summary. | ✓ A pretrained encoder is available and existing lexical features miss semantic similarity.
    leaderboard score 0.81691 → 0.81791 (higher is better; improved by 0.00100)
- expert 55987255 · learning · v124→v136   Sweep minimum document frequency upward in multiplicative steps (e.g., doubling) while watching validation; simultaneously lower maximum document frequency to remove ubiquitous tokens. Vary the n-gram range endpoints one at a time. After each change, check CV; if no improvement after several steps i
    evidence: ✗ The task predicts entities with repeated time-ordered records but uses only one record or a narrow summary. | ✓ Useful text variation is lexical or topical and the current vocabulary filters discard it. | ✓ Document quality depends on length, organization or language statistics not exposed by current representations.
    leaderboard score n/a → n/a (higher is better)
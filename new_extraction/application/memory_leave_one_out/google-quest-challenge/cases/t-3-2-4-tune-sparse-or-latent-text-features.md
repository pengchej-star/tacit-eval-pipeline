# Tune sparse or latent text features  `T.3.2.4`   4 edits, 0 experts
1 scored cases, median improvement +0.00100, 1 improved


- expert 59253662 (Contributor) · learning · v10→v11   Fix the number of topics to a small explicit value rather than using automatic selection, so features are stable across train and test. Use locally cached embedding checkpoints to avoid download failures and ensure reproducibility. Adjust clustering granularity to roughly match the number of target 
    evidence: ✓ Sparse text features are noisy, overly narrow, or too high-dimensional for the downstream learner. | ✓ Available pretrained representations encode information missing from the current tabular features.
    leaderboard score n/a → 0.78393
- expert 58130512 (Master) · learning · v15→v16   Avoid removing the lowest-order n-grams (e.g., unigrams) from word-level features, as they often carry the most discriminative signal. If a score drop follows tightening, restore the original range before attributing the loss to other simultaneous changes. Change n-gram ranges independently from oth
    evidence: ✓ Sparse text features are noisy, overly narrow, or too high-dimensional for the downstream learner.
    leaderboard score n/a → 0.81644
- expert 55987255 (Master) · learning · v1→v5   Test each dense representation (topic-model components, averaged word embeddings) individually by adding/removing it and checking the validation or leaderboard metric. Then combine the ones that each helped individually; complementary representations often stack well because they capture different a
    evidence: ✓ Sparse text features are noisy, overly narrow, or too high-dimensional for the downstream learner. | ✓ Available pretrained representations encode information missing from the current tabular features.
    leaderboard score 0.81691 → 0.81791 (+0.00100)
- expert 55987255 (Master) · learning · v124→v136   Sweep minimum document frequency upward in multiplicative steps (e.g., doubling) while watching validation; simultaneously lower maximum document frequency to remove ubiquitous tokens. Vary the n-gram range endpoints one at a time. After each change, check CV; if no improvement after several steps i
    evidence: ✓ Sparse text features are noisy, overly narrow, or too high-dimensional for the downstream learner. | ✓ Several trained input branches exist and one may add little or harmful information.
    leaderboard score n/a → n/a
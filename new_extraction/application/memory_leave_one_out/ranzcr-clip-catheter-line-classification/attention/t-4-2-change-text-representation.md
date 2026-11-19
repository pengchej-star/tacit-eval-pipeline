# [Change text representation › Which missing text signal should be exposed to the learner?]   141 visits, 16 experts

options: Tune sparse lexical features (2) | Add pretrained embeddings (16) | Add structural text features (17) | Tune compressed text representations (1) | Change text cleaning or input framing (16) | Add retrieval-derived signal (2) | Use generated score features (1)

check first: E66 Text length, structure, or linguistic quality is relevant but absent from current features.  imp 0.85 → +Add structural text features  [first in 50/60 visits that checked it]
then:        E68 Formatting, metadata, or input truncation may obscure task-relevant content.  imp 0.70 → +Change text cleaning or input framing  [first in 39/46 visits that checked it]
then:        E65 The current representation has lexical features but little contextual semantic information.  imp 0.80 → +Add pretrained embeddings  [first in 35/53 visits that checked it]
more:         4 further checks (E64, E67, E69, E70), load on request
enough when:  top option >= 36% (lower quartile over 140 visits) or >= 18 points ahead; median 1 checks
come back:    after 'after a new best' (2/5); after '3 scored steps without a new best' (1/5); after 'regression after a bundled change' (1/5)  [5 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 93% of visits
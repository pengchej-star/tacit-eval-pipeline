# [Choose a new feature source › Which missing information should be represented explicitly?]   186 visits, 20 experts

options: Expand entity summary features (18) | Add domain interactions and metadata (9) | Add text structure and linguistic statistics (12) | Tune sparse and latent text representations (4) | Use frozen pretrained embeddings (16) | Add cross-fitted prediction features (8)

check first: E33 The task predicts entities with repeated time-ordered records but uses only one record or a narrow summary.  imp 0.85 → +Expand entity summary features  [first in 129/169 visits that checked it]
then:        E35 Document quality depends on length, organization or language statistics not exposed by current representations.  imp 0.70 → +Add text structure and linguistic statistics  [first in 15/108 visits that checked it]
then:        E37 A pretrained encoder is available and existing lexical features miss semantic similarity.  imp 0.70 → +Use frozen pretrained embeddings  [first in 12/97 visits that checked it]
more:         4 further checks (E38, E34, E36, E39), load on request
enough when:  top option >= 50% (lower quartile over 186 visits) or >= 24 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (2/3); after '3 scored steps without a new best' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 87% of visits
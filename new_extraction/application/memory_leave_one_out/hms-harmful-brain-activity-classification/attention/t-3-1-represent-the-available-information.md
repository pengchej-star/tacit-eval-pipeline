# [Represent the available information › Which representation should I test for the available raw information?]   302 visits, 33 experts

options: Add entity-history summaries (8) | Add temporal deviation or window features (8) | Add targeted domain interactions (5) | Add text structure and linguistic statistics (15) | Tune sparse text representations (5) | Add frozen semantic embeddings (21) | Add leakage-free auxiliary predictions (14) | Encode metadata or paired text explicitly (7) | Test minimal versus domain-specific text cleaning (9) | Test numeric preprocessing against native handling (9) | Match and sweep image resolution (13) | Match image normalization to training (5) | Adjust sequence truncation (1)

check first: E27 Several observations belong to one prediction entity and only a small summary is currently used.  imp 0.82 → +Add entity-history summaries  [first in 53/60 visits that checked it]
then:        E30 Text structure or error patterns vary with the target beyond the current representation.  imp 0.70 → +Add text structure and linguistic statistics  [first in 45/62 visits that checked it]
then:        E32 Semantic embeddings are absent, or existing embedding sources have uncertain marginal value.  imp 0.72 → +Add frozen semantic embeddings  [first in 43/60 visits that checked it]
more:         10 further checks (E33, E35, E37, E29, E31, E34, E36, E38, E28, E39), load on request
enough when:  top option >= 20% (lower quartile over 302 visits) or >= 8 points ahead; median 1 checks
come back:    after 'after a new best' (4/16); after 'regression after a single change' (3/16); after 'other' (3/16)  [16 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 89% of visits
# [Represent repeated or structured records › Which structured feature construction should I test?]   75 visits, 10 experts

options: Add entity-level summary statistics (6) | Add temporal changes or recent windows (4) | Add domain interactions (5) | Change numeric precision or scaling (4) | Change missing-value handling (4) | Add structured metadata (3)

check first: E49 There are multiple observations per entity but the model sees only a latest row or a narrow summary.  imp 0.72 → +Add entity-level summary statistics  [first in 54/63 visits that checked it]
then:        E51 Related measurements have interpretable differences, ratios, or interactions absent from the feature set.  imp 0.80 → +Add domain interactions  [first in 7/24 visits that checked it]
then:        E52 Stored precision, scaling, or noisy decimals are unsuitable for the learner.  imp 0.55 → +Change numeric precision or scaling  [first in 6/19 visits that checked it]
more:         3 further checks (E54, E53, E50), load on request
enough when:  top option >= 34% (lower quartile over 75 visits) or >= 8 points ahead; median 2 checks
come back:    after 'other' (2/4); after '2 scored steps without a new best' (1/4); after 'regression after a single change' (1/4)  [4 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 75% of visits
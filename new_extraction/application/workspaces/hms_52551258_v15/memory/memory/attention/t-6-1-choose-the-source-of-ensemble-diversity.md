# [Choose the source of ensemble diversity › What kind of additional predictor should I test?]   269 visits, 45 experts

options: Add a different model family (44) | Add an alternative input representation (16) | Add an alternative supervision recipe (12) | Average more fold or snapshot predictions (56) | Average independently seeded models (14) | Average checkpoint weights (1)

check first: E114 Current members share a family and their held-out errors are highly correlated.  imp 0.70 → +Add a different model family  [first in 201/213 visits that checked it]
then:        E117 Compatible unused fold or snapshot predictions are already available.  imp 0.85 → +Average more fold or snapshot predictions  [first in 34/163 visits that checked it]
then:        E115 A relevant modality, feature set, or preprocessing view is not represented.  imp 0.80 → +Add an alternative input representation  [first in 23/72 visits that checked it]
more:         3 further checks (E116, E118, E119), load on request
enough when:  top option >= 37% (lower quartile over 269 visits) or >= 14 points ahead; median 2 checks
come back:    after 'after a new best' (8/20); after '2 scored steps without a new best' (4/20); after '4+ scored steps without a new best' (3/20)  [20 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 64% of visits
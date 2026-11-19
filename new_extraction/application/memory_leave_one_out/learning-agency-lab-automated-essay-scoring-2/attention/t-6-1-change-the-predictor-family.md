# [Change the predictor family › What kind of predictor change fits the current data and available artifacts?]   59 visits, 20 experts

options: Compare a different model family (6) | Change the pretrained backbone (7) | Change backbone capacity (10) | Fit a regressor on fixed embeddings (2) | Add a retrieval predictor (2) | Compare boosting variants (4)

check first: E120 The current family has plateaued despite useful features and controlled tuning.  imp 0.70 → +Compare a different model family  [first in 31/35 visits that checked it]
then:        E121 A domain-relevant or structurally different pretrained backbone is available.  imp 0.80 → +Change the pretrained backbone  [first in 10/23 visits that checked it]
then:        E122 Capacity appears limiting or a smaller model may meet the same quality target.  imp 0.75 → +Change backbone capacity  [first in 9/19 visits that checked it]
more:         6 further checks (E291, E125, E124, E292, E293, E123), load on request
enough when:  top option >= 31% (lower quartile over 59 visits) or >= 6 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (2/3); after '3 scored steps without a new best' (1/3)  [3 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 64% of visits
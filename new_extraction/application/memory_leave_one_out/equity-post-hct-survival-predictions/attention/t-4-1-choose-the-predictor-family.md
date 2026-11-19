# [Choose the predictor family › What kind of predictor change addresses the current limitation?]   124 visits, 25 experts

options: Replace the pretrained backbone (28) | Replace the tabular learner (10) | Change pooling or the prediction head (18) | Change feature fusion (4)

check first: E52 A suitable alternative pretrained family or size is available and current representation quality has plateaued.  imp 0.90 → +Replace the pretrained backbone  [first in 56/62 visits that checked it]
then:        E54 The backbone is strong but pooling or task heads may discard useful information.  imp 0.88 → +Change pooling or the prediction head  [first in 35/41 visits that checked it]
then:        E53 The same feature matrix supports a learner with a different inductive bias or boosting strategy.  imp 0.85 → +Replace the tabular learner  [first in 25/26 visits that checked it]
more:         1 further checks (E55), load on request
enough when:  top option >= 66% (lower quartile over 124 visits) or >= 51 points ahead; median 1 checks
come back:    after '4+ scored steps without a new best' (2/5); after 'regression after a single change' (1/5); after 'other' (1/5)  [5 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 96% of visits
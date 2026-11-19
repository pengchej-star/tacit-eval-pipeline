# [Change how the model is fitted › Which training change addresses the observed learning failure?]   171 visits, 33 experts

options: Transform the learning target (12) | Change the training target or objective (12) | Change tree depth or leaf capacity (15) | Tune model regularization (11) | Tune optimization and training duration (24) | Tune training augmentation strength (3)

check first: E69 Training improves while validation degrades as model complexity or feature count grows.  imp 0.80 → +Tune model regularization  [first in 41/55 visits that checked it]
then:        E70 Training stops while validation is still improving or a lower learning rate has not been given enough rounds.  imp 0.80 → +Tune optimization and training duration  [first in 39/64 visits that checked it]
then:        E66 Observed outcomes are censored, group-conditioned or encoded on a scale poorly matched to direct regression.  imp 0.60 → +Transform the learning target  [first in 26/27 visits that checked it]
more:         4 further checks (E67, E71, E68, E72), load on request
enough when:  top option >= 36% (lower quartile over 146 visits) or >= 16 points ahead; median 1 checks
come back:    after 'after a new best' (7/19); after 'other' (6/19); after '4+ scored steps without a new best' (3/19)  [19 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 71% of visits
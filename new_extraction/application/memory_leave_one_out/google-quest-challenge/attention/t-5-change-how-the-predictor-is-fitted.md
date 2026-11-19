# [Change how the predictor is fitted › Which training control should be changed next?]   194 visits, 27 experts

options: Tune tree capacity (19) | Tune regularization (10) | Tune optimizer and learning schedule (10) | Tune training duration (6) | Change the training objective (7) | Change target construction (11) | Change the boosting procedure (7) | Standardize per-fold fitting (4)

check first: E77 Training fit exceeds validation fit or newly added features increase instability.  imp 0.68 → +Tune regularization  [first in 64/79 visits that checked it]
then:        E76 Tree models show underfitting or overfitting associated with depth or leaf count.  imp 0.72 → +Tune tree capacity  [first in 41/45 visits that checked it]
then:        E79 Training stops before convergence or continues after validation deterioration.  imp 0.75 → +Tune training duration  [first in 20/42 visits that checked it]
more:         6 further checks (E78, E81, E80, E82, E84, E83), load on request
enough when:  top option >= 29% (lower quartile over 189 visits) or >= 12 points ahead; median 1 checks
come back:    after 'other' (8/20); after 'after a new best' (5/20); after '2 scored steps without a new best' (2/20)  [20 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 80% of visits
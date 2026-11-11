# [Change how the model is trained › Which training control addresses the observed fitting problem?]   184 visits, 28 experts

options: Change tree capacity or regularization (34) | Change neural optimization or regularization (16) | Change loss or example weighting (14) | Tune stopping and training duration (8)

check first: E111 A tree learner is limited by capacity, regularization, or boosting convergence.  imp 0.95 → +Change tree capacity or regularization  [first in 115/121 visits that checked it]
then:        E113 The loss or weighting does not match label semantics or the evaluated population.  imp 0.75 → +Change loss or example weighting  [first in 30/56 visits that checked it]
then:        E112 A neural learner shows unstable optimization or a training–validation gap.  imp 0.90 → +Change neural optimization or regularization  [first in 20/119 visits that checked it]
more:         1 further checks (E114), load on request
enough when:  top option >= 62% (lower quartile over 178 visits) or >= 45 points ahead; median 2 checks
come back:    after 'other' (4/12); after 'after a new best' (2/12); after 'regression after a bundled change' (2/12)  [12 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 93% of visits
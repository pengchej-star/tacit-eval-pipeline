# [Choose repeated predictors › Which kind of replication should reduce prediction variance?]   200 visits, 25 experts

options: Select and average fold checkpoints (41) | Average independent training runs (22) | Average valid transformed views (25) | Control inference stochasticity (8)

check first: E92 Available fold checkpoints differ in quality or some are currently unused.  imp 0.72 → +Select and average fold checkpoints  [first in 112/121 visits that checked it]
then:        E94 The task has valid input symmetries or multiple aligned views of the same target.  imp 0.82 → +Average valid transformed views  [first in 42/53 visits that checked it]
then:        E93 Independent training seeds produce materially different errors.  imp 0.78 → +Average independent training runs  [first in 31/41 visits that checked it]
more:         3 further checks (E95, E97, E96), load on request
enough when:  top option >= 50% (lower quartile over 199 visits) or >= 27 points ahead; median 2 checks
come back:    after 'after a new best' (5/9); after '2 scored steps without a new best' (2/9); after 'regression after a single change' (2/9)  [9 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 88% of visits
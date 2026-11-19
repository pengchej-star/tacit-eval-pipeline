# [Choose the training adjustment › Which training limitation is visible in the current fit?]   275 visits, 35 experts

options: Tune tree structure (14) | Tune regularization and subsampling (12) | Tune learning rate and optimizer (13) | Tune training duration and stopping (10) | Select a compatible trained checkpoint (46)

check first: E62 Several compatible snapshots already exist but have not been compared under one inference configuration.  imp 0.70 → +Select a compatible trained checkpoint  [first in 123/130 visits that checked it]
then:        E59 Generalization degrades despite adequate convergence and a fixed feature set.  imp 0.75 → +Tune regularization and subsampling  [first in 68/90 visits that checked it]
then:        E60 Loss is unstable or learning is too slow at the current step size.  imp 0.80 → +Tune learning rate and optimizer  [first in 28/84 visits that checked it]
more:         2 further checks (E58, E61), load on request
enough when:  top option >= 46% (lower quartile over 267 visits) or >= 11 points ahead; median 1 checks
come back:    after 'other' (4/11); after 'after a new best' (3/11); after '2 scored steps without a new best' (2/11)  [11 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 75% of visits
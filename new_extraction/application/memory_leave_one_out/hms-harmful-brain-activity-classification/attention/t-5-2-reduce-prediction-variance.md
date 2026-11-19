# [Reduce prediction variance › Which repetition adds useful independent information?]   95 visits, 20 experts

options: Average more cross-validation folds (26) | Average independent training seeds (16) | Average valid transformed input views (8) | Evaluate stochastic dropout inference (4) | Average compatible training snapshots (1)

check first: E78 Useful fold-trained checkpoints are omitted or too few folds limit training coverage.  imp 0.82 → +Average more cross-validation folds  [first in 53/56 visits that checked it]
then:        E79 Predictions vary across trained seeds beyond the expected evaluation noise.  imp 0.78 → +Average independent training seeds  [first in 23/28 visits that checked it]
then:        E80 The task is invariant to candidate transformations and predictions vary across those views.  imp 0.80 → +Average valid transformed input views  [first in 10/14 visits that checked it]
more:         2 further checks (E81, E82), load on request
enough when:  top option >= 46% (lower quartile over 94 visits) or >= 25 points ahead; median 1 checks
come back:    after 'after a new best' (2/5); after 'regression after a single change' (1/5); after '2 scored steps without a new best' (1/5)  [5 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 93% of visits
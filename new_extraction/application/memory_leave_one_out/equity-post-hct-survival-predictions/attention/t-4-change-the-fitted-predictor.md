# [Change the fitted predictor › Which part of the predictor should I replace or retune?]   423 visits, 45 experts

options: Choose the predictor family (60) | Choose the training signal (12) | Choose the training adjustment (95)

check first: E65 The family is suitable but capacity, convergence, or checkpoint selection remains unresolved.  imp 0.90 → +Choose the training adjustment  [first in 209/315 visits that checked it]
then:        E63 The current representation or inductive bias limits quality despite a converged fit.  imp 0.85 → +Choose the predictor family  [first in 165/181 visits that checked it]
then:        E64 Target construction or the loss is poorly aligned with the label and metric semantics.  imp 0.80 → +Choose the training signal  [first in 36/79 visits that checked it]
more:         2 further checks (E168, E169), load on request
enough when:  top option >= 76% (lower quartile over 417 visits) or >= 60 points ahead; median 2 checks
come back:    after 'other' (4/15); after '2 scored steps without a new best' (4/15); after 'after a new best' (3/15)  [15 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 94% of visits
# [Choose validation membership › Which validation partition best represents the prediction setting?]   53 visits, 8 experts

options: Preserve target balance (3) | Keep related examples together (5) | Validate on the target population (5) | Adjust holdout or fold design (5)

check first: E16 Rows share an entity, prompt, overlapping window, or other dependence that would cross random folds.  imp 0.90 → +Keep related examples together  [first in 19/30 visits that checked it]
then:        E17 A known training subpopulation resembles the test population more than the rest.  imp 0.70 → +Validate on the target population  [first in 13/38 visits that checked it]
then:        E18 The holdout removes a large share of usable training data or nested folds duplicate expensive fitting.  imp 0.60 → +Adjust holdout or fold design  [first in 9/16 visits that checked it]
more:         6 further checks (E143, E15, E147, E145, E144, E146), load on request
enough when:  top option >= 42% (lower quartile over 53 visits) or >= 9 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (1/2); after 'regression after a single change' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 57% of visits
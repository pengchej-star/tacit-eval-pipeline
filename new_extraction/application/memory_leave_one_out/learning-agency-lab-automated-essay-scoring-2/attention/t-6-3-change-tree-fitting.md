# [Change tree fitting › What tree-fitting change should be tested next?]   93 visits, 10 experts

options: Sweep tree depth or leaf capacity (11) | Tune tree regularization (5) | Introduce row and feature sampling (1) | Couple learning rate and boosting budget (6) | Reduce per-member boosting duration (1)

check first: E131 Training improves while validation stagnates under the current tree capacity.  imp 0.90 → +Tune tree regularization  [first in 43/46 visits that checked it]
then:        E130 Training fit is poor under shallow trees or prior depth changes show a clear capacity effect.  imp 0.95 → +Sweep tree depth or leaf capacity  [first in 23/29 visits that checked it]
then:        E133 Lower learning rates reach the round cap or trigger stopping before sustained convergence.  imp 0.90 → +Couple learning rate and boosting budget  [first in 16/29 visits that checked it]
more:         2 further checks (E134, E132), load on request
enough when:  top option >= 54% (lower quartile over 90 visits) or >= 34 points ahead; median 2 checks
come back:    after 'after a new best' (2/4); after '2 scored steps without a new best' (1/4); after 'other' (1/4)  [4 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 74% of visits
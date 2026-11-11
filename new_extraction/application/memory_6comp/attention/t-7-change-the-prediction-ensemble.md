# [Change the prediction ensemble › Which ensemble intervention is supported by the available predictions?]   1060 visits, 54 experts

options: Change ensemble membership (262) | Change the combination rule (147) | Change repeated-model aggregation (90)

check first: E134 New or redundant prediction sources exist whose marginal contribution is unknown.  imp 0.85 → +Change ensemble membership  [first in 774/800 visits that checked it]
then:        E135 The prediction sources are fixed but weighting or output-scale handling is unvalidated.  imp 0.75 → +Change the combination rule  [first in 143/453 visits that checked it]
then:        E136 Compatible fold, seed, or input-view predictions can reduce observed variance.  imp 0.70 → +Change repeated-model aggregation  [first in 113/296 visits that checked it]
more:         4 further checks (E285, E286, E283, E284), load on request
enough when:  top option >= 65% (lower quartile over 1057 visits) or >= 37 points ahead; median 2 checks
come back:    after 'regression after a single change' (6/28); after 'after a new best' (6/28); after 'other' (5/28)  [28 returns, 10 improved the score]

scores: LLM-guessed; top option matches the option taken in 80% of visits
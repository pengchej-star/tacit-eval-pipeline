# [Change inference or output adjustment › What residual prediction problem can be addressed without changing the base training data?]   145 visits, 25 experts

options: Change inference averaging (32) | Change output calibration (14) | Change output granularity (17) | Change structured output corrections (14)

check first: E177 Validated symmetries or unintended stochastic inference could explain residual variance.  imp 0.85 → +Change inference averaging  [first in 45/50 visits that checked it]
then:        E179 Discrete target support or degenerate ties affect the ranking metric.  imp 0.70 → +Change output granularity  [first in 34/43 visits that checked it]
then:        E178 Prediction bias, scale, or probability mass conflicts with the output requirements or validation labels.  imp 0.80 → +Change output calibration  [first in 25/31 visits that checked it]
more:         2 further checks (E180, E335), load on request
enough when:  top option >= 44% (lower quartile over 140 visits) or >= 19 points ahead; median 1 checks
come back:    after 'after a new best' (3/7); after 'regression after a single change' (2/7); after '2 scored steps without a new best' (1/7)  [7 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 94% of visits
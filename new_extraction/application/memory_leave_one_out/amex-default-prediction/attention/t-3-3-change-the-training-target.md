# [Change the training target › Which target representation fits the outcome and scoring rule?]   14 visits, 7 experts

options: Transform censored outcomes (6) | Estimate targets within groups (2) | Center the regression target (1)

check first: E60 Outcomes include both event times and censoring indicators.  imp 0.95 → +Transform censored outcomes  [first in 12/14 visits that checked it]
then:        E61 The metric evaluates named groups separately and group survival distributions differ.  imp 0.85 → +Estimate targets within groups  [first in 1/14 visits that checked it]
then:        E62 Continuous regression targets have fold-dependent offsets and are not censored outcomes.  imp 0.90 → +Center the regression target  [first in 1/11 visits that checked it]
more:         3 further checks (E282, E283, E63), load on request
enough when:  top option >= 66% (lower quartile over 14 visits) or >= 32 points ahead; median 4 checks
come back:    after 'other' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 79% of visits
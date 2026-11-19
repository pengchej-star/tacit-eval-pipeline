# [Choose the fitting objective › Which target or objective change is supported by the metric?]   47 visits, 14 experts

options: Compare censoring-aware target transforms (8) | Test consistent target centering (1) | Compare loss functions or objective parameters (7) | Choose the early-stopping metric (7) | Choose a training interface with required controls (4)

check first: E56 Outcomes contain censoring or the metric evaluates risk ranking within known subgroups.  imp 0.95 → +Compare censoring-aware target transforms  [first in 18/30 visits that checked it]
then:        E59 The best epoch or iteration under the current stopping metric is not best under the target metric.  imp 0.85 → +Choose the early-stopping metric  [first in 11/15 visits that checked it]
then:        E60 The current API obscures required probability output or evaluation controls.  imp 0.70 → +Choose a training interface with required controls  [first in 7/13 visits that checked it]
more:         8 further checks (E58, E57, E145, E149, E150, E146, E148, E147), load on request
enough when:  top option >= 51% (lower quartile over 47 visits) or >= 37 points ahead; median 3 checks
come back:    after 'other' (2/5); after 'after a new best' (2/5); after '4+ scored steps without a new best' (1/5)  [5 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 89% of visits
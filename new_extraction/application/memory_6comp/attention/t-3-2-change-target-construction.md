# [Change target construction › What target representation should the learner optimize?]   17 visits, 7 experts

options: Transform censored outcomes (3) | Construct subgroup-aware targets (2) | Choose an ordinal prediction formulation (2) | Tune target scaling or centering (3)

check first: E54 Some observed times are censored rather than completed events.  imp 0.85 → +Transform censored outcomes  [first in 10/17 visits that checked it]
then:        E55 The score explicitly aggregates performance across groups with different outcome distributions.  imp 0.55 → +Construct subgroup-aware targets  [first in 3/17 visits that checked it]
then:        E57 The existing target transform includes tunable scaling or centering constants.  imp 0.60 → +Tune target scaling or centering  [first in 2/14 visits that checked it]
more:         1 further checks (E56), load on request
enough when:  top option >= 50% (lower quartile over 17 visits) or >= 26 points ahead; median 4 checks
come back:    after 'other' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 53% of visits
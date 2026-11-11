# [Change the information presented to the model › Which input representation should be changed next?]   462 visits, 33 experts

options: Change repeated-record summaries (18) | Change text representation (55) | Change signal or image representation (46) | Change feature retention or preprocessing (59)

check first: E83 The prediction unit has repeated dated tabular observations.  imp 0.92 → +Change repeated-record summaries  [first in 243/333 visits that checked it]
then:        E85 Inputs include raw signals or images derived from signals.  imp 0.88 → +Change signal or image representation  [first in 120/446 visits that checked it]
then:        E86 The current feature matrix is large, sparse, or processed inconsistently with the learner.  imp 0.65 → +Change feature retention or preprocessing  [first in 48/164 visits that checked it]
more:         6 further checks (E84, E218, E217, E216, E219, E220), load on request
enough when:  top option >= 70% (lower quartile over 460 visits) or >= 52 points ahead; median 4 checks
come back:    after 'other' (2/6); after 'after a new best' (2/6); after 'regression after a bundled change' (1/6)  [6 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 79% of visits
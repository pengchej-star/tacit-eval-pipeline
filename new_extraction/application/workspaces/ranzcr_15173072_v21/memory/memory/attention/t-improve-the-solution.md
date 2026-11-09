# [Improve the solution › what can I change to improve my solution?]   3939 visits, 70 experts

options: Improve the evidence for choosing changes (307) | Repair incorrect or mismatched predictions (186) | Change the information presented to the model (183) | Change training examples or targets (42) | Change the learned model (131) | Change the prediction pool (360) | Change prediction combination or output mapping (309) | Make useful experiments feasible (156)

check first: E01 The current predictions fail a schema, signal, or compatibility check.  imp 0.75 → +Repair incorrect or mismatched predictions  [first in 1539/2311 visits that checked it]
then:        E07 Valid cached predictions exist and output mapping or blending is not yet compared on held-out data.  imp 0.72 → +Change prediction combination or output mapping  [first in 535/1154 visits that checked it]
then:        E02 The claimed gain is no larger than variation in prior unchanged runs.  imp 0.55 → +Improve the evidence for choosing changes  [first in 415/1071 visits that checked it]
more:         5 further checks (E08, E06, E05, E04, E03), load on request
enough when:  top option >= 26% (lower quartile over 3422 visits) or >= 4 points ahead; median 2 checks
come back:    after 'other' (16/31); after '2 scored steps without a new best' (5/31); after '4+ scored steps without a new best' (4/31)  [31 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 33% of visits
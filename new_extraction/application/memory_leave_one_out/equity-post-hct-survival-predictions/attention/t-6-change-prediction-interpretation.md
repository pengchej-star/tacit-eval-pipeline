# [Change prediction interpretation › Which output adjustment matches the observed error and metric?]   117 visits, 16 experts

options: Map outputs to discrete targets (41) | Correct continuous outputs (17)

check first: E90 The required labels are discrete or the rank metric is sensitive to ties created by target granularity.  imp 0.92 → +Map outputs to discrete targets  [first in 107/113 visits that checked it]
then:        E185 The evaluation metric is invariant to monotonic transformations of predictions, so scale changes should not affect the score.  imp 0.70 → +Map outputs to discrete targets  [first in 4/109 visits that checked it]
then:        E91 Valid continuous or probability predictions have a reproducible calibration or subgroup bias.  imp 0.55 → +Correct continuous outputs  [first in 3/41 visits that checked it]
more:         6 further checks (E190, E189, E186, E184, E187, E188), load on request
enough when:  top option >= 76% (lower quartile over 117 visits) or >= 51 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (1/2); after '2 scored steps without a new best' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 86% of visits
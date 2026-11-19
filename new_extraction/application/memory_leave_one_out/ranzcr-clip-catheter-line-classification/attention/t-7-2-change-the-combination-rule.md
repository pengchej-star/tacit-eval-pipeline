# [Change the combination rule › Which rule should combine the available prediction sources?]   341 visits, 37 experts

options: Use equal averaging (5) | Tune positive blend weights (80) | Give a weak auxiliary model little weight (13) | Test signed blend weights (2) | Fit an out-of-fold meta-learner (18) | Change meta-learner complexity (10) | Normalize ranks before blending (16) | Choose probability or logit blending (3)

check first: E120 Components have unequal validated quality and their combination changes the metric.  imp 0.80 → +Tune positive blend weights  [first in 208/250 visits that checked it]
then:        E125 The metric depends on ordering and member outputs have incompatible scales or outliers.  imp 0.68 → +Normalize ranks before blending  [first in 33/77 visits that checked it]
then:        E119 Component quality is similar and fitted weights are unstable across validation folds.  imp 0.72 → +Use equal averaging  [first in 30/41 visits that checked it]
more:         5 further checks (E123, E121, E124, E126, E122), load on request
enough when:  top option >= 25% (lower quartile over 340 visits) or >= 4 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (4/14); after 'other' (4/14); after 'after a new best' (3/14)  [14 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 59% of visits
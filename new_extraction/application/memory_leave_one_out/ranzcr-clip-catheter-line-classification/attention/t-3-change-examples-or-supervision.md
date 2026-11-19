# [Change examples or supervision › Which part of the training evidence should change?]   74 visits, 14 experts

options: Change training membership (21) | Change target construction (10)

check first: E58 Available training rows differ in quality, source relevance, or labeling status.  imp 0.70 → +Change training membership  [first in 51/51 visits that checked it]
then:        E59 The learned target does not directly express censoring, ordering, or the subgroup objective.  imp 0.80 → +Change target construction  [first in 9/15 visits that checked it]
then:        E202 The model is currently trained on a subset of the available labeled data rather than the full labeled set.  imp 0.85 → +Change training membership  [first in 5/16 visits that checked it]
more:         3 further checks (E203, E205, E204), load on request
enough when:  top option >= 80% (lower quartile over 71 visits) or >= 60 points ahead; median 1 checks
come back:    after 'after a new best' (2/3); after '4+ scored steps without a new best' (1/3)  [3 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 93% of visits
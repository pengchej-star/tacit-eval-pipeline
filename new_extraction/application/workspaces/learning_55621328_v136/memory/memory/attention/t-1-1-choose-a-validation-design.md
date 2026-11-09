# [Choose a validation design › Which split design should I test for this data?]   35 visits, 9 experts

options: Preserve target proportions (3) | Hold related examples together (6) | Probe subgroup allocation (5) | Change holdout allocation (4)

check first: E14 A recognizable source subgroup differs from the evaluation population.  imp 0.72 → +Probe subgroup allocation  [first in 11/20 visits that checked it]
then:        E13 Multiple rows share an entity, source, or topic that should be unseen at evaluation.  imp 0.90 → +Hold related examples together  [first in 7/12 visits that checked it]
then:        E16 A large fixed holdout substantially reduces fitting data after model choices are settled.  imp 0.65 → +Change holdout allocation  [first in 5/7 visits that checked it]
more:         8 further checks (E191, E12, E195, E193, E15, E192, E194, E190), load on request
enough when:  top option >= 55% (lower quartile over 35 visits) or >= 27 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (2/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 77% of visits
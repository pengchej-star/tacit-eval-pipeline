# [Choose a model formulation › Which model formulation should I compare with the current one?]   139 visits, 30 experts

options: Compare pretrained backbones or capacities (42) | Compare boosting algorithms or libraries (5) | Change pooling, attention or prediction heads (17) | Compare regression, classification and ordinal outputs (4) | Probe direct language-model scoring (1)

check first: E51 Available backbones differ in capacity or domain pretraining relevant to the task.  imp 0.85 → +Compare pretrained backbones or capacities  [first in 80/88 visits that checked it]
then:        E53 A minimal or poorly matched prediction head limits an otherwise useful representation.  imp 0.65 → +Change pooling, attention or prediction heads  [first in 32/47 visits that checked it]
then:        E52 The tuned current tree method has plateaued and another boosting implementation is available.  imp 0.75 → +Compare boosting algorithms or libraries  [first in 20/52 visits that checked it]
more:         2 further checks (E54, E55), load on request
enough when:  top option >= 40% (lower quartile over 139 visits) or >= 20 points ahead; median 1 checks
come back:    after 'regression after a single change' (1/3); after 'other' (1/3); after '4+ scored steps without a new best' (1/3)  [3 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 84% of visits
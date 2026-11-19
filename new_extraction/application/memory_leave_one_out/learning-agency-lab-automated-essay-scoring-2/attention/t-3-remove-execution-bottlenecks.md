# [Remove execution bottlenecks › Which measured execution constraint is limiting useful experiments?]   151 visits, 33 experts

options: Reduce peak memory (25) | Shorten the iteration cycle (44) | Change the runtime interface (9)

check first: E51 Repeated loading, extraction, or full training dominates otherwise working experiments.  imp 0.75 → +Shorten the iteration cycle  [first in 73/85 visits that checked it]
then:        E50 Runs fail or slow sharply at a reproducible memory peak.  imp 0.70 → +Reduce peak memory  [first in 40/60 visits that checked it]
then:        E52 Device support or API limitations block a required operation.  imp 0.85 → +Change the runtime interface  [first in 16/41 visits that checked it]
more:         2 further checks (E230, E231), load on request
enough when:  top option >= 66% (lower quartile over 148 visits) or >= 46 points ahead; median 1 checks
come back:    after 'other' (4/11); after '4+ scored steps without a new best' (3/11); after 'regression after a bundled change' (1/11)  [11 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 98% of visits
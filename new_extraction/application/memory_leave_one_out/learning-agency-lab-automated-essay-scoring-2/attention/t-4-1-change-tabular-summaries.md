# [Change tabular summaries › Which information is missing from the current tabular summaries?]   67 visits, 6 experts

options: Inspect entity and feature structure (1) | Use a minimal entity summary (3) | Expand entity summary statistics (6) | Summarize recent history separately (1) | Add change-over-time features (3) | Add targeted interaction features (4) | Encode elapsed or calendar time (2)

check first: E71 The number and ordering of records per prediction entity are not yet established.  imp 0.85 → +Inspect entity and feature structure  [first in 21/38 visits that checked it]
then:        E72 No working entity-level feature baseline exists.  imp 0.80 → +Use a minimal entity summary  [first in 17/64 visits that checked it]
then:        E76 Domain-related columns have a meaningful ratio or deviation not present in the features.  imp 0.75 → +Add targeted interaction features  [first in 7/16 visits that checked it]
more:         19 further checks (E73, E244, E75, E77, E243, E246, E251, E256, E253, E252, E245, E247, E254, E257, E250, E255, E74, E248, E249), load on request
enough when:  top option >= 32% (lower quartile over 67 visits) or >= 10 points ahead; median 7 checks
come back:    after 'other' (3/5); after 'after a new best' (1/5); after '2 scored steps without a new best' (1/5)  [5 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 55% of visits
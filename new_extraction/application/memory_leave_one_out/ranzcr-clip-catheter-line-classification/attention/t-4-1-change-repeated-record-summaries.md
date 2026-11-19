# [Change repeated-record summaries › What representation should summarize repeated observations?]   61 visits, 7 experts

options: Build a minimal entity summary (2) | Add history summaries (5) | Add temporal contrasts (5) | Add domain interactions (6)

check first: E60 The current model uses raw repeated rows without an entity-level baseline.  imp 0.70 → +Build a minimal entity summary  [first in 49/61 visits that checked it]
then:        E62 Global summaries discard recency or the order of meaningful changes.  imp 0.65 → +Add temporal contrasts  [first in 9/45 visits that checked it]
then:        E61 Multiple observations exist but only one record per entity reaches the model.  imp 0.60 → +Build a minimal entity summary  [first in 3/59 visits that checked it]
more:         1 further checks (E63), load on request
enough when:  top option >= 44% (lower quartile over 61 visits) or >= 11 points ahead; median 3 checks
come back:    after '2 scored steps without a new best' (1/2); after 'other' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 74% of visits
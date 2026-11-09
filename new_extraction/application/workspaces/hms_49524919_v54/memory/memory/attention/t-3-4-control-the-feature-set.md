# [Control the feature set › Which feature-set reduction or refresh should I perform?]   139 visits, 16 experts

options: Ablate a feature family (32) | Estimate feature relevance (6) | Tune the retained feature count (13) | Recompute feature selection (6) | Reduce dense representation dimensions (4)

check first: E67 A newly added feature family coincided with worse held-out performance.  imp 0.82 → +Ablate a feature family  [first in 51/60 visits that checked it]
then:        E69 A ranking exists but its retention threshold is arbitrary or stale.  imp 0.70 → +Tune the retained feature count  [first in 42/65 visits that checked it]
then:        E70 Features were added or renamed after the saved selection file was generated.  imp 0.72 → +Recompute feature selection  [first in 14/50 visits that checked it]
more:         2 further checks (E68, E71), load on request
enough when:  top option >= 40% (lower quartile over 130 visits) or >= 15 points ahead; median 2 checks
come back:    after 'after a new best' (3/10); after 'other' (2/10); after '2 scored steps without a new best' (2/10)  [10 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 65% of visits
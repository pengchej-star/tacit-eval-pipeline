# [Change prediction combination or output mapping › Which operation on valid predictions should I change?]   662 visits, 55 experts

options: Choose a combination rule (60) | Choose how to weight predictors (112) | Choose meta-model inputs (24) | Map continuous scores to discrete labels (38) | Correct output semantics or bias (43) | Choose inference-time averaging (32)

check first: E130 The same valid prediction pool has only an arbitrary weight allocation.  imp 0.85 → +Choose how to weight predictors  [first in 277/336 visits that checked it]
then:        E132 The task requires discrete ordered outputs or labels occupy a few repeated levels.  imp 0.75 → +Map continuous scores to discrete labels  [first in 111/524 visits that checked it]
then:        E129 Prediction scales or the aggregation domain differ across members.  imp 0.72 → +Choose a combination rule  [first in 86/95 visits that checked it]
more:         8 further checks (E131, E306, E133, E134, E310, E308, E307, E309), load on request
enough when:  top option >= 37% (lower quartile over 652 visits) or >= 12 points ahead; median 3 checks
come back:    after 'after a new best' (11/39); after 'regression after a single change' (10/39); after '4+ scored steps without a new best' (8/39)  [39 returns, 11 improved the score]

scores: LLM-guessed; top option matches the option taken in 70% of visits
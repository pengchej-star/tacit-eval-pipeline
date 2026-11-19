# [Choose feature-set complexity › Should the next change prune, expand or ablate the current feature set?]   98 visits, 9 experts

options: Choose a ranked feature cutoff (24) | Expand the retained feature subset (4) | Remove or restore a feature group (10)

check first: E172 The expert is incrementally stepping through feature-selection cutoff values without a systematic grid search or recorded comparison of validation scores.  imp 0.60 → +Choose a ranked feature cutoff  [first in 28/65 visits that checked it]
then:        E41 A fixed cap or stale selection file excludes newly useful feature families.  imp 0.55 → +Expand the retained feature subset  [first in 26/40 visits that checked it]
then:        E40 Many current features have weak or unstable importance and the model overfits.  imp 0.72 → +Choose a ranked feature cutoff  [first in 17/19 visits that checked it]
more:         12 further checks (E42, E174, E176, E180, E181, E173, E182, E178, E175, E179, E177, E43), load on request
enough when:  top option >= 56% (lower quartile over 98 visits) or >= 23 points ahead; median 6 checks
come back:    after 'other' (2/6); after '4+ scored steps without a new best' (2/6); after 'after a new best' (1/6)  [6 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 73% of visits
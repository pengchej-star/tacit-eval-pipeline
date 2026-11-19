# [Choose validation membership › Which validation partition best answers the deployment question?]   53 visits, 13 experts

options: Keep related samples in the same fold (3) | Preserve label balance across folds (5) | Make validation represent the target population (1) | Change the holdout allocation (13) | Reproduce an overlapping-fold diagnostic (4) | Refit on all labeled data (1)

check first: E21 A recognizable training population has a different distribution from the intended test population.  imp 0.80 → +Make validation represent the target population  [first in 12/25 visits that checked it]
then:        E19 Multiple rows share a subject, entity, topic or near-duplicate source that can leak across folds.  imp 0.92 → +Keep related samples in the same fold  [first in 8/19 visits that checked it]
then:        E22 Current validation estimates fluctuate because each holdout has few informative examples.  imp 0.70 → +Change the holdout allocation  [first in 8/15 visits that checked it]
more:         20 further checks (E141, E20, E148, E142, E145, E23, E143, E154, E25, E26, E144, E150, E147, E24, E151, E155, E152, E146, E149, E153), load on request
enough when:  top option >= 37% (lower quartile over 53 visits) or >= 13 points ahead; median 5 checks
come back:    after '4+ scored steps without a new best' (3/6); after 'regression after a bundled change' (1/6); after 'other' (1/6)  [6 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 60% of visits
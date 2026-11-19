# [Change the cost of obtaining feedback › Which bottleneck should be removed to make the next experiment feasible?]   152 visits, 29 experts

options: Use a reduced development run (16) | Cache stable intermediate artifacts (19) | Process data in chunks (6) | Release models between stages (15) | Adjust inference batching (7) | Change numerical precision (3) | Optimize the computation backend (3) | Train folds across saved sessions (2)

check first: E36 Full folds or repetitions dominate development time before code correctness is established.  imp 0.82 → +Use a reduced development run  [first in 39/47 visits that checked it]
then:        E37 The expensive upstream computation is unchanged across downstream trials.  imp 0.78 → +Cache stable intermediate artifacts  [first in 27/42 visits that checked it]
then:        E39 Memory grows as successive models or framework stages are loaded.  imp 0.65 → +Release models between stages  [first in 22/42 visits that checked it]
more:         19 further checks (E38, E40, E196, E43, E194, E193, E189, E192, E41, E44, E42, E200, E201, E199, E195, E198, E197, E191, E190), load on request
enough when:  top option >= 30% (lower quartile over 152 visits) or >= 9 points ahead; median 3 checks
come back:    after 'other' (6/17); after '3 scored steps without a new best' (3/17); after 'after a new best' (3/17)  [17 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 80% of visits
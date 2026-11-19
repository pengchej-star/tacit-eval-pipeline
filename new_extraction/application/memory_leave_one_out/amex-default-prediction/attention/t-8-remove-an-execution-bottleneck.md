# [Remove an execution bottleneck › Which execution change enables more reliable or complete experiments?]   162 visits, 38 experts

options: Reduce peak resource use (26) | Reduce repeated work (61) | Pin stochastic execution (6)

check first: E192 Runtime is dominated by repeated preprocessing, incomplete-stage restarts, or a profiled slow operation.  imp 0.90 → +Reduce repeated work  [first in 89/100 visits that checked it]
then:        E191 The full run exceeds memory capacity or repeatedly fails on large batches.  imp 0.85 → +Reduce peak resource use  [first in 44/51 visits that checked it]
then:        E433 A variable deletion or comment-out removes a definition still referenced downstream, causing a runtime error.  imp 0.40 → +Reduce repeated work  [first in 9/35 visits that checked it]
more:         4 further checks (E193, E435, E434, E436), load on request
enough when:  top option >= 68% (lower quartile over 162 visits) or >= 49 points ahead; median 2 checks
come back:    after 'after a new best' (4/13); after '4+ scored steps without a new best' (3/13); after 'other' (3/13)  [13 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 90% of visits
# [Change training membership › Which examples should enter training?]   57 visits, 10 experts

options: Filter unreliable examples (8) | Add auxiliary labeled data (4) | Add pseudo-labeled examples (3) | Refit on more labeled data (3) | Resample the target population (3)

check first: E49 Specific training groups contain duplicate observations, unreliable labels, or a distribution absent at test time.  imp 0.82 → +Filter unreliable examples  [first in 21/27 visits that checked it]
then:        E50 Additional labeled data has compatible inputs and target semantics.  imp 0.88 → +Add auxiliary labeled data  [first in 8/17 visits that checked it]
then:        E51 Unlabeled examples and a validated teacher are available.  imp 0.80 → +Add pseudo-labeled examples  [first in 7/8 visits that checked it]
more:         12 further checks (E52, E208, E209, E53, E206, E207, E212, E215, E211, E210, E213, E214), load on request
enough when:  top option >= 37% (lower quartile over 57 visits) or >= 9 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (1/2); after 'after a new best' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 63% of visits
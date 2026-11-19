# [Shorten the iteration cycle › Which repeated work is slowing development?]   92 visits, 23 experts

options: Use a reduced development configuration (14) | Cache stable intermediate artifacts (11) | Train unfinished folds across sessions (2) | Accelerate rank post-processing (1) | Centralize variant configuration (16)

check first: E57 A full training run is currently needed just to test code wiring or screen a parameter.  imp 0.95 → +Use a reduced development configuration  [first in 32/35 visits that checked it]
then:        E61 Variant changes require repeated manual edits that have caused configuration drift.  imp 0.75 → +Centralize variant configuration  [first in 29/41 visits that checked it]
then:        E58 The expensive upstream outputs are unchanged across downstream experiments.  imp 0.85 → +Cache stable intermediate artifacts  [first in 20/26 visits that checked it]
more:         7 further checks (E59, E237, E236, E238, E60, E235, E239), load on request
enough when:  top option >= 45% (lower quartile over 92 visits) or >= 28 points ahead; median 2 checks
come back:    after 'other' (3/6); after 'regression after a single change' (2/6); after '4+ scored steps without a new best' (1/6)  [6 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 97% of visits
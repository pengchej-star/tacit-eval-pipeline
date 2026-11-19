# [Repair or accelerate execution › Should the next execution change correct outputs or reduce iteration overhead?]   619 visits, 56 experts

options: Repair the execution contract (154) | Make the pipeline practical to run (124)

check first: E11 The active pipeline crashes, produces invalid outputs or fails prediction parity against the working version.  imp 0.82 → +Repair the execution contract  [first in 524/582 visits that checked it]
then:        E12 Verified predictions are correct but measured runtime or peak memory prevents planned experiments.  imp 0.91 → +Make the pipeline practical to run  [first in 76/262 visits that checked it]
enough when:  top option >= 92% (lower quartile over 600 visits) or >= 83 points ahead; median 1 checks
come back:    after 'other' (9/21); after '4+ scored steps without a new best' (4/21); after 'regression after a single change' (3/21)  [21 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 90% of visits
# [Reuse trained weights differently › Which saved-weight choice is justified by the available artifacts?]   153 visits, 24 experts

options: Select a trained run (56) | Select the stopping snapshot (4) | Average compatible weights (1)

check first: E99 Several compatible runs differ in training procedure or seed and have not been compared consistently.  imp 0.75 → +Select a trained run  [first in 145/145 visits that checked it]
then:        E100 Final-epoch and best-validation snapshots differ and late training may overfit.  imp 0.80 → +Select the stopping snapshot  [first in 6/38 visits that checked it]
then:        E101 Several nearby snapshots from the same parameterization are available.  imp 0.70 → +Average compatible weights  [first in 2/23 visits that checked it]
more:         1 further checks (E102), load on request
enough when:  top option >= 50% (lower quartile over 153 visits) or >= 22 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (1/2); after 'after a new best' (1/2)  [2 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 39% of visits
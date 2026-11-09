# [Change the learned model › Which model-fitting change is the most plausible next intervention?]   296 visits, 46 experts

options: Choose a model family or initialization (36) | Change the prediction architecture (30) | Tune a tree learner (40) | Tune neural optimization or loss (25)

check first: E90 The active learner is a tree model with capacity or convergence problems.  imp 0.88 → +Tune a tree learner  [first in 127/258 visits that checked it]
then:        E88 A correctly implemented backbone or learner has plateaued across local tuning.  imp 0.72 → +Change the prediction architecture  [first in 59/86 visits that checked it]
then:        E91 The active component is neural and its optimization or loss is suspect.  imp 0.85 → +Tune neural optimization or loss  [first in 32/129 visits that checked it]
more:         11 further checks (E248, E89, E245, E247, E246, E249, E252, E254, E251, E253, E250), load on request
enough when:  top option >= 57% (lower quartile over 296 visits) or >= 30 points ahead; median 5 checks
come back:    after 'regression after a single change' (3/11); after 'other' (3/11); after '2 scored steps without a new best' (2/11)  [11 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 70% of visits
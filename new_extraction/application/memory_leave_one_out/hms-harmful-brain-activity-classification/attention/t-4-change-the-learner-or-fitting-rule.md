# [Change the learner or fitting rule › Which modeling constraint should I change next?]   304 visits, 46 experts

options: Choose a model formulation (69) | Choose the fitting objective (27) | Adjust training dynamics (50)

check first: E68 The existing formulation has plateaued and a materially different candidate is available.  imp 0.85 → +Choose a model formulation  [first in 139/148 visits that checked it]
then:        E70 Learning curves show that current fitting settings are inadequate.  imp 0.75 → +Adjust training dynamics  [first in 98/119 visits that checked it]
then:        E69 The current training signal differs from what evaluation rewards.  imp 0.80 → +Choose the fitting objective  [first in 30/50 visits that checked it]
more:         4 further checks (E142, E144, E143, E141), load on request
enough when:  top option >= 66% (lower quartile over 297 visits) or >= 46 points ahead; median 2 checks
come back:    after 'other' (6/18); after 'after a new best' (4/18); after '2 scored steps without a new best' (3/18)  [18 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 92% of visits
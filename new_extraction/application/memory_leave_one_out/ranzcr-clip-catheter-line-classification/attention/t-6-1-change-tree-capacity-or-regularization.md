# [Change tree capacity or regularization › Which tree-training control should be adjusted?]   92 visits, 15 experts

options: Tune depth and leaf capacity (19) | Tune tree regularization (8) | Subsample rows or columns (1) | Tune boosting rate and rounds (6)

check first: E102 Training fit is strong but validation worsens as complexity grows.  imp 0.75 → +Tune tree regularization  [first in 43/48 visits that checked it]
then:        E101 Training error remains high with shallow or small trees.  imp 0.85 → +Tune depth and leaf capacity  [first in 17/21 visits that checked it]
then:        E104 A reduced learning rate exhausts the iteration budget before convergence.  imp 0.80 → +Tune boosting rate and rounds  [first in 16/19 visits that checked it]
more:         1 further checks (E103), load on request
enough when:  top option >= 47% (lower quartile over 78 visits) or >= 15 points ahead; median 1 checks
come back:    after 'other' (3/8); after 'after a new best' (2/8); after '4+ scored steps without a new best' (2/8)  [8 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 67% of visits
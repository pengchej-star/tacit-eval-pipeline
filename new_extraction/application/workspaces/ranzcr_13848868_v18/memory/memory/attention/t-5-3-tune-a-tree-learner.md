# [Tune a tree learner › Which tree-fitting constraint should I adjust?]   115 visits, 15 experts

options: Tune tree depth and leaves (14) | Tune penalties and subsampling (9) | Coordinate boosting rate and rounds (10) | Change stopping patience or criterion (5) | Reset uncertain tree parameters (2)

check first: E103 Learning rate changed without a corresponding convergence budget.  imp 0.78 → +Coordinate boosting rate and rounds  [first in 31/58 visits that checked it]
then:        E101 Trees appear capacity-limited or increased capacity has begun to overfit.  imp 0.72 → +Tune tree depth and leaves  [first in 27/32 visits that checked it]
then:        E102 Training error improves while validation worsens with the current feature set.  imp 0.65 → +Tune penalties and subsampling  [first in 14/25 visits that checked it]
more:         13 further checks (E286, E105, E104, E285, E283, E284, E288, E287, E290, E292, E291, E293, E289), load on request
enough when:  top option >= 37% (lower quartile over 115 visits) or >= 7 points ahead; median 6 checks
come back:    after 'other' (4/9); after 'after a new best' (2/9); after '4+ scored steps without a new best' (2/9)  [9 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 51% of visits
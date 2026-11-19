# [Average repeated training variants › Which repeated-training dimension should be averaged?]   97 visits, 23 experts

options: Average fold checkpoints (40) | Average independently trained seeds (13)

check first: E150 All required fold checkpoints are compatible and currently only some are used.  imp 0.82 → +Average fold checkpoints  [first in 60/70 visits that checked it]
then:        E151 Independent training seeds produce materially different held-out predictions.  imp 0.78 → +Average independently trained seeds  [first in 15/15 visits that checked it]
then:        E365 The current edit removes multi-seed or multi-fold averaging to establish a single-checkpoint baseline before re-adding ensemble members.  imp 0.35 → +Average fold checkpoints  [first in 13/97 visits that checked it]
more:         21 further checks (E366, E152, E153, E369, E373, E378, E376, E371, E368, E381, E372, E382, E383, E374, E377, E384, E367, E370, E379, E375, E380), load on request
enough when:  top option >= 69% (lower quartile over 97 visits) or >= 37 points ahead; median 7 checks
come back:    after 'after a new best' (2/3); after 'other' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 76% of visits
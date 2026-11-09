# [Choose a combination rule › Which rule should I compare against the current aggregation?]   129 visits, 17 experts

options: Compare rank and raw-score averaging (22) | Compare probability and logit aggregation (3) | Group before averaging (5) | Fit a regularized prediction stacker (15) | Change the meta-learner (12) | Try a nonlinear probability blend (3)

check first: E135 The metric rewards ordering and members have different score scales.  imp 0.65 → +Compare rank and raw-score averaging  [first in 77/86 visits that checked it]
then:        E138 Aligned leakage-free out-of-fold predictions exist for a simple learned blender.  imp 0.75 → +Fit a regularized prediction stacker  [first in 18/50 visits that checked it]
then:        E137 Model families contribute unequal numbers of fold or seed predictions.  imp 0.55 → +Group before averaging  [first in 14/49 visits that checked it]
more:         4 further checks (E139, E136, E141, E140), load on request
enough when:  top option >= 36% (lower quartile over 127 visits) or >= 11 points ahead; median 2 checks
come back:    after 'after a new best' (2/4); after 'regression after a single change' (1/4); after '4+ scored steps without a new best' (1/4)  [4 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 61% of visits
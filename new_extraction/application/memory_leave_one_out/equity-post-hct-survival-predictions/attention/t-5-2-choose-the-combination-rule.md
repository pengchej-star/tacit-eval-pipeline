# [Choose the combination rule › What combination rule fits the available prediction evidence?]   314 visits, 38 experts

options: Average predictions uniformly (7) | Tune constrained blend weights (87) | Rank-normalize before blending (15) | Choose probability-space or logit-space averaging (7) | Fit a cross-validated meta-learner (22)

check first: E72 Members have unequal quality and aligned validation predictions are available.  imp 0.60 → -Average predictions uniformly  [first in 153/244 visits that checked it]
then:        E71 Weight estimates are unstable or no independent out-of-fold predictions support fitting them.  imp 0.55 → -Fit a cross-validated meta-learner  [first in 105/184 visits that checked it]
then:        E73 The metric uses ordering and members have incompatible score scales or outliers.  imp 0.75 → +Rank-normalize before blending  [first in 44/147 visits that checked it]
more:         2 further checks (E74, E75), load on request
enough when:  top option >= 42% (lower quartile over 314 visits) or >= 8 points ahead; median 3 checks
come back:    after 'after a new best' (2/9); after 'other' (2/9); after '4+ scored steps without a new best' (2/9)  [9 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 54% of visits
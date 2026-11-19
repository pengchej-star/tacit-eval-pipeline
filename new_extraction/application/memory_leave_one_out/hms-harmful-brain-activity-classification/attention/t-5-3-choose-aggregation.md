# [Choose aggregation › How should aligned member predictions be combined?]   305 visits, 38 experts

options: Use a uniform arithmetic average (9) | Tune fixed blend weights (69) | Test signed blend weights (2) | Compare raw and rank-normalized averaging (21) | Normalize member scales before blending (3) | Average within families before blending (4) | Fit a regularized stacker on out-of-fold predictions (23)

check first: E84 Members differ in useful contribution and held-out predictions support weight comparisons.  imp 0.82 → +Tune fixed blend weights  [first in 165/194 visits that checked it]
then:        E86 Member scales differ or raw versus rank aggregation has changed preference across configurations.  imp 0.70 → +Compare raw and rank-normalized averaging  [first in 53/65 visits that checked it]
then:        E89 Enough OOF examples exist to learn stable complementary relationships among base outputs.  imp 0.88 → +Fit a regularized stacker on out-of-fold predictions  [first in 35/81 visits that checked it]
more:         5 further checks (E83, E88, E87, E85, E90), load on request
enough when:  top option >= 34% (lower quartile over 302 visits) or >= 16 points ahead; median 1 checks
come back:    after '4+ scored steps without a new best' (3/11); after 'regression after a bundled change' (2/11); after 'after a new best' (2/11)  [11 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 81% of visits
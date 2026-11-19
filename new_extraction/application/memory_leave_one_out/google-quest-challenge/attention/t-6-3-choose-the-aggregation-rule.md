# [Choose the aggregation rule › How should aligned predictions be combined?]   409 visits, 40 experts

options: Use uniform averaging (11) | Tune fixed blend weights (98) | Probe signed weights (2) | Compare rank and raw aggregation (21) | Compare logit and probability pooling (3) | Test nonlinear pooling (3) | Fit a regularized meta-learner (33)

check first: E99 Members differ in quality or residual patterns and the current blend has not been retuned after a component change.  imp 0.78 → +Tune fixed blend weights  [first in 238/348 visits that checked it]
then:        E98 Member quality is similar or previous nonuniform weights fail to beat equal weighting.  imp 0.72 → +Use uniform averaging  [first in 85/119 visits that checked it]
then:        E101 The metric is ranking-based and member prediction scales or calibrations differ.  imp 0.65 → +Compare rank and raw aggregation  [first in 63/337 visits that checked it]
more:         6 further checks (E105, E102, E104, E106, E103, E100), load on request
enough when:  top option >= 26% (lower quartile over 409 visits) or >= 6 points ahead; median 4 checks
come back:    after 'other' (6/14); after '4+ scored steps without a new best' (4/14); after 'after a new best' (2/14)  [14 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 58% of visits
# [Change the combination domain › On what scale should member predictions be combined?]   62 visits, 11 experts

options: Preserve raw member magnitudes (2) | Trial per-target rank averaging (18) | Normalize prediction columns (2) | Trial a concave probability transform (3) | Average logits before softmax (1) | Normalize each member before averaging (1)

check first: E168 The metric is rank-based and member score distributions differ in calibration or scale.  imp 0.85 → +Trial per-target rank averaging  [first in 48/61 visits that checked it]
then:        E316 Rank conversion was already tried in a prior version and its effect size is known.  imp 0.50 → +Trial per-target rank averaging  [first in 8/49 visits that checked it]
then:        E171 Compatible pre-softmax logits are available and the task scores categorical probability distributions.  imp 0.75 → +Average logits before softmax  [first in 3/6 visits that checked it]
more:         13 further checks (E324, E167, E170, E323, E317, E320, E318, E321, E319, E322, E325, E169, E172), load on request
enough when:  top option >= 50% (lower quartile over 62 visits) or >= 32 points ahead; median 6 checks
come back:    after 'regression after a single change' (1/2); after 'other' (1/2)  [2 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 69% of visits
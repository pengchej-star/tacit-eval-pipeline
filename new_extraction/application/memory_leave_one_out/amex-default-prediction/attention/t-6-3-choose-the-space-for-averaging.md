# [Choose the space for averaging › Which transformation should be tested before combining model scores?]   74 visits, 14 experts

options: Compare rank and raw averaging (24) | Standardize prediction scales (3) | Reshape scores before averaging (3) | Choose logits or probabilities (2)

check first: E163 The metric depends on ordering and member score scales or calibration differ.  imp 0.75 → +Compare rank and raw averaging  [first in 66/66 visits that checked it]
then:        E166 Models expose both logits and probabilities and the metric evaluates distributions.  imp 0.70 → +Choose logits or probabilities  [first in 5/7 visits that checked it]
then:        E167 Absolute magnitudes are required by a downstream additive correction.  imp 0.75 → +Standardize prediction scales  [first in 3/30 visits that checked it]
more:         2 further checks (E164, E165), load on request
enough when:  top option >= 40% (lower quartile over 74 visits) or >= 18 points ahead; median 1 checks
come back:    after 'regression after a single change' (1/1)  [1 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 82% of visits
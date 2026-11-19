# [Change training duration or checkpoint use › What limits the quality of the currently selected trained state?]   115 visits, 25 experts

options: Sweep training duration (4) | Retune early-stopping patience (2) | Compare existing trained checkpoints (34) | Average compatible model weights (1) | Repair and retune a weak member’s training (6)

check first: E142 Several compatible trained states already exist with different validation results.  imp 0.75 → +Compare existing trained checkpoints  [first in 93/96 visits that checked it]
then:        E140 The metric is still improving at the training cap or extra epochs have started to overfit.  imp 0.85 → +Sweep training duration  [first in 10/10 visits that checked it]
then:        E144 A weak ensemble component lacks the fold discipline or tuning used by the stronger components.  imp 0.70 → +Repair and retune a weak member’s training  [first in 6/7 visits that checked it]
more:         2 further checks (E141, E143), load on request
enough when:  top option >= 44% (lower quartile over 113 visits) or >= 25 points ahead; median 1 checks
come back:    after 'after a new best' (3/3)  [3 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 89% of visits
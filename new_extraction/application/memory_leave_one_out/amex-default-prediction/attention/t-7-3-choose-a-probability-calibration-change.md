# [Choose a probability calibration change › Which probability adjustment is justified by the observed miscalibration?]   12 visits, 6 experts

options: Rescale logits (2) | Reweight class probabilities (3) | Enforce required output ranges (3)

check first: E185 Predictions violate the required range or do not sum to one for a distributional task.  imp 0.88 → +Enforce required output ranges  [first in 4/9 visits that checked it]
then:        E186 The metric only uses within-column rank and no later blend or rounding depends on magnitude.  imp 0.65 → -Rescale logits  [first in 3/12 visits that checked it]
then:        E423 The per-class multipliers were tuned on a different checkpoint version than the one currently in use.  imp 0.55 → -Reweight class probabilities  [first in 3/6 visits that checked it]
more:         4 further checks (E184, E183, E425, E424), load on request
enough when:  top option >= 70% (lower quartile over 12 visits) or >= 45 points ahead; median 4 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 42% of visits
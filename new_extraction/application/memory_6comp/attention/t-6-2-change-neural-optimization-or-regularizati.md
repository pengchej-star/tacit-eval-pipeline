# [Change neural optimization or regularization › Which neural training control should be tested next?]   27 visits, 10 experts

options: Tune learning rate or schedule (7) | Change the optimizer (2) | Tune neural regularization (2) | Change training augmentation (5)

check first: E108 A transformation can vary inputs while preserving or consistently mixing target meaning.  imp 0.70 → +Change training augmentation  [first in 10/12 visits that checked it]
then:        E105 Training loss diverges, oscillates, or converges too slowly under the current schedule.  imp 0.85 → +Tune learning rate or schedule  [first in 7/7 visits that checked it]
then:        E106 Stable learning-rate trials have plateaued with the same optimizer.  imp 0.75 → +Change the optimizer  [first in 4/9 visits that checked it]
more:         5 further checks (E107, E271, E270, E272, E273), load on request
enough when:  top option >= 51% (lower quartile over 27 visits) or >= 27 points ahead; median 3 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 96% of visits
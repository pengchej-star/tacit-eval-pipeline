# [Change the optimization trajectory › Which optimization setting is the next justified change?]   21 visits, 10 experts

options: Tune the learning rate (7) | Change the learning-rate schedule (1) | Change the optimizer (1) | Tune training duration (3) | Monitor the intended validation metric (3)

check first: E123 The stopping callback monitors training data, the wrong metric direction, or the wrong validation set.  imp 0.80 → +Monitor the intended validation metric  [first in 4/4 visits that checked it]
then:        E352 The current learning rate falls outside the commonly recommended range for the model architecture being fine-tuned.  imp 0.85 → +Tune the learning rate  [first in 3/9 visits that checked it]
then:        E122 Validation is still improving at the final epoch or worsens well before it.  imp 0.75 → +Tune training duration  [first in 3/5 visits that checked it]
more:         9 further checks (E351, E119, E121, E354, E357, E120, E353, E355, E356), load on request
enough when:  top option >= 45% (lower quartile over 21 visits) or >= 29 points ahead; median 3 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 100% of visits
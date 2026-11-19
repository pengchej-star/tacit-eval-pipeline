# [Change neural optimization › Which optimization control should be changed first?]   22 visits, 10 experts

options: Bracket the fine-tuning learning rate (5) | Compare learning-rate schedules (1) | Compare optimizers (1) | Tune head dropout (4) | Align the loss and output parameterization (5)

check first: E139 The output activation or training loss imposes assumptions inconsistent with the labels or task metric.  imp 0.82 → +Align the loss and output parameterization  [first in 6/14 visits that checked it]
then:        E135 Training is unstable or converges too slowly under the current fine-tuning rate.  imp 0.88 → +Bracket the fine-tuning learning rate  [first in 6/7 visits that checked it]
then:        E138 The pretrained backbone fits training data well but the added head overfits.  imp 0.87 → +Tune head dropout  [first in 4/5 visits that checked it]
more:         4 further checks (E300, E137, E301, E136), load on request
enough when:  top option >= 53% (lower quartile over 22 visits) or >= 34 points ahead; median 3 checks
come back:    after 'other' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 86% of visits
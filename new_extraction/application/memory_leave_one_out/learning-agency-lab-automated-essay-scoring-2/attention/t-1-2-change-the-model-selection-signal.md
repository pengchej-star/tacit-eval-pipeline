# [Change the model-selection signal › What should change in the metric used to select training iterations?]   24 visits, 6 experts

options: Use the task metric for stopping (5) | Use a smoother stopping proxy (2) | Repair the metric callback (4) | Accelerate repeated metric calculation (1)

check first: E19 Callback values or shapes disagree with an independent calculation.  imp 0.80 → +Repair the metric callback  [first in 11/15 visits that checked it]
then:        E17 The current stopping metric differs from the scored objective and selects worse checkpoints in prior comparisons.  imp 0.85 → +Use the task metric for stopping  [first in 9/10 visits that checked it]
then:        E18 The task metric fluctuates sharply between nearby iterations while a smooth proxy tracks generalization better.  imp 0.75 → +Use a smoother stopping proxy  [first in 2/4 visits that checked it]
more:         2 further checks (E205, E20), load on request
enough when:  top option >= 56% (lower quartile over 24 visits) or >= 31 points ahead; median 1 checks
come back:    after 'other' (2/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 92% of visits
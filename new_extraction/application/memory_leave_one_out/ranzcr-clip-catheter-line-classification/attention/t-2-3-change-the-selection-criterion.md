# [Change the selection criterion › Which metric should control model selection and stopping?]   22 visits, 7 experts

options: Use the task metric (12) | Use a stable proxy for stopping (1)

check first: E34 The current callback differs from the official scoring function or uses the wrong direction.  imp 0.85 → +Use the task metric  [first in 19/19 visits that checked it]
then:        E188 The eval_metric was already set to a reasonable proxy (e.g., AUC) in a prior iteration, so the callback may not need changing.  imp 0.50 → -Use the task metric  [first in 2/14 visits that checked it]
then:        E35 The task metric fluctuates sharply between adjacent iterations while a smooth proxy is stable.  imp 0.65 → +Use a stable proxy for stopping  [first in 1/2 visits that checked it]
enough when:  top option >= 85% (lower quartile over 22 visits) or >= 70 points ahead; median 2 checks
come back:    after 'other' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 95% of visits
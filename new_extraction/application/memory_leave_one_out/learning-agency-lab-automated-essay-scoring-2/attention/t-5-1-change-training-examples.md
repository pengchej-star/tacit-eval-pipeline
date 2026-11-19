# [Change training examples › How should the training population change?]   74 visits, 9 experts

options: Refit on more labeled rows (4) | Trial additional labeled data (4) | Train with validated pseudo-labels (2) | Filter noisy or redundant examples (8) | Tune class or sample weights (4)

check first: E108 Class imbalance or subgroup error patterns suggest the current sample weighting is unsuitable.  imp 0.72 → +Tune class or sample weights  [first in 22/31 visits that checked it]
then:        E107 Training examples contain duplicated windows, flagged outliers, or measurable label-quality variation.  imp 0.82 → +Filter noisy or redundant examples  [first in 21/28 visits that checked it]
then:        E105 Additional labeled examples exist with compatible targets and adaptable input shapes.  imp 0.75 → +Trial additional labeled data  [first in 16/17 visits that checked it]
more:         4 further checks (E104, E106, E284, E283), load on request
enough when:  top option >= 38% (lower quartile over 74 visits) or >= 4 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 57% of visits
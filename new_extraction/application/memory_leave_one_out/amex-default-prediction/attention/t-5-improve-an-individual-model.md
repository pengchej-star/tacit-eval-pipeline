# [Improve an individual model › Which modification to one learner should be tested next?]   434 visits, 48 experts

options: Reuse trained weights differently (61) | Choose a different predictor (38) | Change how representations become predictions (30) | Improve how one model is fitted (57)

check first: E95 Compatible saved variants exist and current inference can compare them without retraining.  imp 0.72 → +Reuse trained weights differently  [first in 230/234 visits that checked it]
then:        E98 Training logs expose optimization, loss, regularization, or implementation shortcomings.  imp 0.68 → +Improve how one model is fitted  [first in 95/117 visits that checked it]
then:        E97 The backbone is useful but pooling, head structure, or modality fusion is restrictive.  imp 0.70 → +Change how representations become predictions  [first in 49/85 visits that checked it]
more:         8 further checks (E96, E312, E310, E313, E314, E311, E315, E316), load on request
enough when:  top option >= 49% (lower quartile over 419 visits) or >= 24 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (6/23); after '2 scored steps without a new best' (6/23); after 'regression after a single change' (4/23)  [23 returns, 6 improved the score]

scores: LLM-guessed; top option matches the option taken in 81% of visits
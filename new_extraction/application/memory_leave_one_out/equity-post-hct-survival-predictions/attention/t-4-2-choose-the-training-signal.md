# [Choose the training signal › How should the objective or target encoding change?]   24 visits, 6 experts

options: Align the loss or prediction formulation (11) | Center or rescale regression targets (1)

check first: E56 The current loss ignores ordinal, pairwise, distributional, or multi-output evaluation structure.  imp 0.95 → +Align the loss or prediction formulation  [first in 19/20 visits that checked it]
then:        E57 Regression target location or scale varies across folds or poorly matches the model output range.  imp 0.85 → +Center or rescale regression targets  [first in 4/6 visits that checked it]
then:        E170 A constant-hessian (ones) baseline for the custom objective is known to be stable and competitive.  imp 0.55 → +Align the loss or prediction formulation  [first in 1/6 visits that checked it]
enough when:  top option >= 90% (lower quartile over 24 visits) or >= 79 points ahead; median 1 checks
come back:    after '4+ scored steps without a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 92% of visits
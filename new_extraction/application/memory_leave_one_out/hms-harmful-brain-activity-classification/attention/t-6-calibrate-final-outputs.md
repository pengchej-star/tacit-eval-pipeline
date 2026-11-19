# [Calibrate final outputs › Which output transformation matches the observed prediction defect?]   127 visits, 23 experts

options: Map outputs to labels (41) | Correct a validated prediction offset or orientation (5) | Calibrate output range before discretization (2) | Reshape component probabilities before combination (5) | Apply a validated auxiliary or metadata correction (11) | Ablate and revalidate the current post-processing (3)

check first: E100 The target has a restricted range or a small ordered set of values.  imp 0.72 → +Map outputs to labels  [first in 98/103 visits that checked it]
then:        E104 An auxiliary classifier or observable rule predicts a specific systematic residual.  imp 0.60 → +Apply a validated auxiliary or metadata correction  [first in 8/28 visits that checked it]
then:        E101 Predictions have an inverted convention or a reproducible additive bias.  imp 0.85 → +Correct a validated prediction offset or orientation  [first in 8/19 visits that checked it]
more:         6 further checks (E103, E167, E105, E169, E168, E102), load on request
enough when:  top option >= 39% (lower quartile over 127 visits) or >= 11 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (3/5); after 'after a new best' (2/5)  [5 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 83% of visits
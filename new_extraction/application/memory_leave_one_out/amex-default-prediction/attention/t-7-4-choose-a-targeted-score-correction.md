# [Choose a targeted score correction › What independent evidence justifies correcting individual predictions?]   36 visits, 10 experts

options: Correct a systematic output offset (5) | Apply an auxiliary-signal correction (9) | Apply a precise metadata rule (4)

check first: E188 A validated auxiliary classifier identifies cases where the base continuous model is biased.  imp 0.88 → +Apply an auxiliary-signal correction  [first in 11/13 visits that checked it]
then:        E187 Residuals show a stable additive offset or target scaling was not inverted.  imp 0.92 → +Correct a systematic output offset  [first in 9/9 visits that checked it]
then:        E189 A metadata rule predicts an affected target with high precision on held-out examples.  imp 0.90 → +Apply a precise metadata rule  [first in 7/8 visits that checked it]
more:         8 further checks (E427, E190, E428, E431, E430, E432, E429, E426), load on request
enough when:  top option >= 53% (lower quartile over 36 visits) or >= 9 points ahead; median 5 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 81% of visits
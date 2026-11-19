# [Correct continuous outputs › Which observed calibration discrepancy should be adjusted?]   37 visits, 8 experts

options: Correct location or scale bias (9) | Calibrate class probabilities (3) | Apply a gated auxiliary correction (5)

check first: E89 An auxiliary classifier or metadata rule identifies a subset with reproducible directional residuals.  imp 0.75 → +Apply a gated auxiliary correction  [first in 11/11 visits that checked it]
then:        E87 Validation residuals show a systematic location or scale error.  imp 0.92 → +Correct location or scale bias  [first in 9/11 visits that checked it]
then:        E193 Raw model outputs may exceed the valid target range or hit exact boundaries.  imp 0.55 → +Correct location or scale bias  [first in 7/14 visits that checked it]
more:         3 further checks (E88, E191, E192), load on request
enough when:  top option >= 68% (lower quartile over 36 visits) or >= 51 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (1/1)  [1 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 97% of visits
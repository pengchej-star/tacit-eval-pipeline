# [Change the final prediction mapping › Which output mismatch calls for a calibration change?]   146 visits, 25 experts

options: Calibrate prediction scale or direction (18) | Choose ordinal output conversion (50) | Apply a validated subgroup correction (11)

check first: E118 The required labels are discrete or the rank metric is affected by the target tie structure.  imp 0.80 → +Choose ordinal output conversion  [first in 85/98 visits that checked it]
then:        E117 Outputs have the wrong direction, link function, range or calibration for the required predictions.  imp 0.85 → +Calibrate prediction scale or direction  [first in 22/23 visits that checked it]
then:        E119 A known subgroup or metadata rule explains systematic residuals beyond the current model.  imp 0.85 → +Apply a validated subgroup correction  [first in 15/26 visits that checked it]
more:         18 further checks (E121, E245, E248, E246, E251, E256, E259, E258, E255, E253, E120, E254, E250, E249, E260, E247, E252, E257), load on request
enough when:  top option >= 63% (lower quartile over 146 visits) or >= 40 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (1/1)  [1 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 81% of visits
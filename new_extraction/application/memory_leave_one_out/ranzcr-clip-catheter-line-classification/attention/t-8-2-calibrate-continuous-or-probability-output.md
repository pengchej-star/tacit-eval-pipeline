# [Calibrate continuous or probability outputs › Which systematic prediction defect should be corrected?]   56 visits, 14 experts

options: Correct prediction bias or scale (10) | Calibrate class distributions (3) | Apply an auxiliary residual correction (6) | Apply a validated conditional rule (7) | Keep unmodified continuous scores (1)

check first: E146 A metadata-defined subset has a reproducible error pattern and its defining fields exist at test time.  imp 0.85 → +Apply a validated conditional rule  [first in 15/16 visits that checked it]
then:        E143 Held-out residuals have a systematic offset or scale error relevant to the metric.  imp 0.95 → +Correct prediction bias or scale  [first in 12/14 visits that checked it]
then:        E147 The metric is invariant to the proposed rescaling and no calibration defect has been demonstrated.  imp 0.80 → +Keep unmodified continuous scores  [first in 9/46 visits that checked it]
more:         10 further checks (E145, E144, E309, E311, E312, E307, E310, E306, E305, E308), load on request
enough when:  top option >= 53% (lower quartile over 56 visits) or >= 33 points ahead; median 5 checks
come back:    after '4+ scored steps without a new best' (3/4); after 'after a new best' (1/4)  [4 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 82% of visits
# [Change the output mapping › Which output mapping fits the target and metric?]   79 visits, 18 experts

options: Tune ordinal cutpoints (18) | Match discrete target support (1) | Calibrate prediction scale (10) | Apply a supported conditional correction (11) | Remove ineffective postprocessing (2)

check first: E107 The target is ordinal and the metric depends on discrete label agreement.  imp 0.90 → +Tune ordinal cutpoints  [first in 72/76 visits that checked it]
then:        E109 Predictions have systematic bias or scale mismatch relevant to the metric or downstream rounding.  imp 0.75 → +Calibrate prediction scale  [first in 3/20 visits that checked it]
then:        E111 Previous postprocessing gains vanished after a model change or the transform preserves a metric-invariant ordering.  imp 0.75 → +Remove ineffective postprocessing  [first in 1/35 visits that checked it]
more:         21 further checks (E110, E200, E193, E210, E108, E198, E202, E196, E209, E201, E206, E197, E195, E194, E199, E207, E208, E203, E204, E112, E205), load on request
enough when:  top option >= 59% (lower quartile over 79 visits) or >= 35 points ahead; median 8 checks
come back:    after '4+ scored steps without a new best' (2/3); after 'regression after a single change' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 63% of visits
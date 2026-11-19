# [Make the pipeline practical to run › Which execution change removes the measured iteration bottleneck?]   284 visits, 37 experts

options: Stream data and release model memory (35) | Cache reusable features and predictions (19) | Use a reduced development run (23) | Refactor with prediction parity checks (47)

check first: E09 Manual toggles, duplicated code or obsolete dependencies have caused integration errors.  imp 0.60 → +Refactor with prediction parity checks  [first in 123/181 visits that checked it]
then:        E06 Peak memory is reached while several models or intermediate matrices coexist.  imp 0.72 → +Stream data and release model memory  [first in 53/68 visits that checked it]
then:        E08 The current trial needs pipeline feedback before a full fold and estimator budget is justified.  imp 0.65 → +Use a reduced development run  [first in 52/85 visits that checked it]
more:         2 further checks (E07, E10), load on request
enough when:  top option >= 45% (lower quartile over 282 visits) or >= 17 points ahead; median 1 checks
come back:    after 'other' (8/26); after '4+ scored steps without a new best' (6/26); after 'after a new best' (5/26)  [26 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 76% of visits
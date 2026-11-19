# [Make the next experiment feasible › Which execution change removes the measured resource bottleneck?]   160 visits, 32 experts

options: Use a controlled reduced-cost development mode (19) | Process complete entities in chunks (5) | Release intermediates between model stages (16) | Reduce or bucket inference batches (4) | Compare reduced-precision inference (2) | Cache reusable features, predictions and search results (14) | Separate and verify model-specific inference paths (20) | Train remaining folds across sessions (2) | Accelerate evaluation with numerical parity checks (1)

check first: E106 Full runs are too expensive to locate errors or screen candidate settings.  imp 0.85 → +Use a controlled reduced-cost development mode  [first in 55/56 visits that checked it]
then:        E112 Multiple variants share fragile duplicated code or overwrite each other’s artifacts.  imp 0.75 → +Separate and verify model-specific inference paths  [first in 31/43 visits that checked it]
then:        E108 Peak memory rises across successive model or feature stages.  imp 0.80 → +Release intermediates between model stages  [first in 25/42 visits that checked it]
more:         6 further checks (E111, E107, E113, E109, E110, E114), load on request
enough when:  top option >= 27% (lower quartile over 160 visits) or >= 11 points ahead; median 1 checks
come back:    after 'other' (7/21); after 'after a new best' (6/21); after '4+ scored steps without a new best' (4/21)  [21 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 89% of visits
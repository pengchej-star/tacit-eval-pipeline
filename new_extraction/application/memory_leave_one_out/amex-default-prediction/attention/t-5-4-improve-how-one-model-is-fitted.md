# [Improve how one model is fitted › Which training intervention should be tested next?]   116 visits, 26 experts

options: Change the optimization trajectory (15) | Change the prediction objective (15) | Choose a regularization intervention (7) | Tune tree complexity and regularization (14) | Repair training discipline (6)

check first: E117 A tree learner’s depth, leaf count, or penalties constrain the observed fit.  imp 0.92 → +Tune tree complexity and regularization  [first in 33/67 visits that checked it]
then:        E343 A recent code or config change has not yet been scored, so a rerun is needed before drawing conclusions.  imp 0.50 → +Repair training discipline  [first in 26/99 visits that checked it]
then:        E115 The current loss or output semantics do not match the target or evaluation metric.  imp 0.78 → +Change the prediction objective  [first in 18/24 visits that checked it]
more:         11 further checks (E116, E118, E342, E346, E114, E348, E344, E347, E350, E345, E349), load on request
enough when:  top option >= 36% (lower quartile over 114 visits) or >= 8 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (2/6); after 'after a new best' (2/6); after 'other' (1/6)  [6 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 68% of visits
# [Repair prediction computation › Which computation defect explains the implausible output?]   64 visits, 20 experts

options: Repair blending arithmetic (18) | Repair output or objective mathematics (3) | Restore all intended predictions (9) | Trace constant predictions (5) | Align prediction direction (3)

check first: E17 A hand-calculated blend disagrees with the implemented blend.  imp 0.85 → +Repair blending arithmetic  [first in 16/16 visits that checked it]
then:        E19 The number of accumulated predictions is smaller than the enabled member count.  imp 0.80 → +Restore all intended predictions  [first in 13/25 visits that checked it]
then:        E20 Predictions are constant or unchanged after changes that should affect them.  imp 0.85 → +Trace constant predictions  [first in 11/13 visits that checked it]
more:         13 further checks (E219, E18, E216, E218, E217, E21, E220, E225, E224, E223, E221, E226, E222), load on request
enough when:  top option >= 50% (lower quartile over 64 visits) or >= 26 points ahead; median 2 checks
come back:    after 'regression after a single change' (2/4); after '4+ scored steps without a new best' (1/4); after 'after a new best' (1/4)  [4 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 69% of visits
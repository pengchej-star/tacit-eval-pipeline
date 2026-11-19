# [Choose the next experiment › What experiment will resolve the current uncertainty most directly?]   901 visits, 55 experts

options: Run a controlled ablation (134) | Measure repeated-run variability (58) | Restore the last verified configuration (53) | Bracket and refine a parameter search (21) | Stop a saturated local search (56)

check first: E13 The last scored version changed several plausible causes of the score movement.  imp 0.72 → +Run a controlled ablation  [first in 540/830 visits that checked it]
then:        E14 The observed improvement is comparable to variation among unchanged reruns.  imp 0.78 → +Measure repeated-run variability  [first in 147/388 visits that checked it]
then:        E18 A stable working configuration is unavailable for controlled comparisons.  imp 0.60 → -Restore the last verified configuration  [first in 73/838 visits that checked it]
more:         3 further checks (E17, E16, E15), load on request
enough when:  top option >= 30% (lower quartile over 899 visits) or >= 9 points ahead; median 3 checks
come back:    after 'regression after a single change' (12/45); after 'after a new best' (11/45); after '4+ scored steps without a new best' (9/45)  [45 returns, 11 improved the score]

scores: LLM-guessed; top option matches the option taken in 63% of visits
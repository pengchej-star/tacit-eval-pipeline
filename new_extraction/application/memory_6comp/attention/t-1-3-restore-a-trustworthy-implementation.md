# [Restore a trustworthy implementation › How should an unreliable implementation be stabilized?]   293 visits, 43 experts

options: Add a small end-to-end smoke run (52) | Restore the last verified configuration (19) | Refactor with prediction parity (34) | Rebuild a minimal working baseline (4)

check first: E12 A newly integrated path has never completed on representative data.  imp 0.85 → +Add a small end-to-end smoke run  [first in 154/236 visits that checked it]
then:        E14 Repeated branches and implicit configuration make model dispatch or data flow inconsistent.  imp 0.65 → +Refactor with prediction parity  [first in 73/247 visits that checked it]
then:        E13 A previously verified configuration exists and recent bundled edits caused a large regression.  imp 0.75 → +Restore the last verified configuration  [first in 59/241 visits that checked it]
more:         1 further checks (E15), load on request
enough when:  top option >= 48% (lower quartile over 293 visits) or >= 15 points ahead; median 3 checks
come back:    after 'other' (7/23); after 'regression after a single change' (5/23); after '4+ scored steps without a new best' (4/23)  [23 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 54% of visits
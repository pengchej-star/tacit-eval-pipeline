# [Repair execution and output assembly › Which execution defect prevents a valid final prediction?]   211 visits, 42 experts

options: Fix API and runtime errors (21) | Repair artifact and dependency loading (11) | Repair ensemble arithmetic (50) | Repair submission generation (5) | Correct output semantics (7) | Repair device configuration (6) | Recover missing member predictions (2)

check first: E07 The blended output disagrees with a direct recomputation from saved member arrays.  imp 0.95 → +Repair ensemble arithmetic  [first in 92/107 visits that checked it]
then:        E05 A small-batch run raises an API, shape, or variable-reference exception.  imp 0.90 → +Fix API and runtime errors  [first in 60/126 visits that checked it]
then:        E06 Required files or packages are absent or incompatible in the submission environment.  imp 0.85 → +Repair artifact and dependency loading  [first in 25/77 visits that checked it]
more:         4 further checks (E08, E09, E10, E11), load on request
enough when:  top option >= 43% (lower quartile over 208 visits) or >= 30 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (5/22); after '3 scored steps without a new best' (4/22); after 'other' (4/22)  [22 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 87% of visits
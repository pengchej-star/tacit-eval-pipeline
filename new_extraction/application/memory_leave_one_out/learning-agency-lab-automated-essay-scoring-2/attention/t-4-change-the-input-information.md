# [Change the input information › What limitation in the current input representation should the next experiment address?]   315 visits, 31 experts

options: Change tabular summaries (20) | Reduce feature noise (25) | Change numerical preprocessing (7) | Change text information (8) | Change image or signal encoding (44) | Change modality use (21)

check first: E69 Spatial or spectral preprocessing removes relevant structure or mismatches trained inputs.  imp 0.80 → +Change image or signal encoding  [first in 93/137 visits that checked it]
then:        E66 Many engineered inputs are redundant, sparse, or implicated in prior regressions.  imp 0.50 → +Reduce feature noise  [first in 66/94 visits that checked it]
then:        E70 Several aligned modalities or channels exist and their use or fusion remains unresolved.  imp 0.80 → +Change modality use  [first in 56/88 visits that checked it]
more:         6 further checks (E65, E68, E242, E240, E241, E67), load on request
enough when:  top option >= 31% (lower quartile over 311 visits) or >= 10 points ahead; median 2 checks
come back:    after 'after a new best' (4/9); after '4+ scored steps without a new best' (2/9); after 'regression after a single change' (2/9)  [9 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 79% of visits
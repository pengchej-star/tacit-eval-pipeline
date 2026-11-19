# [Change signal or image representation › Which aspect of the signal-to-model input should change?]   130 visits, 7 experts

options: Change time-frequency resolution (8) | Change the input window (6) | Change signal filtering (4) | Change input scaling and rendering (6) | Change channel layout (4) | Add or ablate an input modality (18)

check first: E76 An available raw or transformed modality contains information absent from the active branch.  imp 0.82 → +Add or ablate an input modality  [first in 58/66 visits that checked it]
then:        E71 Current time-frequency bins merge potentially informative frequencies or time events.  imp 0.72 → +Change time-frequency resolution  [first in 23/27 visits that checked it]
then:        E72 The current crop omits relevant context or includes long irrelevant regions.  imp 0.65 → +Change the input window  [first in 17/24 visits that checked it]
more:         3 further checks (E75, E74, E73), load on request
enough when:  top option >= 37% (lower quartile over 130 visits) or >= 19 points ahead; median 1 checks
come back:    after 'regression after a single change' (4/11); after 'after a new best' (4/11); after 'other' (2/11)  [11 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 94% of visits
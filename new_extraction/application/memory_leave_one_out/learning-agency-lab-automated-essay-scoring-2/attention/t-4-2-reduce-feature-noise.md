# [Reduce feature noise › What evidence should guide the next feature reduction?]   70 visits, 11 experts

options: Select a stable importance-ranked subset (11) | Ablate a suspected feature group (12) | Test dropping extremely sparse columns (1) | Limit the pooled feature dimension (1)

check first: E79 A particular added feature family coincided with a regression or is error-prone.  imp 0.82 → +Ablate a suspected feature group  [first in 28/30 visits that checked it]
then:        E78 A wide feature table has stable cross-fold importance estimates.  imp 0.75 → +Select a stable importance-ranked subset  [first in 27/30 visits that checked it]
then:        E261 No leaderboard scores have been submitted for recent versions, so the expert lacks external validation to confirm the current feature-selection ratio is optimal.  imp 0.40 → -Select a stable importance-ranked subset  [first in 5/67 visits that checked it]
more:         11 further checks (E259, E258, E81, E264, E80, E267, E260, E262, E265, E263, E266), load on request
enough when:  top option >= 55% (lower quartile over 70 visits) or >= 35 points ahead; median 7 checks
come back:    after 'other' (2/3); after 'after a new best' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 86% of visits
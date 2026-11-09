# [Change the prediction pool › How should I change which trained predictors contribute?]   789 visits, 54 experts

options: Choose the source of ensemble diversity (143) | Choose ensemble membership (174) | Select a trained artifact (43)

check first: E111 Existing members mostly share the same architecture, features, targets, or training randomness.  imp 0.75 → +Choose the source of ensemble diversity  [first in 385/460 visits that checked it]
then:        E112 There are untested, weak, or recently changed members in the current pool.  imp 0.60 → +Choose ensemble membership  [first in 347/686 visits that checked it]
then:        E113 Several compatible saved runs or training-stage artifacts are available.  imp 0.50 → +Select a trained artifact  [first in 42/663 visits that checked it]
more:         6 further checks (E300, E301, E305, E302, E303, E304), load on request
enough when:  top option >= 47% (lower quartile over 788 visits) or >= 12 points ahead; median 5 checks
come back:    after 'after a new best' (10/27); after 'other' (7/27); after 'regression after a single change' (3/27)  [27 returns, 9 improved the score]

scores: LLM-guessed; top option matches the option taken in 64% of visits
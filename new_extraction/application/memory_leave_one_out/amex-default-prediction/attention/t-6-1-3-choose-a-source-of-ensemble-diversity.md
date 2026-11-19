# [Choose a source of ensemble diversity › Which source of different prediction errors should be added?]   234 visits, 33 experts

options: Add a different model family (82) | Blend different input views (22) | Blend different prediction heads (5) | Blend different target encodings (6)

check first: E145 Current members use similar algorithms and have strongly correlated held-out residuals.  imp 0.70 → +Add a different model family  [first in 110/119 visits that checked it]
then:        E146 Available modalities or feature representations are not covered by current members.  imp 0.80 → +Blend different input views  [first in 57/79 visits that checked it]
then:        E149 A candidate’s held-out errors are almost identical to those of an existing member.  imp 0.70 → -Add a different model family  [first in 12/44 visits that checked it]
more:         2 further checks (E148, E147), load on request
enough when:  top option >= 36% (lower quartile over 198 visits) or >= 12 points ahead; median 1 checks
come back:    after 'other' (4/10); after 'after a new best' (4/10); after '4+ scored steps without a new best' (1/10)  [10 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 69% of visits
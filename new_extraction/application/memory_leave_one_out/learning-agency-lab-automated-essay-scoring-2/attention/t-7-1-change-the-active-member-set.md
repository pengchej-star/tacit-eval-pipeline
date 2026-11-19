# [Change the active member set › What membership experiment is justified by the existing component evidence?]   371 visits, 31 experts

options: Trial one additional candidate (44) | Replace one ensemble slot (15) | Ablate or prune active members (52) | Compare a member with the ensemble (37) | Restore a proven diverse blend (16)

check first: E150 A compatible unused candidate has reasonable standalone predictions and potentially different residual errors.  imp 0.55 → +Trial one additional candidate  [first in 177/190 visits that checked it]
then:        E152 An active member has repeatedly worsened the fixed blend or seems redundant.  imp 0.70 → -Ablate or prune active members  [first in 83/139 visits that checked it]
then:        E153 No same-split comparison establishes that the ensemble beats its strongest member.  imp 0.85 → +Compare a member with the ensemble  [first in 56/126 visits that checked it]
more:         2 further checks (E154, E151), load on request
enough when:  top option >= 32% (lower quartile over 365 visits) or >= 12 points ahead; median 2 checks
come back:    after 'after a new best' (10/26); after '4+ scored steps without a new best' (7/26); after 'regression after a single change' (5/26)  [26 returns, 8 improved the score]

scores: LLM-guessed; top option matches the option taken in 48% of visits
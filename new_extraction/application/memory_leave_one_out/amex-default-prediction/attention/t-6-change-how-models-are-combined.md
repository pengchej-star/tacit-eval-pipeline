# [Change how models are combined › Which ensemble intervention should be tested next?]   1046 visits, 54 experts

options: Change ensemble membership (291) | Choose a prediction combiner (126) | Choose the space for averaging (32) | Change the stacker inputs (18) | Bound blend-search effort (2)

check first: E135 Members have not been ablated or unused complementary checkpoints exist.  imp 0.85 → +Change ensemble membership  [first in 747/762 visits that checked it]
then:        E136 The member set is stable but its averaging or stacking rule has not been compared.  imp 0.90 → +Choose a prediction combiner  [first in 223/403 visits that checked it]
then:        E137 Member outputs differ in scale, calibration, or activation semantics.  imp 0.75 → +Choose the space for averaging  [first in 42/103 visits that checked it]
more:         2 further checks (E138, E139), load on request
enough when:  top option >= 44% (lower quartile over 1034 visits) or >= 14 points ahead; median 1 checks
come back:    after 'other' (7/24); after '4+ scored steps without a new best' (7/24); after 'regression after a single change' (4/24)  [24 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 90% of visits
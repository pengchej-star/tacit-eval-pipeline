# [Restore model compatibility › Which saved training contract is violated at inference?]   152 visits, 33 experts

options: Match architecture and weights (18) | Restore training preprocessing (36) | Repair dependencies and devices (21)

check first: E02 The model loads, but tokenization, normalization, feature order, or input shape differs from training.  imp 0.92 → +Restore training preprocessing  [first in 68/93 visits that checked it]
then:        E03 Execution stops at an import, file lookup, API call, or device transfer.  imp 0.88 → +Repair dependencies and devices  [first in 54/125 visits that checked it]
then:        E01 The checkpoint reports missing keys or incompatible layer dimensions.  imp 0.95 → +Match architecture and weights  [first in 23/74 visits that checked it]
more:         6 further checks (E124, E129, E128, E125, E127, E126), load on request
enough when:  top option >= 77% (lower quartile over 150 visits) or >= 63 points ahead; median 2 checks
come back:    after 'other' (3/8); after '4+ scored steps without a new best' (2/8); after '3 scored steps without a new best' (1/8)  [8 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 84% of visits
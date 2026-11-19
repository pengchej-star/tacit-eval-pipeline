# [Choose the averaging domain › In which score space should the fixed predictions be combined?]   68 visits, 12 experts

options: Average unranked predictions (4) | Choose raw or rank-space averaging (16) | Choose probability or logit-space aggregation (6)

check first: E91 The metric depends on ordering and members use incompatible output scales or target transforms.  imp 0.65 → +Choose raw or rank-space averaging  [first in 39/47 visits that checked it]
then:        E94 The upstream model changed after the last raw-versus-rank comparison.  imp 0.50 → +Choose raw or rank-space averaging  [first in 14/56 visits that checked it]
then:        E93 The task scores probability distributions and logits are available before normalization.  imp 0.85 → +Choose probability or logit-space aggregation  [first in 12/28 visits that checked it]
more:         5 further checks (E92, E234, E232, E235, E233), load on request
enough when:  top option >= 61% (lower quartile over 68 visits) or >= 36 points ahead; median 4 checks
come back:    after '2 scored steps without a new best' (1/2); after 'other' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 69% of visits
# [Change the learning information › Which part of the available information should I change next?]   622 visits, 39 experts

options: Change training examples (30) | Choose a replacement representation (155) | Choose feature retention (50)

check first: E50 Current inputs discard available temporal, semantic, spatial, or domain information.  imp 0.75 → +Choose a replacement representation  [first in 323/365 visits that checked it]
then:        E51 Many feature blocks are redundant, noisy, or absent from a stale selection artifact.  imp 0.65 → +Choose feature retention  [first in 129/220 visits that checked it]
then:        E49 The training population contains questionable labels, imbalance, or unused compatible examples.  imp 0.45 → +Change training examples  [first in 105/115 visits that checked it]
more:         3 further checks (E148, E149, E150), load on request
enough when:  top option >= 54% (lower quartile over 605 visits) or >= 28 points ahead; median 1 checks
come back:    after 'other' (3/8); after 'after a new best' (3/8); after '4+ scored steps without a new best' (1/8)  [8 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 87% of visits
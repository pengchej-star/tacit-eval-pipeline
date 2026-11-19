# [Choose an ordinal mapping › Which mapping from continuous scores to discrete labels is supported?]   75 visits, 10 experts

options: Tune ordinal cutpoints (32) | Match discrete label frequencies (3) | Use subgroup-specific cutpoints (2) | Test explicit tie handling (2)

check first: E177 Targets occupy a finite ordered set and continuous outputs need a discrete mapping.  imp 0.85 → +Tune ordinal cutpoints  [first in 75/75 visits that checked it]
then:        E182 Training and expected test label frequencies differ.  imp 0.72 → +Match discrete label frequencies  [first in 0/37 visits that checked it]
then:        E178 The expected test label proportions are credibly stable relative to training.  imp 0.80 → +Tune ordinal cutpoints  [first in 0/20 visits that checked it]
more:         3 further checks (E180, E179, E181), load on request
enough when:  top option >= 33% (lower quartile over 75 visits) or >= 10 points ahead; median 2 checks
come back:    after 'regression after a single change' (1/4); after '4+ scored steps without a new best' (1/4); after 'other' (1/4)  [4 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 51% of visits
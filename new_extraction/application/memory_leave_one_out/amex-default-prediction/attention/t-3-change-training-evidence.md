# [Change training evidence › Which change to supervision should be tested next?]   77 visits, 14 experts

options: Change how labeled rows are used (17) | Add training supervision (7) | Change the training target (9)

check first: E48 Existing training rows contain suspected label errors, duplicates, imbalance, or identifiable source shift.  imp 0.82 → +Change how labeled rows are used  [first in 41/41 visits that checked it]
then:        E49 Compatible auxiliary labeled or unlabeled examples are available but unused.  imp 0.85 → +Add training supervision  [first in 17/26 visits that checked it]
then:        E50 The present target ignores censoring, metric-relevant groups, or a reversible offset.  imp 0.75 → +Change the training target  [first in 12/17 visits that checked it]
more:         3 further checks (E257, E259, E258), load on request
enough when:  top option >= 69% (lower quartile over 77 visits) or >= 50 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (2/4); after 'after a new best' (2/4)  [4 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 94% of visits
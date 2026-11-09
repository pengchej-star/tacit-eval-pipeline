# [Choose training examples › Which change to the training population is justified?]   82 visits, 12 experts

options: Filter or deduplicate training data (9) | Add labeled auxiliary data (4) | Use pseudo-labeled examples (3) | Reweight or resample subpopulations (8) | Interpolate training examples (3)

check first: E78 A class or test-representative subgroup is underexposed during training.  imp 0.75 → +Reweight or resample subpopulations  [first in 32/42 visits that checked it]
then:        E75 Duplicates, overlapping windows, unreliable labels, or mismatched sources are identifiable.  imp 0.85 → +Filter or deduplicate training data  [first in 19/28 visits that checked it]
then:        E76 Additional labeled data with compatible input and label definitions exists.  imp 0.85 → +Add labeled auxiliary data  [first in 14/17 visits that checked it]
more:         12 further checks (E77, E233, E80, E235, E232, E238, E237, E239, E234, E236, E240, E79), load on request
enough when:  top option >= 39% (lower quartile over 82 visits) or >= 12 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (1/3); after 'after a new best' (1/3); after 'regression after a bundled change' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 72% of visits
# [Choose the training examples › How should the training sample distribution change?]   102 visits, 14 experts

options: Filter or curate examples (10) | Reweight observed examples (7) | Augment labeled examples (11) | Add auxiliary labeled data (3) | Use pseudo-labeled examples (3)

check first: E39 Low-confidence labels, duplicates, or a mismatched source subset can be identified.  imp 0.85 → +Filter or curate examples  [first in 28/31 visits that checked it]
then:        E40 Rare classes or relevant subgroups contribute too little to the current objective.  imp 0.70 → +Reweight observed examples  [first in 26/38 visits that checked it]
then:        E41 The training set is small or imbalanced and plausible label-preserving transformations exist.  imp 0.80 → +Augment labeled examples  [first in 20/25 visits that checked it]
more:         4 further checks (E42, E44, E43, E45), load on request
enough when:  top option >= 39% (lower quartile over 101 visits) or >= 15 points ahead; median 1 checks
come back:    after 'after a new best' (2/4); after '4+ scored steps without a new best' (1/4); after 'regression after a bundled change' (1/4)  [4 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 86% of visits
# [Change feature retention or preprocessing › How should the existing feature matrix be simplified or made usable?]   130 visits, 15 experts

options: Select features by validated importance (29) | Ablate a feature family (17) | Drop sparse or invalid columns (3) | Use native feature handling (4) | Impute and encode explicitly (4) | Coarsen continuous features (2)

check first: E77 A large engineered feature matrix contains low-importance or redundant dimensions.  imp 0.85 → +Select features by validated importance  [first in 85/94 visits that checked it]
then:        E78 One recently added or removed feature block has uncertain marginal value.  imp 0.80 → +Ablate a feature family  [first in 22/70 visits that checked it]
then:        E81 A model requires finite inputs or the test set contains unseen categories.  imp 0.70 → +Impute and encode explicitly  [first in 8/11 visits that checked it]
more:         3 further checks (E80, E82, E79), load on request
enough when:  top option >= 48% (lower quartile over 130 visits) or >= 26 points ahead; median 2 checks
come back:    after 'other' (4/10); after '2 scored steps without a new best' (3/10); after 'after a new best' (2/10)  [10 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 72% of visits
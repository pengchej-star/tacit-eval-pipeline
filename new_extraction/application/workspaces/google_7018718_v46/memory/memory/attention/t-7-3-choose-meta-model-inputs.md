# [Choose meta-model inputs › Which stacking feature change should I test?]   50 visits, 11 experts

options: Generate valid out-of-fold meta-features (9) | Add auxiliary stacking features (10) | Select a smaller meta-feature set (5)

check first: E150 The meta-feature pool has grown while validation stagnates or regresses.  imp 0.75 → +Select a smaller meta-feature set  [first in 16/35 visits that checked it]
then:        E149 Additional aligned auxiliary outputs provide signal not captured by existing base scores.  imp 0.80 → +Add auxiliary stacking features  [first in 10/18 visits that checked it]
then:        E314 Fold-specific or pre-trained model checkpoints are available for generating out-of-fold predictions for a candidate meta-feature source.  imp 0.75 → +Add auxiliary stacking features  [first in 7/32 visits that checked it]
more:         6 further checks (E313, E148, E311, E312, E315, E316), load on request
enough when:  top option >= 64% (lower quartile over 49 visits) or >= 43 points ahead; median 3 checks
come back:    after 'other' (2/4); after '4+ scored steps without a new best' (2/4)  [4 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 63% of visits
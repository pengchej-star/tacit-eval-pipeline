# [Select a trained artifact › Which checkpoint comparison should I perform?]   120 visits, 19 experts

options: Compare trained runs or folds (32) | Compare training stages or stopping rules (9) | Compare full-data and fold-trained weights (2)

check first: E126 Several runs or fold checkpoints have matching architecture and preprocessing.  imp 0.50 → +Compare trained runs or folds  [first in 111/120 visits that checked it]
then:        E127 Artifacts differ mainly by training stage or stopping criterion.  imp 0.70 → +Compare training stages or stopping rules  [first in 7/78 visits that checked it]
then:        E128 Both full-data-trained and fold-trained artifacts are available.  imp 0.80 → +Compare full-data and fold-trained weights  [first in 2/10 visits that checked it]
enough when:  top option >= 41% (lower quartile over 120 visits) or >= 11 points ahead; median 2 checks
come back:    after 'after a new best' (3/5); after '4+ scored steps without a new best' (2/5)  [5 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 63% of visits
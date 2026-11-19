# [Bound memory with chunks and sequential loads › Which memory allocation should be reduced?]   40 visits, 13 experts

options: Stream complete sample groups (4) | Release completed stages (20)

check first: E123 Memory accumulates across completed models or feature stages.  imp 0.75 → +Release completed stages  [first in 31/38 visits that checked it]
then:        E122 The dataset or feature matrix is too large even with only one model loaded.  imp 0.85 → +Stream complete sample groups  [first in 6/18 visits that checked it]
then:        E213 Premature deletion of a variable (e.g., X_train_fold) causes errors because a later pipeline stage still references it.  imp 0.30 → +Stream complete sample groups  [first in 2/21 visits that checked it]
more:         2 further checks (E212, E211), load on request
enough when:  top option >= 77% (lower quartile over 40 visits) or >= 54 points ahead; median 2 checks
come back:    after 'other' (2/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 95% of visits
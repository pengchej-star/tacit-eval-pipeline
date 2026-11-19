# [Choose validation evidence › Which validation construction best matches the intended prediction setting?]   54 visits, 10 experts

options: Use target-stratified folds (6) | Use disjoint group-aware folds (5) | Audit subgroup-specific fold construction (4) | Adjust held-out training allocation (4) | Audit validation against held-out rankings (3)

check first: E18 Local validation and external evaluation rank the same candidate models differently.  imp 0.72 → +Audit validation against held-out rankings  [first in 14/25 visits that checked it]
then:        E16 A known training subgroup differs from the expected test population.  imp 0.70 → +Audit subgroup-specific fold construction  [first in 10/22 visits that checked it]
then:        E14 Target imbalance or sparse target ranges leave random folds unrepresentative.  imp 0.82 → +Use target-stratified folds  [first in 9/14 visits that checked it]
more:         14 further checks (E17, E126, E15, E131, E122, E128, E125, E124, E19, E129, E132, E123, E127, E130), load on request
enough when:  top option >= 51% (lower quartile over 54 visits) or >= 23 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 74% of visits
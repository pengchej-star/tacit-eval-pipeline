# [Change numerical preprocessing › Which numerical preprocessing policy fits the inputs and estimator?]   12 visits, 5 experts

options: Preserve native tree inputs (4) | Use model-specific imputation (1) | Coarsen noisy numerical precision (2)

check first: E82 The current tree implementation handles missing values and added preprocessing erases missingness or removes useful extremes.  imp 0.85 → +Preserve native tree inputs  [first in 6/7 visits that checked it]
then:        E84 Low-precision storage creates spurious fine-scale differences relative to meaningful measurement resolution.  imp 0.80 → +Coarsen noisy numerical precision  [first in 3/3 visits that checked it]
then:        E268 The existing preprocessing code contains an implementation bug that prevents it from executing correctly and must be fixed before evaluating the preprocessing strategy.  imp 0.55 → +Use model-specific imputation  [first in 2/4 visits that checked it]
more:         1 further checks (E83), load on request
enough when:  top option >= 69% (lower quartile over 12 visits) or >= 49 points ahead; median 2 checks
come back:    after '2 scored steps without a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 83% of visits
# [Choose missing-value treatment › Should missing values be left native, explicitly imputed or accompanied by simpler numeric preprocessing?]   18 visits, 6 experts

options: Use native missing-value handling (3) | Impute and encode for the consuming model (4) | Simplify numerical preprocessing (3)

check first: E53 The active neural or other estimator fails on NaNs or unseen categorical values.  imp 0.90 → +Impute and encode for the consuming model  [first in 7/14 visits that checked it]
then:        E52 The active estimator supports NaNs and prior imputation erased useful missingness patterns.  imp 0.85 → +Use native missing-value handling  [first in 5/9 visits that checked it]
then:        E54 Scaling, rounding or sparse-column filtering has no demonstrated benefit for the active tree model.  imp 0.60 → -Simplify numerical preprocessing  [first in 5/8 visits that checked it]
more:         1 further checks (E183), load on request
enough when:  top option >= 84% (lower quartile over 18 visits) or >= 70 points ahead; median 2 checks
come back:    after '2 scored steps without a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 83% of visits
# [Change the validation population › Which allocation of training and validation examples should be used?]   40 visits, 12 experts

options: Stratify independent examples (3) | Keep related examples together (3) | Validate on the target population (6) | Use ordinary out-of-fold validation (8) | Resize the development holdout (1)

check first: E30 The expected test population matches only an identifiable subset of training data.  imp 0.85 → +Validate on the target population  [first in 12/16 visits that checked it]
then:        E31 Stacking or calibration currently uses predictions fitted on their own training labels.  imp 0.40 → +Use ordinary out-of-fold validation  [first in 9/9 visits that checked it]
then:        E29 Rows share entities, overlapping signals, or near-duplicate content across folds.  imp 0.75 → +Keep related examples together  [first in 6/13 visits that checked it]
more:         14 further checks (E28, E177, E178, E32, E33, E181, E184, E186, E182, E187, E180, E183, E179, E185), load on request
enough when:  top option >= 34% (lower quartile over 40 visits) or >= 11 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (2/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 62% of visits
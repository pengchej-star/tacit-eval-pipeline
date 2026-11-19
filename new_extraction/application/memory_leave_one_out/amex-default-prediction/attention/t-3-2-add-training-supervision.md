# [Add training supervision › Which additional source of supervision can be tested?]   24 visits, 3 experts

options: Add filtered labeled data (4) | Use pseudo-labeled examples (3)

check first: E57 Additional labeled examples have compatible targets and observable quality indicators.  imp 0.85 → +Add filtered labeled data  [first in 11/17 visits that checked it]
then:        E275 Previous attempts to include extra data in training consistently failed to beat the best score without extra data.  imp 0.65 → -Add filtered labeled data  [first in 6/22 visits that checked it]
then:        E274 The pseudo-labeled model's standalone score is competitive with the component it would replace in the ensemble.  imp 0.75 → +Use pseudo-labeled examples  [first in 2/5 visits that checked it]
more:         8 further checks (E58, E280, E276, E277, E279, E278, E281, E59), load on request
enough when:  top option >= 77% (lower quartile over 24 visits) or >= 54 points ahead; median 5 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 83% of visits
# [Change the model or fitting procedure › Which single-model limitation should be addressed next?]   325 visits, 43 experts

options: Change the predictor family (31) | Change the prediction head (18) | Change tree fitting (24) | Change neural optimization (16) | Change training duration or checkpoint use (47)

check first: E119 The available trained states differ more than recent architecture changes or stopping is poorly configured.  imp 0.82 → +Change training duration or checkpoint use  [first in 117/149 visits that checked it]
then:        E117 A tree model’s capacity, regularization, or round budget is implicated by learning curves.  imp 0.85 → +Change tree fitting  [first in 95/172 visits that checked it]
then:        E115 The current predictor’s inductive bias or pretraining domain appears unsuitable.  imp 0.90 → +Change the predictor family  [first in 47/88 visits that checked it]
more:         4 further checks (E116, E118, E289, E290), load on request
enough when:  top option >= 44% (lower quartile over 321 visits) or >= 19 points ahead; median 3 checks
come back:    after '2 scored steps without a new best' (6/21); after 'other' (5/21); after 'after a new best' (5/21)  [21 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 87% of visits
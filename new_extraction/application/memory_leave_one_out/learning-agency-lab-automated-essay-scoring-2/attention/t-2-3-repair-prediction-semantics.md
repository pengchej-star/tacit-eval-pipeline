# [Repair prediction semantics › Which numerical mismatch explains the implausible predictions?]   36 visits, 14 experts

options: Align prediction units and direction (7) | Correct ensemble arithmetic (11) | Locate non-finite values (1) | Correct the prediction or preprocessing API (4)

check first: E43 Ensemble scale changes after member removal or the formula uses list arithmetic or an incorrect denominator.  imp 0.85 → +Correct ensemble arithmetic  [first in 19/26 visits that checked it]
then:        E45 The called method or argument belongs to a different API wrapper than the instantiated object.  imp 0.80 → +Correct the prediction or preprocessing API  [first in 7/10 visits that checked it]
then:        E42 Prediction units or monotonic direction disagree with the labels or other members.  imp 0.92 → +Align prediction units and direction  [first in 7/9 visits that checked it]
more:         2 further checks (E224, E44), load on request
enough when:  top option >= 64% (lower quartile over 35 visits) or >= 51 points ahead; median 1 checks
come back:    after '2 scored steps without a new best' (1/2); after 'regression after a single change' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 91% of visits
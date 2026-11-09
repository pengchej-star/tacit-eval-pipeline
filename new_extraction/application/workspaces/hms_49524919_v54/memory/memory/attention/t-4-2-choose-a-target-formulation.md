# [Choose a target formulation › Which supervision representation should I test?]   19 visits, 7 experts

options: Transform censored outcomes (3) | Construct targets within evaluation groups (2) | Tune target centering or transformation strength (3) | Use ordinal or classification supervision (3)

check first: E81 Targets contain event times and censoring indicators rather than fully observed outcomes.  imp 0.90 → +Transform censored outcomes  [first in 12/19 visits that checked it]
then:        E84 Labels are ordered discrete levels but the current model is plain regression.  imp 0.85 → +Use ordinal or classification supervision  [first in 6/15 visits that checked it]
then:        E83 A scalar target transform or centering convention changed or remains untuned.  imp 0.65 → +Tune target centering or transformation strength  [first in 1/11 visits that checked it]
more:         3 further checks (E82, E242, E241), load on request
enough when:  top option >= 79% (lower quartile over 19 visits) or >= 60 points ahead; median 5 checks
come back:    after 'other' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 58% of visits
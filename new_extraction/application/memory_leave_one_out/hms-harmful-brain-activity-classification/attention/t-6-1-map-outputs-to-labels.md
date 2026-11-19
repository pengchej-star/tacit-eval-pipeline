# [Map outputs to labels › How should continuous predictions be mapped to the target support?]   79 visits, 11 experts

options: Retain raw continuous predictions (5) | Use simple fixed rounding or bins (12) | Optimize ordered thresholds on held-out predictions (17) | Test target-frequency mapping (4) | Compare global and group-specific calibration (3)

check first: E95 Labels occupy known ordered levels and learned thresholds are not reliably better.  imp 0.55 → +Use simple fixed rounding or bins  [first in 31/44 visits that checked it]
then:        E94 The metric depends on order and proposed transformations only erase or perturb useful ordering.  imp 0.60 → +Retain raw continuous predictions  [first in 22/33 visits that checked it]
then:        E96 Continuous outputs carry signal but fixed cutpoints systematically misallocate ordinal labels.  imp 0.75 → +Optimize ordered thresholds on held-out predictions  [first in 11/24 visits that checked it]
more:         3 further checks (E97, E98, E99), load on request
enough when:  top option >= 41% (lower quartile over 77 visits) or >= 18 points ahead; median 2 checks
come back:    after 'regression after a single change' (2/5); after 'regression after a bundled change' (1/5); after '2 scored steps without a new best' (1/5)  [5 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 77% of visits
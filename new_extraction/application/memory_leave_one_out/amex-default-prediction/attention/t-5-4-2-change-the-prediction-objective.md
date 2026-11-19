# [Change the prediction objective › Which objective better matches the target and evaluation rule?]   30 visits, 9 experts

options: Train against distributional error (1) | Use independent output losses (2) | Train pairwise ordering (1) | Use an ordinal formulation (4) | Validate and tune a custom objective (4) | Add an auxiliary target head (3)

check first: E124 Targets are probability distributions and the evaluation uses distributional divergence.  imp 0.95 → +Train against distributional error  [first in 17/29 visits that checked it]
then:        E128 A custom differentiable objective is already used and its constants or derivatives are unverified.  imp 0.80 → +Validate and tune a custom objective  [first in 6/10 visits that checked it]
then:        E127 Labels occupy an ordered finite scale.  imp 0.85 → +Use an ordinal formulation  [first in 4/24 visits that checked it]
more:         3 further checks (E125, E126, E129), load on request
enough when:  top option >= 40% (lower quartile over 30 visits) or >= 7 points ahead; median 3 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 60% of visits
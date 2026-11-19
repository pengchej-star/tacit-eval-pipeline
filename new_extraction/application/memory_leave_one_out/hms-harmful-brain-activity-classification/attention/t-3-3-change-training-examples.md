# [Change training examples › Which training-population adjustment should I test?]   50 visits, 10 experts

options: Filter or down-weight noisy and mismatched examples (4) | Tune class or subgroup weights (7) | Test synthetic feature-space augmentation (3) | Tune label-preserving image augmentation (4)

check first: E45 Rare classes or target-like subgroups have insufficient influence on fitting.  imp 0.70 → +Tune class or subgroup weights  [first in 23/34 visits that checked it]
then:        E44 A known subset has unreliable labels or differs from the intended test population.  imp 0.75 → +Filter or down-weight noisy and mismatched examples  [first in 15/16 visits that checked it]
then:        E47 Training images exhibit nuisance variation that valid augmentation could reproduce.  imp 0.80 → +Tune label-preserving image augmentation  [first in 6/30 visits that checked it]
more:         9 further checks (E133, E134, E135, E137, E139, E136, E140, E138, E46), load on request
enough when:  top option >= 45% (lower quartile over 50 visits) or >= 17 points ahead; median 5 checks
come back:    after 'after a new best' (1/2); after 'regression after a bundled change' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 66% of visits
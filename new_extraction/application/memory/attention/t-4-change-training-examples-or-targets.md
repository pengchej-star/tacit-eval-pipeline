# [Change training examples or targets › Which data or target intervention should I test?]   114 visits, 17 experts

options: Choose training examples (27) | Choose a target formulation (11) | Choose training augmentation (4)

check first: E72 Sample quality, class proportions, or source coverage differ from the intended test population.  imp 0.70 → +Choose training examples  [first in 65/67 visits that checked it]
then:        E73 The label definition includes censoring, ordinal levels, or group-specific ranking.  imp 0.75 → +Choose a target formulation  [first in 19/67 visits that checked it]
then:        E74 A neural model overfits and the input admits label-preserving perturbations.  imp 0.80 → +Choose training augmentation  [first in 9/38 visits that checked it]
more:         3 further checks (E229, E231, E230), load on request
enough when:  top option >= 53% (lower quartile over 101 visits) or >= 15 points ahead; median 2 checks
come back:    after 'after a new best' (3/4); after '4+ scored steps without a new best' (1/4)  [4 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 51% of visits
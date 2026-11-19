# [Choose ordinal output conversion › Should outputs use optimized boundaries, simple rounding or retain their existing values?]   94 visits, 12 experts

options: Fit or simplify ordinal thresholds (45) | Use simple rounding (1) | Preserve the current output mapping (4)

check first: E111 Targets occupy discrete ordered levels and the metric is sensitive to class boundaries or ties.  imp 0.85 → +Fit or simplify ordinal thresholds  [first in 87/88 visits that checked it]
then:        E113 The metric is unchanged by strictly monotone rescaling and no discretization gain has been established.  imp 0.75 → +Preserve the current output mapping  [first in 5/81 visits that checked it]
then:        E116 The current output is already valid and additional random perturbations only reorder close predictions.  imp 0.65 → +Preserve the current output mapping  [first in 2/12 visits that checked it]
more:         12 further checks (E265, E114, E261, E263, E266, E268, E262, E115, E264, E269, E267, E112), load on request
enough when:  top option >= 84% (lower quartile over 94 visits) or >= 68 points ahead; median 5 checks
come back:    after 'regression after a single change' (1/2); after '2 scored steps without a new best' (1/2)  [2 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 93% of visits
# [Choose feature retention › How should I reduce or refresh the feature set?]   117 visits, 11 experts

options: Tune the importance cutoff (12) | Ablate whole feature blocks (20) | Refit feature selection without leakage (18)

check first: E47 A recognizable feature block was recently added or removed with uncertain benefit.  imp 0.78 → +Ablate whole feature blocks  [first in 48/80 visits that checked it]
then:        E46 An importance-ranked list exists but its retention count is arbitrary or aggressive.  imp 0.72 → +Tune the importance cutoff  [first in 47/57 visits that checked it]
then:        E48 Feature sources changed after the selection artifact was fitted, or selection used validation labels.  imp 0.85 → +Refit feature selection without leakage  [first in 21/36 visits that checked it]
more:         7 further checks (E164, E163, E162, E167, E166, E161, E165), load on request
enough when:  top option >= 61% (lower quartile over 117 visits) or >= 29 points ahead; median 3 checks
come back:    after 'other' (2/9); after 'after a new best' (2/9); after '4+ scored steps without a new best' (2/9)  [9 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 84% of visits
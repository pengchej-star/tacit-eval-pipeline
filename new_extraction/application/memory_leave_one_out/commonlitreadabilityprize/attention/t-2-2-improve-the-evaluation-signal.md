# [Improve the evaluation signal › Should the validation rows or the scoring rule be changed?]   86 visits, 17 experts

options: Choose validation membership (27) | Use the target metric for model selection (13)

check first: E27 Current folds leak related rows or poorly represent the target population.  imp 0.85 → +Choose validation membership  [first in 28/28 visits that checked it]
then:        E28 Training selects checkpoints using a different objective direction or output convention from the task metric.  imp 0.80 → +Use the target metric for model selection  [first in 17/18 visits that checked it]
then:        E29 The exact task metric is unstable across epochs while a smooth surrogate tracks held-out generalization better.  imp 0.90 → +Use the target metric for model selection  [first in 13/14 visits that checked it]
more:         3 further checks (E140, E139, E138), load on request
enough when:  top option >= 83% (lower quartile over 67 visits) or >= 66 points ahead; median 1 checks
come back:    after 'after a new best' (2/4); after '4+ scored steps without a new best' (2/4)  [4 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 96% of visits
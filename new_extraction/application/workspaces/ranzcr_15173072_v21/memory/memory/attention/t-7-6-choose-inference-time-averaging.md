# [Choose inference-time averaging › Which repeated-view inference strategy should I test?]   56 visits, 13 experts

options: Average deterministic symmetry views (14) | Average windows or resolutions (3) | Compare stochastic forward-pass averaging (6) | Disable unintended stochastic inference (9)

check first: E165 A deterministic flip or sensor symmetry preserves the label.  imp 0.82 → +Average deterministic symmetry views  [first in 20/31 visits that checked it]
then:        E168 Repeated passes should be identical but differ because training-mode layers or random transforms remain active.  imp 0.80 → +Disable unintended stochastic inference  [first in 11/19 visits that checked it]
then:        E167 Repeated forward passes intentionally vary and prior stochastic-view evidence is promising.  imp 0.88 → +Compare stochastic forward-pass averaging  [first in 7/15 visits that checked it]
more:         8 further checks (E166, E325, E326, E169, E329, E328, E327, E330), load on request
enough when:  top option >= 47% (lower quartile over 56 visits) or >= 17 points ahead; median 5 checks
come back:    after '4+ scored steps without a new best' (1/2); after 'after a new best' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 61% of visits
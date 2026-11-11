# [Change repeated-model aggregation › Which repeated prediction source should be added or selected?]   169 visits, 31 experts

options: Select and average fold checkpoints (43) | Weight fold predictions by evidence (6) | Average independent training runs (17) | Average valid input views (16) | Average stochastic forward passes (3) | Average compatible model weights (1) | Use deterministic evaluation mode (4)

check first: E127 Only part of an available compatible cross-validation checkpoint set is used.  imp 0.92 → +Select and average fold checkpoints  [first in 91/99 visits that checked it]
then:        E129 Independent training seeds produce materially different errors.  imp 0.60 → +Average independent training runs  [first in 25/35 visits that checked it]
then:        E130 Input transformations preserve target meaning and were supported by the training representation.  imp 0.72 → +Average valid input views  [first in 24/25 visits that checked it]
more:         4 further checks (E128, E131, E133, E132), load on request
enough when:  top option >= 30% (lower quartile over 163 visits) or >= 12 points ahead; median 1 checks
come back:    after 'after a new best' (5/8); after '4+ scored steps without a new best' (2/8); after '2 scored steps without a new best' (1/8)  [8 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 66% of visits
# [Change the stacking stage › What change to learned stacking is supported by the current evidence?]   64 visits, 7 experts

options: Compare learned stacking with averaging (14) | Compare meta-learner families (6) | Tune meta-learner regularization (5) | Change the stacker’s feature set (10)

check first: E173 A fixed blend has plateaued and enough aligned held-out base predictions exist to fit a small combiner.  imp 0.60 → +Compare learned stacking with averaging  [first in 35/37 visits that checked it]
then:        E174 The current stacker’s model class underfits or a complex stacker overfits the available meta-data.  imp 0.70 → +Compare meta-learner families  [first in 8/16 visits that checked it]
then:        E176 Useful new OOF outputs or embeddings exist, or the current meta-feature schema contains weak redundant columns.  imp 0.70 → +Change the stacker’s feature set  [first in 7/26 visits that checked it]
more:         10 further checks (E175, E326, E327, E334, E330, E333, E331, E329, E328, E332), load on request
enough when:  top option >= 39% (lower quartile over 64 visits) or >= 9 points ahead; median 4 checks
come back:    after 'after a new best' (2/3); after '3 scored steps without a new best' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 59% of visits
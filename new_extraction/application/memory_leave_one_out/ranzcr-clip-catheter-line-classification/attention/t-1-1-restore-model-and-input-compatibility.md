# [Restore model and input compatibility › Which saved training contract is violated at inference?]   82 visits, 20 experts

options: Match architecture and weights (12) | Restore the training tokenizer (7) | Restore training preprocessing (18) | Repair row and feature alignment (7)

check first: E03 The same raw sample receives different feature values in training and inference.  imp 0.90 → +Restore training preprocessing  [first in 29/31 visits that checked it]
then:        E01 Checkpoint keys or tensor dimensions do not match the instantiated model.  imp 0.95 → +Match architecture and weights  [first in 20/46 visits that checked it]
then:        E02 Tokenizer vocabulary or special-token handling differs from the fine-tuning artifact.  imp 0.90 → +Restore the training tokenizer  [first in 13/28 visits that checked it]
more:         6 further checks (E04, E163, E160, E162, E164, E161), load on request
enough when:  top option >= 65% (lower quartile over 82 visits) or >= 45 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (2/4); after 'regression after a single change' (1/4); after 'regression after a bundled change' (1/4)  [4 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 93% of visits
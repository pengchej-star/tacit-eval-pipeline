# [Restore model and input compatibility › Which training-to-inference contract is broken?]   118 visits, 26 experts

options: Match architecture and weights (23) | Match input preprocessing (20) | Match tokenizer and vocabulary (6) | Match feature schema and encoders (15)

check first: E30 Checkpoint keys or tensor dimensions disagree with the reconstructed model.  imp 0.90 → +Match architecture and weights  [first in 34/46 visits that checked it]
then:        E31 Inference transforms differ from those recorded for the training checkpoint.  imp 0.85 → +Match input preprocessing  [first in 30/40 visits that checked it]
then:        E33 A downstream model receives different columns, encodings, or dimensions from those used in fitting.  imp 0.90 → +Match feature schema and encoders  [first in 24/30 visits that checked it]
more:         7 further checks (E32, E207, E206, E205, E202, E204, E203), load on request
enough when:  top option >= 58% (lower quartile over 117 visits) or >= 38 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (4/7); after 'regression after a single change' (1/7); after 'after a new best' (1/7)  [7 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 85% of visits
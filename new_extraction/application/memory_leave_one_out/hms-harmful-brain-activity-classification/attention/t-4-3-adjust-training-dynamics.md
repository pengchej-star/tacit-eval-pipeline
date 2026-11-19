# [Adjust training dynamics › Which training control matches the observed learning behavior?]   118 visits, 26 experts

options: Tune tree depth and leaf capacity (17) | Tune penalties, subsampling or dropout (7) | Tune learning rate with sufficient training budget (10) | Tune epochs, rounds or stopping patience (8) | Compare optimizer or learning-rate schedule (3) | Train and persist models with proper cross-validation (4) | Average compatible model weights (1)

check first: E61 Training fit or the train-validation gap suggests an inappropriate tree capacity.  imp 0.85 → +Tune tree depth and leaf capacity  [first in 37/46 visits that checked it]
then:        E63 Training is unstable or stops before a lower-rate run can converge.  imp 0.80 → +Tune learning rate with sufficient training budget  [first in 22/33 visits that checked it]
then:        E64 Validation improvement continues at the cap or has already reversed before the selected checkpoint.  imp 0.75 → +Tune epochs, rounds or stopping patience  [first in 20/34 visits that checked it]
more:         12 further checks (E62, E156, E66, E153, E65, E155, E151, E157, E67, E152, E158, E154), load on request
enough when:  top option >= 31% (lower quartile over 118 visits) or >= 11 points ahead; median 3 checks
come back:    after 'after a new best' (3/9); after 'other' (3/9); after '3 scored steps without a new best' (1/9)  [9 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 75% of visits
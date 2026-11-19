# [Change the predictor › Which predictor change is the most promising replacement experiment?]   207 visits, 22 experts

options: Select a different checkpoint (39) | Replace the model family or capacity (29) | Use domain-adapted weights (2) | Choose the prediction architecture (23)

check first: E67 Compatible checkpoints differ in training history or validation quality.  imp 0.55 → +Select a different checkpoint  [first in 138/149 visits that checked it]
then:        E68 The current model is underpowered or a different inductive bias is supported by prior errors.  imp 0.85 → +Replace the model family or capacity  [first in 42/82 visits that checked it]
then:        E70 A strong backbone uses a limited head or cannot yet combine available branches.  imp 0.60 → +Choose the prediction architecture  [first in 26/48 visits that checked it]
more:         2 further checks (E69, E71), load on request
enough when:  top option >= 41% (lower quartile over 207 visits) or >= 18 points ahead; median 2 checks
come back:    after 'regression after a single change' (3/11); after 'after a new best' (3/11); after '2 scored steps without a new best' (2/11)  [11 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 93% of visits
# [Replace the model family or implementation › Which alternative learner fits the available representation and current limitation?]   83 visits, 17 experts

options: Compare tree learner families (5) | Change the boosting algorithm (4) | Change pretrained backbone or capacity (27) | Compare a classical downstream learner (1) | Use the native training interface (1) | Use an estimator interface (1)

check first: E89 Alternative pretrained backbones or capacities are available with compatible task inputs.  imp 0.88 → +Change pretrained backbone or capacity  [first in 54/56 visits that checked it]
then:        E87 The current tabular learner has plateaued on a stable feature set.  imp 0.72 → +Compare tree learner families  [first in 23/24 visits that checked it]
then:        E240 The proposed alternative was already tried and reverted in a prior iteration, so the replacement has already been evaluated.  imp 0.60 → -Compare tree learner families  [first in 2/77 visits that checked it]
more:         29 further checks (E239, E242, E92, E254, E253, E236, E250, E241, E258, E251, E257, E259, E246, E261, E255, E252, E243, E238, E260, E237, E88, E256, E244, E247, E245, E249, E91, E248, E90), load on request
enough when:  top option >= 48% (lower quartile over 83 visits) or >= 17 points ahead; median 9 checks
come back:    after '3 scored steps without a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 84% of visits
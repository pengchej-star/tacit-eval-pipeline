# [Choose a model family or initialization › Which replacement model should I test as a standalone candidate?]   86 visits, 19 experts

options: Change pretrained backbone or capacity (20) | Use domain-adapted pretraining (2) | Change tree learner or boosting variant (11) | Fit a model for a different representation (3)

check first: E92 A compatible alternative pretrained backbone or size is available.  imp 0.85 → +Change pretrained backbone or capacity  [first in 41/49 visits that checked it]
then:        E94 The features are tabular or fixed vectors and the current tree implementation has plateaued.  imp 0.85 → +Change tree learner or boosting variant  [first in 22/64 visits that checked it]
then:        E95 A meaningful input representation is not served well by the current architecture.  imp 0.75 → +Fit a model for a different representation  [first in 10/16 visits that checked it]
more:         23 further checks (E260, E259, E257, E270, E261, E256, E264, E267, E271, E93, E262, E276, E269, E265, E255, E272, E266, E263, E273, E258, E275, E268, E274), load on request
enough when:  top option >= 53% (lower quartile over 86 visits) or >= 27 points ahead; median 11 checks
come back:    after '4+ scored steps without a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 76% of visits
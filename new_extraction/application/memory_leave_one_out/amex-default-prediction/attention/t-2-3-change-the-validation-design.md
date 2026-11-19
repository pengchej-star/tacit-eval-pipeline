# [Change the validation design › Which split construction best represents the required generalization?]   51 visits, 8 experts

options: Preserve target proportions (3) | Hold related examples together (5) | Derive provisional groups (1) | Tune the validation fold count (5) | Probe subgroup-enriched folds (4)

check first: E40 A known subgroup resembles the test population and is poorly represented in the current folds.  imp 0.65 → +Probe subgroup-enriched folds  [first in 11/25 visits that checked it]
then:        E37 Related examples share an entity or source that must be unseen at evaluation.  imp 0.95 → +Hold related examples together  [first in 11/21 visits that checked it]
then:        E39 The current fold count leaves very small or unstable validation sets.  imp 0.60 → +Tune the validation fold count  [first in 10/14 visits that checked it]
more:         17 further checks (E244, E36, E38, E249, E245, E253, E251, E248, E252, E247, E41, E250, E254, E256, E243, E246, E255), load on request
enough when:  top option >= 38% (lower quartile over 51 visits) or >= 10 points ahead; median 5 checks
come back:    after '4+ scored steps without a new best' (1/2); after 'regression after a single change' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 65% of visits
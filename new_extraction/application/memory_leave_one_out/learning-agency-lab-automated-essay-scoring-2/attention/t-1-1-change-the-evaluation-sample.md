# [Change the evaluation sample › Which evaluation design should replace the current unreliable comparison?]   49 visits, 11 experts

options: Score candidates locally (2) | Balance target distributions across folds (3) | Keep related observations together (2) | Generate aligned out-of-fold predictions (2) | Check local-to-external score agreement (7)

check first: E16 Local and public scores have ranked existing checkpoints differently.  imp 0.78 → +Check local-to-external score agreement  [first in 25/32 visits that checked it]
then:        E12 Several candidate configurations can be scored on an existing representative holdout.  imp 0.92 → +Score candidates locally  [first in 6/13 visits that checked it]
then:        E201 The public test set is too small for single-checkpoint swaps to produce meaningful score differences.  imp 0.70 → +Score candidates locally  [first in 5/16 visits that checked it]
more:         6 further checks (E13, E14, E203, E15, E202, E204), load on request
enough when:  top option >= 55% (lower quartile over 49 visits) or >= 41 points ahead; median 3 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 78% of visits
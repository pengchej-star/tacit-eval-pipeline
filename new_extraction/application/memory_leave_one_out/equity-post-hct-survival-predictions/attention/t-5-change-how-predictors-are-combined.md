# [Change how predictors are combined › Which ensemble intervention should I test next?]   932 visits, 51 experts

options: Choose ensemble membership (241) | Choose the combination rule (138) | Choose repeated inference views (29)

check first: E80 The pool includes untested candidates, redundant members, or unused folds or seeds.  imp 0.20 → +Choose ensemble membership  [first in 615/641 visits that checked it]
then:        E81 The current members are fixed but scale, weights, or combination method remain unresolved.  imp 0.25 → +Choose the combination rule  [first in 255/466 visits that checked it]
then:        E82 The input has valid alternate views or the checkpoint supports useful repeated inference.  imp 0.85 → +Choose the combination rule  [first in 40/94 visits that checked it]
more:         4 further checks (E173, E171, E172, E174), load on request
enough when:  top option >= 38% (lower quartile over 932 visits) or >= 7 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (3/10); after 'other' (2/10); after 'regression after a single change' (2/10)  [10 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 69% of visits
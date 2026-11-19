# [Change ensemble membership › Which membership change should be tested?]   550 visits, 40 experts

options: Add a complementary model (92) | Replace a component with a stronger variant (26) | Prune or restore members by ablation (123) | Change stacker input features (21)

check first: E117 Members are weak, redundant, or untested after the ensemble changed.  imp 0.80 → +Prune or restore members by ablation  [first in 276/374 visits that checked it]
then:        E115 An available model makes useful errors different from the current ensemble.  imp 0.72 → +Add a complementary model  [first in 173/208 visits that checked it]
then:        E116 A component has a compatible retrained variant with better controlled validation results.  imp 0.65 → +Replace a component with a stronger variant  [first in 52/77 visits that checked it]
more:         1 further checks (E118), load on request
enough when:  top option >= 44% (lower quartile over 534 visits) or >= 11 points ahead; median 1 checks
come back:    after 'after a new best' (8/28); after 'regression after a single change' (6/28); after '4+ scored steps without a new best' (6/28)  [28 returns, 12 improved the score]

scores: LLM-guessed; top option matches the option taken in 79% of visits
# [Choose prediction-pool changes › Should the ensemble gain diversity, prune members or average more repeats?]   464 visits, 38 experts

options: Add a complementary ensemble member (54) | Select the ensemble subset (104) | Average additional folds or seeds (37)

check first: E87 A member removal improves held-out performance or the full blend fails to beat its best component.  imp 0.85 → +Select the ensemble subset  [first in 202/262 visits that checked it]
then:        E86 Existing members make highly correlated errors and a reasonable candidate differs in inputs, targets or architecture.  imp 0.60 → +Add a complementary ensemble member  [first in 123/130 visits that checked it]
then:        E88 Additional compatible folds or seeds are available and prior additions reduce prediction variance.  imp 0.70 → +Average additional folds or seeds  [first in 91/177 visits that checked it]
more:         2 further checks (E90, E89), load on request
enough when:  top option >= 55% (lower quartile over 460 visits) or >= 25 points ahead; median 2 checks
come back:    after 'after a new best' (7/16); after '4+ scored steps without a new best' (2/16); after '3 scored steps without a new best' (2/16)  [16 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 77% of visits
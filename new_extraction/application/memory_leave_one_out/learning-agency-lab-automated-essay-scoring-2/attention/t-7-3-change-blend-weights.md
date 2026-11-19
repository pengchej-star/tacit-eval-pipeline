# [Change blend weights › How should the active prediction sources be weighted?]   254 visits, 34 experts

options: Use equal member weights (9) | Optimize fixed blend weights (80) | Test signed blend coefficients (3) | Weight model groups separately (9) | Replace unstable adaptive weights (1) | Test class-specific blend weights (1)

check first: E162 Component quality differs reproducibly or a member’s predictions have changed since weights were tuned.  imp 0.85 → +Optimize fixed blend weights  [first in 123/212 visits that checked it]
then:        E161 Members have comparable quality and tuned weights have not reliably improved the simple average.  imp 0.82 → +Use equal member weights  [first in 104/129 visits that checked it]
then:        E164 Model families contain unequal numbers of folds or variants.  imp 0.75 → +Weight model groups separately  [first in 13/39 visits that checked it]
more:         3 further checks (E165, E163, E166), load on request
enough when:  top option >= 39% (lower quartile over 247 visits) or >= 13 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (4/12); after 'regression after a single change' (2/12); after 'after a new best' (2/12)  [12 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 75% of visits
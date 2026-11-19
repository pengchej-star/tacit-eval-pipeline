# [Change the prediction head › Which head modification should be compared with the current trained head?]   36 visits, 10 experts

options: Enrich the prediction head (9) | Simplify the prediction head (3) | Change representation pooling (3) | Add an auxiliary prediction task (3)

check first: E127 A complex multi-head or normalization design has regressed or overfit.  imp 0.75 → +Simplify the prediction head  [first in 12/25 visits that checked it]
then:        E126 The backbone is strong but its current head is only a minimal projection.  imp 0.82 → +Enrich the prediction head  [first in 12/14 visits that checked it]
then:        E294 An alternative attention/block design is architecturally motivated to capture information (e.g., spatial) that the current block does not.  imp 0.45 → +Enrich the prediction head  [first in 3/9 visits that checked it]
more:         7 further checks (E129, E128, E297, E295, E296, E299, E298), load on request
enough when:  top option >= 50% (lower quartile over 36 visits) or >= 25 points ahead; median 5 checks
come back:    after 'regression after a single change' (2/5); after '4+ scored steps without a new best' (2/5); after 'after a new best' (1/5)  [5 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 69% of visits
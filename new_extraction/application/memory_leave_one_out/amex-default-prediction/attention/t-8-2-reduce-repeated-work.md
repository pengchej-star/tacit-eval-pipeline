# [Reduce repeated work › Which execution change removes the measured iteration bottleneck?]   113 visits, 31 experts

options: Cache expensive intermediate results (18) | Resume completed training stages (3) | Parameterize model execution (36) | Accelerate the measured bottleneck (4)

check first: E200 Adding or removing models requires edits in several inconsistent code locations.  imp 0.75 → +Parameterize model execution  [first in 47/58 visits that checked it]
then:        E198 Expensive features or base predictions are recomputed unchanged during downstream sweeps.  imp 0.92 → +Cache expensive intermediate results  [first in 29/32 visits that checked it]
then:        E199 Completed folds or training stages are repeated because a session cannot finish all work.  imp 0.80 → +Resume completed training stages  [first in 9/15 visits that checked it]
more:         10 further checks (E453, E449, E446, E201, E448, E447, E451, E452, E450, E202), load on request
enough when:  top option >= 45% (lower quartile over 113 visits) or >= 18 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (2/8); after 'after a new best' (2/8); after 'regression after a single change' (1/8)  [8 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 91% of visits
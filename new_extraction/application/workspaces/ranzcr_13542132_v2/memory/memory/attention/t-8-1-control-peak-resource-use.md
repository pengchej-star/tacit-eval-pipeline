# [Control peak resource use › Which resource intervention fits the observed bottleneck?]   66 visits, 21 experts

options: Stream complete entities or prediction batches (5) | Release sequential model state (14) | Reduce stored feature precision (2) | Tune inference batch size (9) | Compare inference precision (3) | Optimize expensive computation (4)

check first: E174 Memory accumulates across successive model loads.  imp 0.75 → +Release sequential model state  [first in 19/28 visits that checked it]
then:        E176 Peak memory occurs inside one forward pass and scales with batch size.  imp 0.80 → +Tune inference batch size  [first in 12/13 visits that checked it]
then:        E173 The full data or feature table cannot fit, but complete entities can be processed independently.  imp 0.85 → +Stream complete entities or prediction batches  [first in 7/7 visits that checked it]
more:         11 further checks (E178, E175, E349, E177, E350, E347, E345, E348, E344, E351, E346), load on request
enough when:  top option >= 37% (lower quartile over 65 visits) or >= 19 points ahead; median 3 checks
come back:    after 'after a new best' (4/7); after 'other' (2/7); after 'regression after a single change' (1/7)  [7 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 85% of visits
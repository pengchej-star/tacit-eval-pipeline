# [Change execution to enable useful experiments › Which execution change removes the observed bottleneck?]   305 visits, 44 experts

options: Use a representative smoke run (29) | Cache reusable computations (17) | Bound memory with chunks and sequential loads (24) | Tune inference batching and precision (12) | Centralize reproducible configuration (22) | Refactor with output equivalence (30) | Accelerate repeated metric evaluation (1) | Use a compatible signal backend (1) | Eliminate repeated conversions (1)

check first: E117 Frequent variant edits cause stale paths, mismatched parameters, or accidental component omissions.  imp 0.68 → +Centralize reproducible configuration  [first in 94/153 visits that checked it]
then:        E113 Full runs are slow and new code frequently fails before producing predictions.  imp 0.72 → +Use a representative smoke run  [first in 86/107 visits that checked it]
then:        E115 Peak memory grows with full datasets or simultaneously retained models.  imp 0.70 → +Bound memory with chunks and sequential loads  [first in 39/53 visits that checked it]
more:         6 further checks (E114, E118, E116, E120, E121, E119), load on request
enough when:  top option >= 25% (lower quartile over 302 visits) or >= 10 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (11/39); after 'other' (10/39); after 'after a new best' (10/39)  [39 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 78% of visits
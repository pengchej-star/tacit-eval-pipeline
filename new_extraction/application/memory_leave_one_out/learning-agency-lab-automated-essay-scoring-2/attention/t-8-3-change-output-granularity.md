# [Change output granularity › What should be done about discreteness or ties in the predictions?]   36 visits, 5 experts

options: Map predictions to label levels (13) | Fall back for collapsed columns (2) | Test tie handling explicitly (2)

check first: E189 Targets occupy a small set of repeated levels while model outputs are fully continuous.  imp 0.85 → +Map predictions to label levels  [first in 33/36 visits that checked it]
then:        E190 Existing binning collapses one or more prediction columns to a constant.  imp 0.80 → +Fall back for collapsed columns  [first in 2/12 visits that checked it]
then:        E358 The implementation contains a bug where edge cases (e.g., empty arrays, off-by-one errors) cause incorrect or degenerate overwrites.  imp 0.60 → +Fall back for collapsed columns  [first in 1/17 visits that checked it]
more:         6 further checks (E355, E356, E357, E191, E360, E359), load on request
enough when:  top option >= 67% (lower quartile over 36 visits) or >= 46 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (1/2); after 'after a new best' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 81% of visits
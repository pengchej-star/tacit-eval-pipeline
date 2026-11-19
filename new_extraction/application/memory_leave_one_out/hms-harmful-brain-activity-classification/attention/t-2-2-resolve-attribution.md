# [Resolve attribution › How should I disentangle the recent score change?]   237 visits, 38 experts

options: Change or ablate one factor (63) | Restore the last verified configuration (36) | Test a small interaction grid (8)

check first: E11 Several independently adjustable factors changed together.  imp 0.45 → -Change or ablate one factor  [first in 224/236 visits that checked it]
then:        E12 A recent modification caused a substantial regression relative to a reproducible saved baseline.  imp 0.75 → +Restore the last verified configuration  [first in 13/188 visits that checked it]
then:        E13 The preferred setting has reversed when another tightly coupled setting changed.  imp 0.70 → +Test a small interaction grid  [first in 0/44 visits that checked it]
enough when:  top option >= 46% (lower quartile over 237 visits) or >= 3 points ahead; median 2 checks
come back:    after 'other' (6/17); after '4+ scored steps without a new best' (3/17); after 'regression after a single change' (2/17)  [17 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 34% of visits
# [Resolve the first execution failure › What dependency failure prevents the intended computation?]   141 visits, 40 experts

options: Resolve artifact paths (12) | Resolve package compatibility (6) | Match computation devices (6) | Repair syntax or API contracts (28) | Write the intended submission (5)

check first: E43 The first failure names an undefined variable, invalid keyword, type, or method.  imp 0.95 → +Repair syntax or API contracts  [first in 77/117 visits that checked it]
then:        E40 The error is a missing file or a read-only source path.  imp 0.95 → +Resolve artifact paths  [first in 25/108 visits that checked it]
then:        E41 The failure is an import, missing symbol, or incompatible package version.  imp 0.90 → +Resolve package compatibility  [first in 23/115 visits that checked it]
more:         2 further checks (E42, E44), load on request
enough when:  top option >= 56% (lower quartile over 140 visits) or >= 35 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (3/7); after '3 scored steps without a new best' (2/7); after '2 scored steps without a new best' (1/7)  [7 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 87% of visits
# [Reduce peak memory › What dominates peak memory in the failing stage?]   63 visits, 19 experts

options: Process rows in chunks (6) | Release completed stages (17) | Reduce batch or precision footprint (13)

check first: E93 Memory accumulates across finished models or framework stages.  imp 0.75 → +Release completed stages  [first in 28/38 visits that checked it]
then:        E94 A single forward batch exceeds memory or padding wastes most tokens.  imp 0.88 → +Reduce batch or precision footprint  [first in 19/37 visits that checked it]
then:        E92 The complete dataset or feature matrix dominates memory, but independent row groups can be processed separately.  imp 0.92 → +Process rows in chunks  [first in 9/16 visits that checked it]
more:         3 further checks (E194, E196, E195), load on request
enough when:  top option >= 63% (lower quartile over 62 visits) or >= 40 points ahead; median 2 checks
come back:    after 'other' (1/2); after 'after a new best' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 84% of visits
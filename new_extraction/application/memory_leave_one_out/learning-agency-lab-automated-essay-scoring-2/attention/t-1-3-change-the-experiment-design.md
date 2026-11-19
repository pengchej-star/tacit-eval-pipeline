# [Change the experiment design › What experiment should be run next given the evidence already available?]   534 visits, 50 experts

options: Establish an end-to-end baseline (4) | Test one controlled change (71) | Measure repeated-run variation (49) | Bracket a bounded search (2) | Recover the last validated configuration (32) | Stop an exhausted local search (30) | Replace a clearly inadequate baseline (1)

check first: E21 No complete pipeline has yet produced a scored prediction file.  imp 0.95 → +Establish an end-to-end baseline  [first in 178/532 visits that checked it]
then:        E22 The last score change followed several simultaneous functional edits.  imp 0.75 → +Test one controlled change  [first in 174/511 visits that checked it]
then:        E23 Existing unchanged runs vary by as much as the candidate gain.  imp 0.85 → +Measure repeated-run variation  [first in 125/225 visits that checked it]
more:         4 further checks (E26, E25, E24, E27), load on request
enough when:  top option >= 43% (lower quartile over 534 visits) or >= 9 points ahead; median 4 checks
come back:    after 'regression after a single change' (11/27); after 'after a new best' (7/27); after 'other' (5/27)  [27 returns, 10 improved the score]

scores: LLM-guessed; top option matches the option taken in 63% of visits
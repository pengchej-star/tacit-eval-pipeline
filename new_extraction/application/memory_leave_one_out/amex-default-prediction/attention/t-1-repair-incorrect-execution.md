# [Repair incorrect execution › Which failure should be repaired before interpreting model scores?]   427 visits, 51 experts

options: Repair model compatibility (102) | Repair prediction computation (38) | Repair failed execution (57)

check first: E09 A checkpoint or feature-pipeline change preceded the first large regression.  imp 0.72 → +Repair model compatibility  [first in 251/268 visits that checked it]
then:        E11 The run errors or fails to create a valid complete output file.  imp 0.85 → +Repair failed execution  [first in 108/340 visits that checked it]
then:        E10 All components run, but combining their outputs causes the regression.  imp 0.55 → +Repair prediction computation  [first in 33/131 visits that checked it]
more:         14 further checks (E12, E208, E203, E210, E213, E204, E214, E211, E209, E215, E205, E206, E207, E212), load on request
enough when:  top option >= 65% (lower quartile over 419 visits) or >= 39 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (13/32); after 'other' (6/32); after '3 scored steps without a new best' (5/32)  [32 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 73% of visits
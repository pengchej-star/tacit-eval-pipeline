# [Choose a feature retention policy › How should the candidate feature set be reduced or retained?]   118 visits, 12 experts

options: Tune ranked retention (26) | Remove or restore feature groups (17) | Regenerate compatible feature selection (7)

check first: E54 A ranked feature list exists but its cutoff has not been validated for the current pipeline.  imp 0.72 → +Tune ranked retention  [first in 54/59 visits that checked it]
then:        E55 A named feature group is redundant, noisy, or was removed before a regression.  imp 0.65 → +Remove or restore feature groups  [first in 34/42 visits that checked it]
then:        E56 A cached selection list predates new features or refers to absent columns.  imp 0.68 → +Regenerate compatible feature selection  [first in 16/36 visits that checked it]
more:         19 further checks (E146, E152, E154, E153, E162, E149, E150, E148, E160, E161, E155, E159, E147, E157, E151, E156, E163, E158, E57), load on request
enough when:  top option >= 60% (lower quartile over 118 visits) or >= 32 points ahead; median 8 checks
come back:    after '2 scored steps without a new best' (3/8); after '4+ scored steps without a new best' (2/8); after 'other' (1/8)  [8 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 77% of visits
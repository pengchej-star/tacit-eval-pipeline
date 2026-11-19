# [Change prediction combination › Which limitation in the current ensemble should be addressed next?]   1004 visits, 52 experts

options: Change the active member set (164) | Choose a source of diversity (125) | Change blend weights (103) | Change the combination domain (27) | Change the stacking stage (35)

check first: E145 The value of specific active or candidate members is uncertain.  imp 0.72 → +Change the active member set  [first in 475/582 visits that checked it]
then:        E146 Current members have highly correlated errors and additional independent prediction sources are available.  imp 0.78 → +Choose a source of diversity  [first in 159/332 visits that checked it]
then:        E147 Membership is stable but existing weights ignore quality differences or group sizes.  imp 0.75 → +Change blend weights  [first in 155/312 visits that checked it]
more:         16 further checks (E148, E302, E149, E303, E305, E304, E307, E306, E315, E309, E310, E314, E312, E311, E313, E308), load on request
enough when:  top option >= 42% (lower quartile over 1004 visits) or >= 18 points ahead; median 7 checks
come back:    after 'after a new best' (10/28); after 'other' (9/28); after 'regression after a single change' (5/28)  [28 returns, 7 improved the score]

scores: LLM-guessed; top option matches the option taken in 64% of visits
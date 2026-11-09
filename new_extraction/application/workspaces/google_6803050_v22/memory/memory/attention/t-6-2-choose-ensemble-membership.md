# [Choose ensemble membership › Which membership experiment should I run next?]   400 visits, 37 experts

options: Measure a candidate in isolation (55) | Test one additional member (29) | Remove a harmful or redundant member (47) | Replace one fixed ensemble slot (21) | Restore complementary members (17) | Retest membership after upstream changes (5)

check first: E120 The candidate has not yet produced verified standalone predictions.  imp 0.92 → +Measure a candidate in isolation  [first in 184/275 visits that checked it]
then:        E122 A member is weak, redundant, or associated with a regression.  imp 0.75 → +Remove a harmful or redundant member  [first in 139/243 visits that checked it]
then:        E124 Removing formerly useful members caused a reproducible regression.  imp 0.80 → +Restore complementary members  [first in 28/152 visits that checked it]
more:         3 further checks (E121, E125, E123), load on request
enough when:  top option >= 34% (lower quartile over 400 visits) or >= 9 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (11/33); after 'regression after a single change' (8/33); after 'after a new best' (8/33)  [33 returns, 12 improved the score]

scores: LLM-guessed; top option matches the option taken in 43% of visits
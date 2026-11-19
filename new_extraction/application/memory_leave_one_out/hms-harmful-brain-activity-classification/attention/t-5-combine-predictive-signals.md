# [Combine predictive signals › Which combination change should I evaluate?]   700 visits, 51 experts

options: Choose ensemble membership (151) | Reduce prediction variance (55) | Choose aggregation (131)

check first: E91 The current set may omit complementary signal or include harmful members.  imp 0.45 → +Choose ensemble membership  [first in 310/318 visits that checked it]
then:        E93 Valid model outputs differ in quality, scale or complementary error.  imp 0.30 → +Choose aggregation  [first in 190/300 visits that checked it]
then:        E92 A single predictor is unstable and repeatable alternatives are available.  imp 0.55 → +Reduce prediction variance  [first in 80/126 visits that checked it]
more:         8 further checks (E159, E160, E162, E161, E164, E166, E163, E165), load on request
enough when:  top option >= 50% (lower quartile over 700 visits) or >= 18 points ahead; median 4 checks
come back:    after 'other' (5/18); after 'regression after a single change' (4/18); after 'after a new best' (4/18)  [18 returns, 7 improved the score]

scores: LLM-guessed; top option matches the option taken in 66% of visits
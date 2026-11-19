# [Select or refresh features › What kind of feature reduction or refresh is justified?]   110 visits, 13 experts

options: Tune the retained feature count (22) | Ablate suspect feature groups (17) | Compare feature-ranking methods (2) | Regenerate selection artifacts after input changes (6)

check first: E40 Many low-ranked features remain and their contribution is uncertain.  imp 0.85 → +Tune the retained feature count  [first in 63/63 visits that checked it]
then:        E41 A specific feature family is redundant, noisy or previously harmful.  imp 0.75 → +Ablate suspect feature groups  [first in 34/37 visits that checked it]
then:        E43 A saved feature list was built for a different feature schema.  imp 0.80 → +Regenerate selection artifacts after input changes  [first in 11/32 visits that checked it]
more:         1 further checks (E42), load on request
enough when:  top option >= 53% (lower quartile over 110 visits) or >= 35 points ahead; median 1 checks
come back:    after 'after a new best' (2/9); after 'regression after a bundled change' (2/9); after 'other' (1/9)  [9 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 86% of visits
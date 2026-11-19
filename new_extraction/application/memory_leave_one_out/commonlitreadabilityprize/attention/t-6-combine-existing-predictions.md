# [Combine existing predictions › Which ensemble intervention addresses the observed limitation?]   769 visits, 49 experts

options: Choose prediction-pool changes (195) | Choose the combination-rule change (105) | Choose test-time views (24)

check first: E107 The pool lacks independent predictions or includes demonstrably harmful members.  imp 0.85 → +Choose prediction-pool changes  [first in 367/378 visits that checked it]
then:        E108 The member pool is stable but output conventions or coefficient choices have not been validated.  imp 0.75 → +Choose the combination-rule change  [first in 227/350 visits that checked it]
then:        E208 A code bug (e.g., shape mismatch, wrong variable, broken loop, path error) prevents the ensemble pipeline from executing correctly or producing valid blended predictions.  imp 0.50 → +Choose prediction-pool changes  [first in 92/536 visits that checked it]
more:         11 further checks (E109, E209, E110, E212, E213, E216, E211, E210, E214, E217, E215), load on request
enough when:  top option >= 55% (lower quartile over 768 visits) or >= 24 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (5/15); after '2 scored steps without a new best' (4/15); after 'regression after a single change' (2/15)  [15 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 82% of visits
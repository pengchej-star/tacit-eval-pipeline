# [Change target construction › Should target construction be global or conditioned on evaluation groups?]   11 visits, 5 experts

options: Transform the censored outcome (5) | Construct targets within evaluation groups (2)

check first: E109 The outcome is censored and ordinary regression targets do not express the observed event information.  imp 0.75 → +Transform the censored outcome  [first in 7/11 visits that checked it]
then:        E110 The metric scores predefined groups and their outcome distributions differ substantially.  imp 0.65 → +Construct targets within evaluation groups  [first in 4/11 visits that checked it]
then:        E285 The group-conditioning implementation correctly identifies and matches group labels in the data (e.g., no mismatch between string labels and encoded values).  imp 0.70 → +Construct targets within evaluation groups  [first in 0/4 visits that checked it]
more:         1 further checks (E111), load on request
enough when:  top option >= 50% (lower quartile over 11 visits) or >= 0 points ahead; median 2 checks
come back:    after 'other' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 36% of visits
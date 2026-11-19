# [Summarize repeated observations › Which information is missing from the current entity representation?]   77 visits, 6 experts

options: Aggregate entity histories (10) | Encode temporal changes (6) | Encode domain interactions (3) | Change numeric or categorical preprocessing (6)

check first: E29 Each prediction entity has multiple records but the model sees only one record or a few summaries.  imp 0.85 → +Aggregate entity histories  [first in 48/56 visits that checked it]
then:        E32 Missingness, category handling, quantization, or scaling differs between model families.  imp 0.50 → +Change numeric or categorical preprocessing  [first in 12/13 visits that checked it]
then:        E31 Related measurements have meaningful contrasts not encoded in the current features.  imp 0.65 → +Encode domain interactions  [first in 11/16 visits that checked it]
more:         8 further checks (E30, E159, E156, E160, E154, E157, E155, E158), load on request
enough when:  top option >= 45% (lower quartile over 77 visits) or >= 10 points ahead; median 3 checks
come back:    after '2 scored steps without a new best' (1/2); after 'other' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 55% of visits
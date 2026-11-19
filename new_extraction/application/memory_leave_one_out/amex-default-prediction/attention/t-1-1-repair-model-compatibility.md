# [Repair model compatibility › Which model contract is inconsistent with the saved training configuration?]   226 visits, 36 experts

options: Match architecture and weights (34) | Restore training preprocessing (27) | Align rows and feature columns (12) | Repair a stage handoff (29)

check first: E16 A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.  imp 0.65 → +Repair a stage handoff  [first in 88/171 visits that checked it]
then:        E14 The same raw example produces different training and inference features.  imp 0.75 → +Restore training preprocessing  [first in 55/74 visits that checked it]
then:        E13 Strict loading reports missing keys or incompatible tensor dimensions.  imp 0.88 → +Match architecture and weights  [first in 42/63 visits that checked it]
more:         1 further checks (E15), load on request
enough when:  top option >= 44% (lower quartile over 223 visits) or >= 20 points ahead; median 1 checks
come back:    after '4+ scored steps without a new best' (6/15); after 'regression after a single change' (3/15); after 'other' (3/15)  [15 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 78% of visits
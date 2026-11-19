# [Choose the validation design › Which validation split best approximates the prediction setting?]   56 visits, 10 experts

options: Keep related samples together (5) | Balance targets across folds (4) | Validate on the target population (6) | Adjust validation coverage (6)

check first: E32 An identifiable training subgroup differs from the expected test population.  imp 0.80 → +Validate on the target population  [first in 21/40 visits that checked it]
then:        E30 Samples share entities, topics, overlapping windows, or other dependence groups.  imp 0.95 → +Keep related samples together  [first in 14/36 visits that checked it]
then:        E33 Current folds leave too little fitting data or unstable validation and out-of-fold coverage.  imp 0.60 → +Adjust validation coverage  [first in 5/16 visits that checked it]
more:         13 further checks (E31, E138, E135, E136, E139, E145, E142, E140, E144, E141, E137, E34, E143), load on request
enough when:  top option >= 52% (lower quartile over 56 visits) or >= 28 points ahead; median 5 checks
come back:    after 'other' (1/3); after '4+ scored steps without a new best' (1/3); after 'regression after a single change' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 82% of visits
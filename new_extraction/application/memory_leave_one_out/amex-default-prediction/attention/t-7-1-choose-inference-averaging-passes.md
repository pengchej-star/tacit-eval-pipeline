# [Choose inference averaging passes › Which extra inference passes are justified?]   54 visits, 9 experts

options: Average valid transformed views (24) | Choose deterministic or dropout inference (6)

check first: E173 There are known label-preserving flips, sensor permutations, crops, or views.  imp 0.95 → +Average valid transformed views  [first in 41/44 visits that checked it]
then:        E174 Dropout is intentionally active and repeated passes produce different outputs.  imp 0.92 → +Choose deterministic or dropout inference  [first in 6/11 visits that checked it]
then:        E412 TTA effect is inconsistent across checkpoint versions or ensemble compositions, so its benefit must be re-validated when the model changes.  imp 0.40 → -Average valid transformed views  [first in 2/26 visits that checked it]
more:         19 further checks (E411, E405, E413, E175, E422, E418, E176, E410, E416, E420, E417, E406, E409, E419, E414, E415, E421, E408, E407), load on request
enough when:  top option >= 88% (lower quartile over 54 visits) or >= 75 points ahead; median 7 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 93% of visits
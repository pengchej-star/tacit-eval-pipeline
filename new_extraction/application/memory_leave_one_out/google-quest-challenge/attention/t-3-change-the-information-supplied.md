# [Change the information supplied › Which input-side change addresses the missing or misleading signal?]   650 visits, 40 experts

options: Choose the training examples (34) | Choose a new feature representation (88) | Choose a feature retention policy (50) | Choose the input transformation (82)

check first: E38 Current transformations may discard useful information or differ from checkpoint training.  imp 0.65 → +Choose the input transformation  [first in 182/238 visits that checked it]
then:        E36 The current feature set omits identifiable temporal, semantic, or domain information.  imp 0.85 → +Choose a new feature representation  [first in 168/188 visits that checked it]
then:        E37 New features increased dimensionality or earlier ablations suggest some features hurt.  imp 0.75 → +Choose a feature retention policy  [first in 167/265 visits that checked it]
more:         1 further checks (E35), load on request
enough when:  top option >= 49% (lower quartile over 614 visits) or >= 28 points ahead; median 1 checks
come back:    after 'after a new best' (9/16); after 'other' (4/16); after '4+ scored steps without a new best' (2/16)  [16 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 72% of visits
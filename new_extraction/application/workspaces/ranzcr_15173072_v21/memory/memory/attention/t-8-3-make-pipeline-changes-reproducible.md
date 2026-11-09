# [Make pipeline changes reproducible › Which code-organization change addresses the observed fragility?]   136 visits, 29 experts

options: Parameterize and separate model pipelines (23) | Verify a cleanup or inference-only refactor (25) | Pin configurations and artifacts (10) | Make missing-component behavior explicit (3)

check first: E183 Adding model variants repeatedly requires editing duplicated code and shared globals.  imp 0.65 → +Parameterize and separate model pipelines  [first in 51/75 visits that checked it]
then:        E184 Dead code or training-only paths obscure a stable inference pipeline.  imp 0.60 → +Verify a cleanup or inference-only refactor  [first in 34/67 visits that checked it]
then:        E185 Identical code can load different artifacts or settings across runs.  imp 0.80 → +Pin configurations and artifacts  [first in 31/70 visits that checked it]
more:         7 further checks (E363, E367, E186, E366, E364, E365, E368), load on request
enough when:  top option >= 48% (lower quartile over 136 visits) or >= 18 points ahead; median 4 checks
come back:    after 'other' (2/7); after '4+ scored steps without a new best' (2/7); after 'regression after a single change' (1/7)  [7 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 55% of visits
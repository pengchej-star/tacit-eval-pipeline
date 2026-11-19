# [Change structured output corrections › Which structured correction, if any, has supporting evidence?]   27 visits, 8 experts

options: Use a validated auxiliary prediction (7) | Apply a high-precision metadata rule (4) | Remove or restore an output correction (3)

check first: E192 An auxiliary classifier or head gives held-out information not captured by the main prediction.  imp 0.85 → +Use a validated auxiliary prediction  [first in 14/15 visits that checked it]
then:        E194 The current post-processing was tuned for older checkpoints or its contribution is unverified.  imp 0.65 → +Remove or restore an output correction  [first in 6/20 visits that checked it]
then:        E193 A prediction-time metadata condition almost determines a particular target in training and held-out examples.  imp 0.90 → +Apply a high-precision metadata rule  [first in 6/8 visits that checked it]
more:         1 further checks (E361), load on request
enough when:  top option >= 61% (lower quartile over 27 visits) or >= 35 points ahead; median 2 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 100% of visits
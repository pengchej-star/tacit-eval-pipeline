# [Correct output semantics or bias › Which output correction should I test or repair?]   80 visits, 23 experts

options: Restore prediction units and activation (10) | Align risk-score direction (4) | Rescale probabilities or logits (5) | Correct systematic prediction bias (5) | Apply auxiliary or metadata corrections (12) | Ablate an existing output transform (7)

check first: E163 A previously helpful post-processing step has not been reassessed after upstream changes.  imp 0.65 → +Ablate an existing output transform  [first in 19/47 visits that checked it]
then:        E162 A high-precision auxiliary classifier or metadata rule identifies a predictable error subset.  imp 0.88 → +Apply auxiliary or metadata corrections  [first in 17/21 visits that checked it]
then:        E158 Outputs have the wrong units, activation, range, or probability sum.  imp 0.95 → +Restore prediction units and activation  [first in 16/23 visits that checked it]
more:         11 further checks (E159, E161, E322, E160, E164, E324, E323, E320, E319, E321, E318), load on request
enough when:  top option >= 37% (lower quartile over 79 visits) or >= 11 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (2/5); after 'regression after a single change' (1/5); after 'other' (1/5)  [5 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 56% of visits
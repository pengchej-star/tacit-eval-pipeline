# [Repair artifact loading › What prevents the intended checkpoint from being loaded correctly?]   65 visits, 22 experts

options: Verify artifact paths and lifetime (9) | Resolve dependency and import conflicts (6) | Match architecture to the checkpoint (12) | Verify loaded weights are effective (5)

check first: E32 A configured artifact is missing or its resolved path differs from the saved artifact.  imp 0.70 → +Verify artifact paths and lifetime  [first in 22/29 visits that checked it]
then:        E34 Checkpoint keys, tensor shapes, tokenizer vocabulary, or head dimensions disagree with the constructed model.  imp 0.85 → +Match architecture to the checkpoint  [first in 20/26 visits that checked it]
then:        E33 Imports fail or resolve to a different library copy than the checkpoint requires.  imp 0.75 → +Resolve dependency and import conflicts  [first in 15/19 visits that checked it]
more:         5 further checks (E35, E211, E209, E208, E210), load on request
enough when:  top option >= 46% (lower quartile over 65 visits) or >= 18 points ahead; median 2 checks
come back:    after 'other' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 83% of visits
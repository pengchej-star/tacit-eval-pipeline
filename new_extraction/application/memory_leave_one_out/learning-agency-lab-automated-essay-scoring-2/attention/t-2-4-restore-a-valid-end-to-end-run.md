# [Restore a valid end-to-end run › What is preventing a valid full prediction run?]   153 visits, 34 experts

options: Debug a minimal end-to-end run (26) | Validate prediction export (4) | Make missing-member handling explicit (3) | Rebuild a tangled pipeline (27)

check first: E49 Repeated patches leave duplicated transformations or hidden dependencies that prevent reliable fixes.  imp 0.78 → +Rebuild a tangled pipeline  [first in 56/127 visits that checked it]
then:        E46 The pipeline fails before completing even one sample or model.  imp 0.92 → +Debug a minimal end-to-end run  [first in 52/85 visits that checked it]
then:        E47 Inference finishes but the expected prediction file is absent or malformed.  imp 0.82 → +Validate prediction export  [first in 12/36 visits that checked it]
more:         6 further checks (E48, E229, E226, E225, E227, E228), load on request
enough when:  top option >= 52% (lower quartile over 153 visits) or >= 22 points ahead; median 3 checks
come back:    after 'after a new best' (3/10); after 'other' (3/10); after '4+ scored steps without a new best' (2/10)  [10 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 65% of visits
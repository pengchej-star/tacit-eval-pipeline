# [Reduce peak resource use › Which resource reduction preserves the intended prediction pipeline?]   41 visits, 15 experts

options: Release stage-local memory (15) | Fit the batch to memory (8) | Compare reduced precision (3)

check first: E194 Memory remains allocated after one model finishes and grows across stages.  imp 0.85 → +Release stage-local memory  [first in 21/23 visits that checked it]
then:        E195 The first forward pass fails at the current batch size.  imp 0.80 → +Fit the batch to memory  [first in 8/15 visits that checked it]
then:        E438 The object being deleted is still referenced downstream in the pipeline, causing a runtime error.  imp 0.55 → -Release stage-local memory  [first in 4/18 visits that checked it]
more:         10 further checks (E196, E442, E437, E440, E443, E197, E445, E441, E444, E439), load on request
enough when:  top option >= 58% (lower quartile over 41 visits) or >= 33 points ahead; median 3 checks
come back:    after 'regression after a single change' (1/2); after 'after a new best' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 80% of visits
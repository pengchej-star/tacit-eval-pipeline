# [Change the feature source › Which feature representation should replace or extend the current one?]   158 visits, 13 experts

options: Tune sparse or topic representations (5) | Add fixed semantic embeddings (8) | Test an engineered feature group (23) | Add structured metadata features (3) | Select a compact feature set (30)

check first: E82 Recent feature additions increased dimension without a reliable validation gain.  imp 0.60 → +Select a compact feature set  [first in 74/148 visits that checked it]
then:        E80 A domain interaction or structural statistic is plausible and not explicitly represented.  imp 0.80 → +Test an engineered feature group  [first in 36/47 visits that checked it]
then:        E79 The current representation lacks semantic information available from a compatible pretrained encoder.  imp 0.75 → +Add fixed semantic embeddings  [first in 16/29 visits that checked it]
more:         3 further checks (E83, E78, E81), load on request
enough when:  top option >= 38% (lower quartile over 157 visits) or >= 16 points ahead; median 2 checks
come back:    after 'after a new best' (1/2); after '4+ scored steps without a new best' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 73% of visits
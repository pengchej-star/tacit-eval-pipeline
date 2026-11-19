# [Change representation aggregation inside the model › Which architectural aggregation should replace the current head?]   33 visits, 10 experts

options: Change pooling or normalization (8) | Add auxiliary supervision (3) | Change branch fusion (4) | Add a learned temporal or attention head (1) | Resize the neural feature extractor (2)

check first: E95 Multiple input branches are reduced by a fixed combination that may discard information.  imp 0.70 → +Change branch fusion  [first in 8/8 visits that checked it]
then:        E93 The current head discards useful token, layer, or channel information.  imp 0.75 → +Change pooling or normalization  [first in 7/7 visits that checked it]
then:        E262 A previous change to the aggregation head degraded performance, indicating the current head design is suboptimal.  imp 0.55 → +Change pooling or normalization  [first in 3/18 visits that checked it]
more:         10 further checks (E263, E267, E94, E97, E96, E264, E268, E266, E265, E269), load on request
enough when:  top option >= 44% (lower quartile over 32 visits) or >= 29 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (1/2); after 'after a new best' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 97% of visits
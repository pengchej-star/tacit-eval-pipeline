# [Change input preprocessing › Which aspect of the model input is mismatched or missing useful detail?]   232 visits, 19 experts

options: Match and ablate text cleaning (12) | Change image input resolution (10) | Match or ablate input normalization (9) | Tune the time-frequency representation (13) | Tune raw-signal filtering and clipping (6) | Change the signal context window (8) | Change the input channels or modalities (29)

check first: E50 An available channel or modality captures structure not present in the active input.  imp 0.82 → +Change the input channels or modalities  [first in 74/100 visits that checked it]
then:        E46 Input scale, channel order or reshape differs from the checkpoint training pipeline.  imp 0.75 → +Match or ablate input normalization  [first in 34/60 visits that checked it]
then:        E47 The current time-frequency transform blurs transient events or narrow spectral patterns.  imp 0.80 → +Tune the time-frequency representation  [first in 30/57 visits that checked it]
more:         5 further checks (E44, E45, E49, E51, E48), load on request
enough when:  top option >= 35% (lower quartile over 230 visits) or >= 12 points ahead; median 2 checks
come back:    after 'after a new best' (4/9); after 'regression after a single change' (3/9); after 'other' (2/9)  [9 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 85% of visits
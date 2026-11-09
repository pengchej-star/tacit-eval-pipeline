# [Represent images and signals › Which spatial or signal representation should I test?]   109 visits, 13 experts

options: Sweep input resolution (13) | Change time-frequency resolution (8) | Change the observed window (8) | Change signal filtering or clipping (7) | Change input normalization (7) | Change channel layout or rendering (7)

check first: E61 Resizing removes label-relevant detail and compatible resolution checkpoints exist.  imp 0.92 → +Sweep input resolution  [first in 25/29 visits that checked it]
then:        E62 Time-frequency detail is unresolved at the current transform settings.  imp 0.88 → +Change time-frequency resolution  [first in 24/32 visits that checked it]
then:        E63 The current crop misses the labeled interval or includes mostly irrelevant context.  imp 0.82 → +Change the observed window  [first in 22/33 visits that checked it]
more:         3 further checks (E65, E64, E66), load on request
enough when:  top option >= 44% (lower quartile over 109 visits) or >= 21 points ahead; median 1 checks
come back:    after 'other' (2/8); after 'after a new best' (2/8); after '4+ scored steps without a new best' (2/8)  [8 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 90% of visits
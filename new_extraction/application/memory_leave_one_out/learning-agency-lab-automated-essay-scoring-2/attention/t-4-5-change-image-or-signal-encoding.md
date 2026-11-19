# [Change image or signal encoding › Which aspect of the image or signal representation should be changed?]   95 visits, 11 experts

options: Sweep input spatial resolution (12) | Change the retained context window (7) | Change time-frequency resolution (9) | Match input normalization (7) | Change signal filtering (4) | Tune signal dynamic-range clipping (2) | Test scalar-to-color encoding (1) | Change signal-to-image layout (2)

check first: E91 Time-frequency bins are too coarse for the event durations or frequency structure of interest.  imp 0.90 → +Change time-frequency resolution  [first in 24/26 visits that checked it]
then:        E89 Useful fine detail is lost at the current resize and compatible higher-resolution weights exist.  imp 0.95 → +Sweep input spatial resolution  [first in 16/26 visits that checked it]
then:        E90 The current temporal or spatial window misses the labeled region or includes irrelevant context.  imp 0.70 → +Change the retained context window  [first in 15/17 visits that checked it]
more:         9 further checks (E92, E270, E93, E96, E94, E95, E272, E271, E273), load on request
enough when:  top option >= 31% (lower quartile over 95 visits) or >= 17 points ahead; median 3 checks
come back:    after 'after a new best' (3/10); after 'regression after a single change' (3/10); after '4+ scored steps without a new best' (2/10)  [10 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 98% of visits
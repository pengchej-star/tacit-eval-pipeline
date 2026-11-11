# [Change the fitted learner › Which model-level replacement should be tested?]   225 visits, 30 experts

options: Replace the model family or implementation (39) | Change representation aggregation inside the model (18) | Select a compatible saved checkpoint (38)

check first: E100 Several compatible trained states are already available and differ in validation quality.  imp 0.65 → +Select a compatible saved checkpoint  [first in 104/172 visits that checked it]
then:        E98 The current model family or pretrained capacity has plateaued despite a stable implementation.  imp 0.72 → +Replace the model family or implementation  [first in 87/89 visits that checked it]
then:        E99 Useful model representations are being discarded or combined by an inadequate head.  imp 0.78 → +Change representation aggregation inside the model  [first in 22/34 visits that checked it]
more:         15 further checks (E224, E221, E234, E223, E233, E230, E225, E227, E232, E226, E231, E229, E228, E235, E222), load on request
enough when:  top option >= 60% (lower quartile over 224 visits) or >= 34 points ahead; median 8 checks
come back:    after '2 scored steps without a new best' (3/10); after '4+ scored steps without a new best' (3/10); after 'after a new best' (3/10)  [10 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 79% of visits
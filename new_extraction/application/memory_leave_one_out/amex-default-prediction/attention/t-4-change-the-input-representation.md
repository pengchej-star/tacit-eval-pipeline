# [Change the input representation › Which representation change should be tested next?]   308 visits, 32 experts

options: Change basic feature encoding (9) | Change what the text encoder sees (15) | Change the feature source (69) | Choose a signal front end (25) | Change retained input extent (20)

check first: E66 Useful feature sources are absent or an expanded feature set has become noisy.  imp 0.50 → +Change the feature source  [first in 157/165 visits that checked it]
then:        E67 Raw signals can support an untested domain-valid filter or representation.  imp 0.90 → +Choose a signal front end  [first in 47/50 visits that checked it]
then:        E68 The current resize, crop, or time window discards relevant information.  imp 0.75 → +Change retained input extent  [first in 44/65 visits that checked it]
more:         5 further checks (E65, E284, E64, E285, E286), load on request
enough when:  top option >= 34% (lower quartile over 303 visits) or >= 4 points ahead; median 2 checks
come back:    after 'after a new best' (3/8); after '4+ scored steps without a new best' (2/8); after 'regression after a single change' (2/8)  [8 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 85% of visits
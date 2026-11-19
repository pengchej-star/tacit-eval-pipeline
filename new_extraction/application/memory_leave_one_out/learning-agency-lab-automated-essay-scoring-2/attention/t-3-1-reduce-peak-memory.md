# [Reduce peak memory › What accounts for the memory peak?]   40 visits, 15 experts

options: Process data in bounded chunks (6) | Release completed models and intermediates (11) | Reduce inference batch size (6) | Compare reduced and full precision (2)

check first: E54 Memory grows between sequential model runs because completed objects remain live.  imp 0.85 → +Release completed models and intermediates  [first in 14/22 visits that checked it]
then:        E53 The raw table or engineered feature table exceeds memory before model inference starts.  imp 0.90 → +Process data in bounded chunks  [first in 12/20 visits that checked it]
then:        E55 Memory failure occurs in a single forward pass and grows with batch size.  imp 0.80 → +Reduce inference batch size  [first in 9/23 visits that checked it]
more:         4 further checks (E56, E234, E232, E233), load on request
enough when:  top option >= 59% (lower quartile over 39 visits) or >= 36 points ahead; median 2 checks
come back:    after 'other' (1/3); after 'regression after a single change' (1/3); after 'after a new best' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 90% of visits
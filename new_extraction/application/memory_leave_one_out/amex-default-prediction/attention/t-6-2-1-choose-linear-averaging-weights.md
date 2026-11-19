# [Choose linear averaging weights › Which coefficient rule is supported by current validation evidence?]   238 visits, 33 experts

options: Use a uniform average (11) | Tune global blend weights (82) | Allow subtractive coefficients (2)

check first: E160 Members differ consistently in quality and aligned held-out predictions are available.  imp 0.85 → +Tune global blend weights  [first in 107/160 visits that checked it]
then:        E159 Members have comparable held-out quality and weight tweaks have not generalized.  imp 0.72 → +Use a uniform average  [first in 99/127 visits that checked it]
then:        E162 The dataset is small and fitted coefficients vary sharply across folds.  imp 0.70 → +Use a uniform average  [first in 15/76 visits that checked it]
more:         1 further checks (E161), load on request
enough when:  top option >= 67% (lower quartile over 223 visits) or >= 45 points ahead; median 1 checks
come back:    after '2 scored steps without a new best' (3/6); after '4+ scored steps without a new best' (2/6); after 'other' (1/6)  [6 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 73% of visits
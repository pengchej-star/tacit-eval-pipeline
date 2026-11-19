# [Choose a signal front end › Which signal transformation is most justified for the next experiment?]   58 visits, 5 experts

options: Tune the time-frequency representation (12) | Change signal filtering (3) | Clip signal outliers (1) | Change derived input channels (5) | Change spectral image rendering (2) | Change the signal-to-image layout (2)

check first: E84 The current time-frequency representation obscures short events or narrow frequency structure.  imp 0.85 → +Tune the time-frequency representation  [first in 13/16 visits that checked it]
then:        E87 Available sensors or meaningful channel differences are absent from the current input.  imp 0.60 → +Change derived input channels  [first in 11/11 visits that checked it]
then:        E296 The proposed front-end change was previously bundled with other modifications and has never been ablated in isolation.  imp 0.50 → -Tune the time-frequency representation  [first in 9/46 visits that checked it]
more:         12 further checks (E298, E88, E89, E297, E299, E86, E90, E85, E301, E300, E295, E294), load on request
enough when:  top option >= 34% (lower quartile over 58 visits) or >= 10 points ahead; median 4 checks
come back:    after 'after a new best' (3/6); after 'regression after a single change' (3/6)  [6 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 90% of visits
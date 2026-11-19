# [Change inference or final output mapping › Which inference-only intervention fits the metric and observed errors?]   181 visits, 29 experts

options: Choose inference averaging passes (30) | Choose an ordinal mapping (39) | Choose a probability calibration change (8) | Choose a targeted score correction (18) | Ablate existing post-processing (3)

check first: E169 The target is discrete or the metric treats ties and ordinal errors specially.  imp 0.80 → +Choose an ordinal mapping  [first in 95/148 visits that checked it]
then:        E168 Valid alternate input views or stochastic model outputs are available.  imp 0.72 → +Choose inference averaging passes  [first in 56/58 visits that checked it]
then:        E171 Residual bias is localized to a reliable reference, auxiliary signal, or metadata rule.  imp 0.82 → +Choose a targeted score correction  [first in 12/28 visits that checked it]
more:         10 further checks (E170, E172, E399, E404, E402, E400, E401, E398, E403, E397), load on request
enough when:  top option >= 42% (lower quartile over 181 visits) or >= 9 points ahead; median 3 checks
come back:    after 'after a new best' (3/6); after 'regression after a single change' (1/6); after '2 scored steps without a new best' (1/6)  [6 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 83% of visits
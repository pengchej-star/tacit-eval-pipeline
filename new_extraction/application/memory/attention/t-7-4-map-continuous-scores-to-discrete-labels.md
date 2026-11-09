# [Map continuous scores to discrete labels › Which discretization rule should I compare?]   72 visits, 10 experts

options: Optimize ordinal cutpoints (19) | Use simple clip-and-round (3) | Match empirical target frequencies (4) | Merge or threshold near-equal scores (6) | Compare group-specific cutpoints (2) | Handle degenerate bins and ties (4)

check first: E151 The ordinal metric is sensitive to cutpoints and representative held-out predictions are available.  imp 0.82 → +Optimize ordinal cutpoints  [first in 37/45 visits that checked it]
then:        E154 Continuous predictions correspond to a small set of repeated target levels.  imp 0.55 → +Merge or threshold near-equal scores  [first in 24/71 visits that checked it]
then:        E153 Known target frequencies are stable enough to support a distribution-matching comparison.  imp 0.65 → +Match empirical target frequencies  [first in 4/27 visits that checked it]
more:         5 further checks (E317, E152, E156, E157, E155), load on request
enough when:  top option >= 30% (lower quartile over 72 visits) or >= 5 points ahead; median 4 checks
come back:    after 'regression after a single change' (2/5); after 'regression after a bundled change' (1/5); after '4+ scored steps without a new best' (1/5)  [5 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 49% of visits
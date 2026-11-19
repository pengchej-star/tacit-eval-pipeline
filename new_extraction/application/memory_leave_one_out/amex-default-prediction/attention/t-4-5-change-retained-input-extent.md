# [Change retained input extent › Which part of the input extent should be varied?]   44 visits, 9 experts

options: Tune input resolution (12) | Tune the spatial crop (5) | Match the temporal context (3)

check first: E91 Relevant small structures disappear at the current resize resolution.  imp 0.85 → +Tune input resolution  [first in 15/18 visits that checked it]
then:        E302 The resolution-vs-score curve from prior experiments provides a clear signal (trend or peak) to guide the next resolution choice.  imp 0.75 → +Tune input resolution  [first in 8/24 visits that checked it]
then:        E92 Spatial borders contain irrelevant regions or the current crop removes useful content.  imp 0.80 → +Tune the spatial crop  [first in 6/10 visits that checked it]
more:         9 further checks (E307, E94, E93, E305, E303, E304, E309, E308, E306), load on request
enough when:  top option >= 63% (lower quartile over 44 visits) or >= 44 points ahead; median 4 checks
come back:    after 'regression after a single change' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 89% of visits
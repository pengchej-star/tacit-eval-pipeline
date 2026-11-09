# [Make useful experiments feasible › Which execution change removes the current bottleneck?]   362 visits, 45 experts

options: Control peak resource use (37) | Shorten experiment turnaround (58) | Make pipeline changes reproducible (61)

check first: E172 Hard-coded paths, duplicated model code, or unrecorded settings cause configuration drift.  imp 0.80 → +Make pipeline changes reproducible  [first in 105/140 visits that checked it]
then:        E171 Repeated trials recompute unchanged work or fail late after expensive training.  imp 0.75 → +Shorten experiment turnaround  [first in 86/119 visits that checked it]
then:        E170 Peak memory or per-batch throughput is the limiting resource.  imp 0.85 → +Control peak resource use  [first in 66/91 visits that checked it]
more:         13 further checks (E333, E331, E332, E342, E340, E335, E339, E336, E338, E337, E343, E341, E334), load on request
enough when:  top option >= 53% (lower quartile over 360 visits) or >= 22 points ahead; median 3 checks
come back:    after 'other' (9/26); after '4+ scored steps without a new best' (7/26); after '3 scored steps without a new best' (4/26)  [26 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 76% of visits
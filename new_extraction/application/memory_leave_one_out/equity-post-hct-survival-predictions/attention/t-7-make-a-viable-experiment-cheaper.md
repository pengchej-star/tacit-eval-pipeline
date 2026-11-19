# [Make a viable experiment cheaper › Which measured bottleneck should I remove?]   252 visits, 42 experts

options: Reduce peak memory (36) | Cache stable intermediate artifacts (18) | Use a reduced development run (24) | Consolidate configuration and preserve outputs (35) | Replace a slow computation with an equivalent implementation (2)

check first: E98 Repeated manual path, flag, or member-list edits cause configuration drift.  imp 0.65 → +Consolidate configuration and preserve outputs  [first in 83/118 visits that checked it]
then:        E97 A full run is expensive before basic correctness or a coarse candidate can be assessed.  imp 0.78 → +Use a reduced development run  [first in 61/77 visits that checked it]
then:        E95 Runs fail or become unstable at a measured memory peak.  imp 0.92 → +Reduce peak memory  [first in 57/75 visits that checked it]
more:         2 further checks (E96, E99), load on request
enough when:  top option >= 43% (lower quartile over 247 visits) or >= 24 points ahead; median 1 checks
come back:    after '4+ scored steps without a new best' (8/26); after 'other' (7/26); after 'after a new best' (4/26)  [26 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 88% of visits
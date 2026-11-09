# [Shorten experiment turnaround › What can I reduce or reuse without invalidating the experiment?]   160 visits, 27 experts

options: Run a reduced end-to-end smoke test (37) | Cache expensive reusable artifacts (16) | Resume only unfinished training (3) | Restore full production execution (2)

check first: E179 The current task is checking correctness and failures occur after expensive work.  imp 0.72 → +Run a reduced end-to-end smoke test  [first in 78/89 visits that checked it]
then:        E180 Only downstream settings change while upstream features or predictions remain identical.  imp 0.78 → +Cache expensive reusable artifacts  [first in 32/44 visits that checked it]
then:        E353 The expert is iterating over a single hyperparameter and needs fast per-trial feedback rather than full production runs.  imp 0.70 → +Run a reduced end-to-end smoke test  [first in 20/80 visits that checked it]
more:         12 further checks (E182, E357, E181, E352, E356, E362, E359, E354, E361, E358, E355, E360), load on request
enough when:  top option >= 52% (lower quartile over 160 visits) or >= 28 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (4/9); after 'other' (2/9); after 'regression after a bundled change' (1/9)  [9 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 80% of visits
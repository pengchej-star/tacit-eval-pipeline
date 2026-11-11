# [Decode predictions onto an ordered label scale › Which discretization rule should map scores to allowed labels?]   72 visits, 10 experts

options: Use simple fixed rounding (1) | Tune global thresholds (30) | Match a justified label distribution (1) | Use subgroup-specific thresholds (1) | Handle discrete ties and degenerate outputs (4) | Restore global thresholds (1)

check first: E289 Public high-scoring solutions or known best practices for this task use threshold optimization (e.g., Nelder-Mead on OOF) to maximize the evaluation metric.  imp 0.85 → +Tune global thresholds  [first in 24/60 visits that checked it]
then:        E138 Labels are ordinal and held-out continuous predictions have systematic boundary errors.  imp 0.70 → +Tune global thresholds  [first in 13/23 visits that checked it]
then:        E292 The discretization code path has a bug (missing column, name inconsistency, or incorrect guard) that prevents it from executing correctly.  imp 0.60 → +Handle discrete ties and degenerate outputs  [first in 7/28 visits that checked it]
more:         19 further checks (E139, E141, E137, E290, E142, E302, E295, E140, E299, E298, E293, E296, E304, E291, E294, E301, E303, E297, E300), load on request
enough when:  top option >= 44% (lower quartile over 72 visits) or >= 24 points ahead; median 6 checks
come back:    after 'regression after a single change' (2/3); after 'after a new best' (1/3)  [3 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 64% of visits
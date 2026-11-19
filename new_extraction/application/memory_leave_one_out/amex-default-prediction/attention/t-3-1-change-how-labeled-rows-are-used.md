# [Change how labeled rows are used › Which change to the existing labeled population is justified?]   39 visits, 8 experts

options: Filter suspected label errors (2) | Select a representative training subset (6) | Deduplicate overlapping observations (1) | Resample underrepresented examples (5) | Weight training examples (2) | Refit with more labeled rows (1)

check first: E52 An identifiable source or low-confidence subset differs from the expected test population.  imp 0.75 → +Select a representative training subset  [first in 17/23 visits that checked it]
then:        E260 A previous version implementing this change was not submitted/scored, so a re-run is needed to obtain the leaderboard score.  imp 0.40 → +Select a representative training subset  [first in 9/26 visits that checked it]
then:        E53 Training includes duplicated observations or overlapping windows from the same event.  imp 0.85 → +Deduplicate overlapping observations  [first in 4/6 visits that checked it]
more:         17 further checks (E51, E54, E56, E261, E268, E266, E265, E267, E263, E264, E262, E269, E273, E55, E271, E270, E272), load on request
enough when:  top option >= 34% (lower quartile over 39 visits) or >= 9 points ahead; median 9 checks
come back:    after 'after a new best' (3/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 38% of visits
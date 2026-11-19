# [Repair failed execution › What prevents the intended inference run from producing a valid artifact?]   137 visits, 30 experts

options: Repair imports and artifact paths (17) | Use a supported device path (7) | Verify the submitted artifact (9) | Repair the first failing operation (20) | Replace invalid fallback predictions (4)

check first: E22 The first failure is an import error or unresolved artifact path.  imp 0.95 → +Repair imports and artifact paths  [first in 44/108 visits that checked it]
then:        E25 The first failure is an API, variable, or configuration error on a small batch.  imp 0.88 → +Repair the first failing operation  [first in 44/66 visits that checked it]
then:        E24 Inference finishes but the required prediction file is absent, incomplete, or from debug mode.  imp 0.85 → +Verify the submitted artifact  [first in 15/38 visits that checked it]
more:         10 further checks (E23, E228, E230, E229, E227, E26, E27, E231, E233, E232), load on request
enough when:  top option >= 60% (lower quartile over 137 visits) or >= 39 points ahead; median 5 checks
come back:    after '4+ scored steps without a new best' (3/10); after '2 scored steps without a new best' (3/10); after 'other' (3/10)  [10 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 75% of visits
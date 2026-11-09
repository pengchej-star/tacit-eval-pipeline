# [Repair incorrect or mismatched predictions › Which failure mechanism should I investigate first?]   392 visits, 58 experts

options: Restore model and input compatibility (64) | Locate a data-flow defect (65) | Resolve the first execution failure (57)

check first: E27 A new artifact or representation was introduced immediately before the failure.  imp 0.40 → +Restore model and input compatibility  [first in 273/335 visits that checked it]
then:        E29 A traceback or absent output file identifies an execution dependency failure.  imp 0.90 → +Resolve the first execution failure  [first in 57/269 visits that checked it]
then:        E28 Execution completes but outputs are constant, implausible, or omit configured components.  imp 0.75 → -Resolve the first execution failure  [first in 35/137 visits that checked it]
more:         6 further checks (E196, E199, E201, E198, E197, E200), load on request
enough when:  top option >= 59% (lower quartile over 390 visits) or >= 21 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (12/33); after 'other' (8/33); after '3 scored steps without a new best' (5/33)  [33 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 69% of visits
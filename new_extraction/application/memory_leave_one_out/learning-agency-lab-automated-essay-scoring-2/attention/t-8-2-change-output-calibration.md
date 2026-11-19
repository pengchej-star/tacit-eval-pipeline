# [Change output calibration › What systematic output mismatch should be corrected?]   27 visits, 9 experts

options: Correct a validated prediction offset (3) | Tune logit temperature before blending (2) | Reweight class probabilities (3) | Enforce the required output range (3) | Keep the raw ordered predictions (3)

check first: E188 Only ordering is scored and added scaling or clipping has no validated benefit.  imp 0.88 → +Keep the raw ordered predictions  [first in 7/27 visits that checked it]
then:        E349 A previous calibration change (e.g., scaling multiplier) was associated with a score change, suggesting reverting or re-testing that specific setting is warranted.  imp 0.65 → +Correct a validated prediction offset  [first in 7/26 visits that checked it]
then:        E184 Held-out regression residuals show a stable offset or a reliable reference example exposes one.  imp 0.92 → +Correct a validated prediction offset  [first in 5/6 visits that checked it]
more:         8 further checks (E187, E186, E185, E350, E354, E352, E351, E353), load on request
enough when:  top option >= 48% (lower quartile over 27 visits) or >= 24 points ahead; median 5 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 59% of visits
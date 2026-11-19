# [Make a comparison interpretable › Which observation or experiment is needed before accepting the next change?]   725 visits, 52 experts

options: Isolate one change (134) | Measure repeatability (47) | Control randomness (4) | Redirect an unproductive search (32) | Bracket interacting settings (28) | Screen candidates locally (3) | Profile the prediction units and data schema (1) | Evaluate the first complete baseline (1)

check first: E19 The score comparison changed multiple settings or artifacts simultaneously.  imp 0.72 → +Isolate one change  [first in 413/701 visits that checked it]
then:        E20 The claimed gain is comparable to variation already observed across unchanged runs.  imp 0.78 → +Measure repeatability  [first in 181/408 visits that checked it]
then:        E22 Recent trials along the same lever repeatedly tie or worsen the best validated result.  imp 0.65 → +Redirect an unproductive search  [first in 96/390 visits that checked it]
more:         6 further checks (E23, E21, E24, E27, E25, E26), load on request
enough when:  top option >= 28% (lower quartile over 725 visits) or >= 5 points ahead; median 4 checks
come back:    after 'regression after a single change' (10/34); after 'after a new best' (10/34); after 'other' (6/34)  [34 returns, 12 improved the score]

scores: LLM-guessed; top option matches the option taken in 65% of visits
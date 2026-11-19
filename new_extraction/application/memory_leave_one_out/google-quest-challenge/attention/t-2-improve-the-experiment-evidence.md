# [Improve the experiment evidence › What evidence-producing change should guide the next modeling decision?]   798 visits, 58 experts

options: Choose a diagnostic comparison (248) | Choose the validation design (21) | Align local evaluation with the task (15) | Inspect the prediction units (1)

check first: E18 Multiple edits, noisy scores, or a regression obscure the effect of the latest experiment.  imp 0.55 → +Choose a diagnostic comparison  [first in 757/782 visits that checked it]
then:        E20 Training selects models using a surrogate metric or incorrectly configured callback.  imp 0.70 → +Align local evaluation with the task  [first in 13/29 visits that checked it]
then:        E128 A known code bug (variable name error, type mismatch, uninitialized variable, or incorrect construction) is corrupting results or blocking execution.  imp 0.50 → +Choose a diagnostic comparison  [first in 8/233 visits that checked it]
more:         11 further checks (E130, E129, E21, E19, E133, E125, E127, E131, E126, E134, E132), load on request
enough when:  top option >= 49% (lower quartile over 798 visits) or >= 27 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (6/14); after 'other' (4/14); after 'regression after a single change' (2/14)  [14 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 93% of visits
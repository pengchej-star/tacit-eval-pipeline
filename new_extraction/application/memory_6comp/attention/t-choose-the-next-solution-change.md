# [Choose the next solution change › what can I change to improve my solution?]   3658 visits, 60 experts

options: Repair prediction validity (255) | Improve the evidence for choosing a change (355) | Change examples or supervision (31) | Change the information presented to the model (178) | Change the fitted learner (95) | Change how the model is trained (72) | Change the prediction ensemble (499) | Change prediction decoding or calibration (65)

check first: E150 The current pipeline crashes or produces missing, incompatible, or implausible predictions.  imp 0.85 → +Repair prediction validity  [first in 3154/3336 visits that checked it]
then:        E151 Existing comparisons are confounded, noisy, unrepresentative, or too expensive to complete.  imp 0.55 → +Improve the evidence for choosing a change  [first in 189/1529 visits that checked it]
then:        E156 Multiple validated prediction sources or compatible repeated views have complementary errors.  imp 0.70 → +Change the prediction ensemble  [first in 73/1138 visits that checked it]
more:         5 further checks (E157, E154, E153, E155, E152), load on request
enough when:  top option >= 25% (lower quartile over 3609 visits) or >= 3 points ahead; median 2 checks
come back:    after 'other' (12/20); after '4+ scored steps without a new best' (4/20); after '2 scored steps without a new best' (3/20)  [20 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 74% of visits
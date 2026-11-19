# [Improve comparison reliability › What prevents the current evaluation from supporting the next model choice?]   607 visits, 52 experts

options: Change the evaluation sample (16) | Change the model-selection signal (12) | Change the experiment design (189)

check first: E11 Multiple edits or stochastic reruns make the latest score movement ambiguous.  imp 0.65 → +Change the experiment design  [first in 549/584 visits that checked it]
then:        E10 The reported evaluation callback is incorrect, unstable, or a measured runtime bottleneck.  imp 0.80 → +Change the model-selection signal  [first in 26/32 visits that checked it]
then:        E200 No valid submission file has been produced, so external (leaderboard) scoring feedback is unavailable for comparison.  imp 0.65 → +Change the model-selection signal  [first in 9/512 visits that checked it]
more:         6 further checks (E196, E09, E197, E198, E195, E199), load on request
enough when:  top option >= 54% (lower quartile over 606 visits) or >= 25 points ahead; median 3 checks
come back:    after 'after a new best' (5/13); after 'other' (4/13); after '4+ scored steps without a new best' (3/13)  [13 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 76% of visits
# [Choose the next improvement › what can I change to improve my solution?]   3425 visits, 60 experts

options: Repair incorrect execution (197) | Improve the evidence for a change (283) | Change training evidence (33) | Change the input representation (138) | Improve an individual model (186) | Change how models are combined (469) | Change inference or final output mapping (98) | Remove an execution bottleneck (93)

check first: E01 The current pipeline fails, produces implausible predictions, or regressed sharply after an integration change.  imp 0.82 → +Repair incorrect execution  [first in 2954/3148 visits that checked it]
then:        E02 There is no trustworthy baseline or the observed gain cannot be distinguished from confounding or variability.  imp 0.55 → +Improve the evidence for a change  [first in 161/2549 visits that checked it]
then:        E06 Several valid prediction sources exist and their held-out errors are not identical.  imp 0.70 → +Change how models are combined  [first in 99/1517 visits that checked it]
more:         5 further checks (E08, E04, E07, E05, E03), load on request
enough when:  top option >= 28% (lower quartile over 3411 visits) or >= 6 points ahead; median 3 checks
come back:    after 'other' (12/23); after '2 scored steps without a new best' (5/23); after 'regression after a single change' (2/23)  [23 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 62% of visits
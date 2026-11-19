# [Repair prediction validity › Which failure should be repaired before comparing model quality?]   586 visits, 57 experts

options: Restore model and input compatibility (44) | Repair execution and output assembly (102) | Restore a trustworthy implementation (109)

check first: E17 There is a traceback, missing output, or incorrect ensemble calculation.  imp 0.85 → +Repair execution and output assembly  [first in 285/422 visits that checked it]
then:        E18 The code runs but repeated refactors have made the effective configuration uncertain.  imp 0.55 → +Restore a trustworthy implementation  [first in 207/536 visits that checked it]
then:        E16 The loaded model or transformed inputs differ from the training artifacts.  imp 0.72 → +Restore model and input compatibility  [first in 86/134 visits that checked it]
more:         2 further checks (E159, E158), load on request
enough when:  top option >= 63% (lower quartile over 584 visits) or >= 32 points ahead; median 3 checks
come back:    after 'other' (10/34); after '4+ scored steps without a new best' (9/34); after 'regression after a single change' (4/34)  [34 returns, 8 improved the score]

scores: LLM-guessed; top option matches the option taken in 50% of visits
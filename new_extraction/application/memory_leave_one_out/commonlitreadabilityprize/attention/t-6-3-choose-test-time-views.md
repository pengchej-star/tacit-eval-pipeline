# [Choose test-time views › Should inference average transformed views or preserve the original view?]   48 visits, 8 experts

options: Average valid test-time views (21) | Use identity-only inference (3)

check first: E103 Flips, mirrored channels or alternate crops preserve the task label and were compatible with training.  imp 0.85 → +Average valid test-time views  [first in 20/25 visits that checked it]
then:        E105 Controlled TTA trials show no reliable gain for this checkpoint or ensemble.  imp 0.70 → +Use identity-only inference  [first in 11/36 visits that checked it]
then:        E241 The TTA change is being combined with another inference change in the same submission, confounding the comparison.  imp 0.40 → +Use identity-only inference  [first in 5/47 visits that checked it]
more:         10 further checks (E236, E104, E238, E242, E240, E243, E244, E239, E106, E237), load on request
enough when:  top option >= 70% (lower quartile over 48 visits) or >= 39 points ahead; median 6 checks
come back:    after 'after a new best' (1/1)  [1 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 81% of visits
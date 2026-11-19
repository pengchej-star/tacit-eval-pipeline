# [Repair the pipeline › Which observed failure should I correct first?]   447 visits, 52 experts

options: Repair dependencies and device setup (22) | Match the model to its checkpoint (21) | Verify checkpoint selection and file discovery (3) | Join features and predictions by identifier (13) | Reuse fitted encoders and preprocessing (9) | Correct prediction arithmetic and data flow (25) | Correct metric and objective implementations (8) | Verify the actual submitted predictions (17) | Isolate a failing stage on a small sample (57) | Check prediction parity after refactoring (19)

check first: E01 Execution fails during import, file access or device initialization.  imp 0.95 → +Repair dependencies and device setup  [first in 186/339 visits that checked it]
then:        E09 Several stages are unverified and the first faulty transformation is unknown.  imp 0.95 → +Isolate a failing stage on a small sample  [first in 72/182 visits that checked it]
then:        E02 The loaded checkpoint disagrees with the model architecture or vocabulary.  imp 0.90 → +Match the model to its checkpoint  [first in 42/120 visits that checked it]
more:         7 further checks (E06, E04, E08, E10, E05, E03, E07), load on request
enough when:  top option >= 31% (lower quartile over 446 visits) or >= 10 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (14/36); after 'other' (6/36); after '3 scored steps without a new best' (4/36)  [36 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 79% of visits
# [Change prediction decoding or calibration › Which output adjustment addresses the metric mismatch?]   128 visits, 22 experts

options: Decode predictions onto an ordered label scale (38) | Calibrate continuous or probability outputs (27)

check first: E148 Allowed outputs are discrete or quasi-discrete and the metric rewards their correct ordering or agreement.  imp 0.90 → +Decode predictions onto an ordered label scale  [first in 120/124 visits that checked it]
then:        E149 Outputs remain continuous or probabilistic but exhibit a systematic held-out calibration defect.  imp 0.90 → +Calibrate continuous or probability outputs  [first in 6/38 visits that checked it]
then:        E288 The evaluation metric is invariant to monotonic transformations, making certain calibration adjustments (e.g., clipping) irrelevant to the score.  imp 0.40 → -Calibrate continuous or probability outputs  [first in 2/127 visits that checked it]
more:         1 further checks (E287), load on request
enough when:  top option >= 94% (lower quartile over 128 visits) or >= 87 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (1/2); after '2 scored steps without a new best' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 80% of visits
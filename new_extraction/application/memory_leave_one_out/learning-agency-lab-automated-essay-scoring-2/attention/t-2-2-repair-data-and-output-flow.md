# [Repair data and output flow › Which data-flow invariant is failing?]   154 visits, 30 experts

options: Trace rows and executed branches (35) | Audit intermediate feature tensors (13) | Restore training-time preprocessing (21) | Reuse encoders with unknown-category handling (2) | Remove unavailable or leaking inputs (2) | Compare outputs across a refactor (3)

check first: E38 Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.  imp 0.75 → +Restore training-time preprocessing  [first in 44/63 visits that checked it]
then:        E36 Outputs are constant across substantial edits or some configured members never produce predictions.  imp 0.72 → +Trace rows and executed branches  [first in 38/44 visits that checked it]
then:        E213 The variable feeding a downstream stage references the wrong version of the data (e.g., raw vs. preprocessed, or vice versa).  imp 0.70 → +Trace rows and executed branches  [first in 14/43 visits that checked it]
more:         15 further checks (E41, E37, E39, E220, E214, E212, E216, E40, E219, E221, E215, E222, E217, E218, E223), load on request
enough when:  top option >= 32% (lower quartile over 153 visits) or >= 9 points ahead; median 2 checks
come back:    after 'other' (4/11); after '4+ scored steps without a new best' (4/11); after 'regression after a single change' (2/11)  [11 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 66% of visits
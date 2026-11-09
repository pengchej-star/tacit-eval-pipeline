# [Change the prediction architecture › Which architectural component should I alter?]   58 visits, 14 experts

options: Change head capacity or attention (6) | Change pooling or representation normalization (7) | Add auxiliary supervision (3) | Change feature-level modality fusion (10) | Change training-time dropout (4)

check first: E99 Multiple informative branches are merged by a lossy or untested rule.  imp 0.70 → +Change feature-level modality fusion  [first in 18/23 visits that checked it]
then:        E96 The backbone feeds a minimal, inappropriate shared, or oversized head.  imp 0.72 → +Change head capacity or attention  [first in 11/14 visits that checked it]
then:        E97 Only one hidden layer or pooling statistic is used despite variable-length or multi-layer information.  imp 0.82 → +Change pooling or representation normalization  [first in 7/11 visits that checked it]
more:         8 further checks (E100, E98, E278, E280, E282, E277, E279, E281), load on request
enough when:  top option >= 42% (lower quartile over 57 visits) or >= 22 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (2/3); after 'after a new best' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 91% of visits
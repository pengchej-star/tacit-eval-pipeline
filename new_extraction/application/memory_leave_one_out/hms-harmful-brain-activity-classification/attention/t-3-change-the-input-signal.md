# [Change the input signal › Which input intervention addresses the missing or noisy signal?]   462 visits, 38 experts

options: Represent the available information (120) | Select or refresh features (47) | Change training examples (18)

check first: E48 Raw data contains structure not represented by current features.  imp 0.75 → +Represent the available information  [first in 214/217 visits that checked it]
then:        E49 The feature set is large, changed recently or contains suspected unhelpful groups.  imp 0.70 → +Select or refresh features  [first in 150/223 visits that checked it]
then:        E50 Label quality, imbalance or limited coverage constrains the current learner.  imp 0.60 → +Change training examples  [first in 39/48 visits that checked it]
enough when:  top option >= 58% (lower quartile over 403 visits) or >= 30 points ahead; median 1 checks
come back:    after 'after a new best' (5/9); after 'other' (3/9); after 'regression after a single change' (1/9)  [9 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 86% of visits
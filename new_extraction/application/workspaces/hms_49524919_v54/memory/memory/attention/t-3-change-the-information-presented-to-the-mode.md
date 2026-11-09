# [Change the information presented to the model › Which input representation should I change next?]   452 visits, 38 experts

options: Represent repeated or structured records (26) | Represent text for the model (46) | Represent images and signals (50) | Control the feature set (61)

check first: E47 Image or signal preprocessing discards potentially label-relevant detail.  imp 0.90 → +Represent images and signals  [first in 103/326 visits that checked it]
then:        E46 Free text is the principal input and residuals vary with language or document structure.  imp 0.90 → +Represent text for the model  [first in 91/257 visits that checked it]
then:        E48 An expanded or stale feature set is associated with worse validation or schema drift.  imp 0.70 → +Control the feature set  [first in 81/182 visits that checked it]
more:         22 further checks (E45, E208, E214, E216, E215, E212, E209, E223, E225, E217, E221, E210, E219, E218, E220, E213, E228, E226, E211, E227, E222, E224), load on request
enough when:  top option >= 54% (lower quartile over 450 visits) or >= 24 points ahead; median 6 checks
come back:    after 'after a new best' (6/12); after 'other' (3/12); after '3 scored steps without a new best' (1/12)  [12 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 76% of visits
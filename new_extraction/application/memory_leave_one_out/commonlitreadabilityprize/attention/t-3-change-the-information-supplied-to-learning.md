# [Change the information supplied to learning › Which information change addresses the observed input limitation?]   610 visits, 41 experts

options: Choose a new feature source (67) | Choose feature-set complexity (38) | Change input preprocessing (87) | Choose missing-value treatment (10) | Choose training examples (27)

check first: E62 The feature matrix is large or recently expanded and selection artifacts may be stale.  imp 0.65 → +Choose a new feature source  [first in 147/190 visits that checked it]
then:        E63 A fixed trained model receives text, images or signals whose representation can be checked against training.  imp 0.60 → +Change input preprocessing  [first in 109/180 visits that checked it]
then:        E156 Recently added engineered features have not improved the score, suggesting a different feature source or transformation type is needed.  imp 0.78 → +Choose a new feature source  [first in 67/192 visits that checked it]
more:         18 further checks (E65, E61, E158, E164, E161, E163, E160, E64, E166, E159, E157, E169, E162, E168, E167, E165, E170, E171), load on request
enough when:  top option >= 40% (lower quartile over 608 visits) or >= 12 points ahead; median 4 checks
come back:    after 'after a new best' (7/15); after 'other' (3/15); after '4+ scored steps without a new best' (3/15)  [15 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 49% of visits
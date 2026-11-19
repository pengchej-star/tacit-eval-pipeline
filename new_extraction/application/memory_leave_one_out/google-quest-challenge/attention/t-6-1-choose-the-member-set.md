# [Choose the member set › How should the ensemble member set change?]   525 visits, 42 experts

options: Add a complementary member (116) | Replace a weak member (18) | Prune or retain through ablation (105) | Restore lost diversity (14)

check first: E88 A candidate has nonredundant errors and plausible standalone quality.  imp 0.60 → +Add a complementary member  [first in 223/242 visits that checked it]
then:        E90 A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.  imp 0.70 → +Prune or retain through ablation  [first in 193/253 visits that checked it]
then:        E91 A previously better ensemble lost members during a recent change.  imp 0.80 → +Restore lost diversity  [first in 63/358 visits that checked it]
more:         1 further checks (E89), load on request
enough when:  top option >= 43% (lower quartile over 502 visits) or >= 6 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (8/20); after 'after a new best' (6/20); after 'other' (3/20)  [20 returns, 9 improved the score]

scores: LLM-guessed; top option matches the option taken in 52% of visits
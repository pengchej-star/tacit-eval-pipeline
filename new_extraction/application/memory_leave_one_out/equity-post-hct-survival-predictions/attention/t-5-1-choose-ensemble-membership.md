# [Choose ensemble membership › How should the current member set change?]   565 visits, 40 experts

options: Add a complementary predictor (100) | Prune or substitute members (50) | Compare a single predictor with the blend (30) | Change the number of fold checkpoints (50) | Average independent training seeds (11)

check first: E66 A plausible candidate has errors different from the current ensemble on the same validation rows.  imp 0.82 → +Add a complementary predictor  [first in 166/197 visits that checked it]
then:        E67 A member or group has weak or redundant marginal contribution in earlier ablations.  imp 0.65 → +Prune or substitute members  [first in 156/312 visits that checked it]
then:        E68 The full blend has never been compared with its strongest member under the same evaluation.  imp 0.45 → +Compare a single predictor with the blend  [first in 122/335 visits that checked it]
more:         2 further checks (E69, E70), load on request
enough when:  top option >= 33% (lower quartile over 557 visits) or >= 5 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (10/29); after 'after a new best' (10/29); after '2 scored steps without a new best' (4/29)  [29 returns, 11 improved the score]

scores: LLM-guessed; top option matches the option taken in 60% of visits
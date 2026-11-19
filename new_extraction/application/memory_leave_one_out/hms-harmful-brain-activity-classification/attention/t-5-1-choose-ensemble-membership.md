# [Choose ensemble membership › Which membership change is justified by marginal contribution?]   300 visits, 33 experts

options: Add a complementary model family (51) | Add diversity from training or input variants (12) | Select members by marginal ensemble contribution (51) | Restore validated ensemble members (4) | Compare matched checkpoint variants (18) | Select fold or full-data checkpoints (15)

check first: E71 The ensemble’s errors are shared across similar members and a distinct candidate is available.  imp 0.85 → +Add a complementary model family  [first in 89/89 visits that checked it]
then:        E73 Some available members may add noise or redundancy despite acceptable standalone scores.  imp 0.75 → +Select members by marginal ensemble contribution  [first in 79/124 visits that checked it]
then:        E75 Several compatible trained checkpoints differ in seed, recipe or training stage.  imp 0.50 → +Compare matched checkpoint variants  [first in 59/150 visits that checked it]
more:         4 further checks (E72, E74, E76, E77), load on request
enough when:  top option >= 32% (lower quartile over 297 visits) or >= 9 points ahead; median 2 checks
come back:    after 'after a new best' (8/23); after '4+ scored steps without a new best' (4/23); after '3 scored steps without a new best' (3/23)  [23 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 64% of visits
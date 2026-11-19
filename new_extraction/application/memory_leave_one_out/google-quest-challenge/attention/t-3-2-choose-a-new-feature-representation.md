# [Choose a new feature representation › Which feature representation should be tested next?]   251 visits, 22 experts

options: Summarize entity histories (12) | Encode change and interactions (9) | Add structural and linguistic features (14) | Tune sparse or latent text features (4) | Add pretrained representations (29) | Add a complementary signal representation (11) | Select input branches by ablation (9)

check first: E50 Available pretrained representations encode information missing from the current tabular features.  imp 0.80 → +Add pretrained representations  [first in 49/66 visits that checked it]
then:        E46 Multiple observations describe each prediction entity but only a narrow summary is used.  imp 0.95 → +Summarize entity histories  [first in 47/58 visits that checked it]
then:        E48 Text structure or metadata relevant to the target is absent from current representations.  imp 0.80 → +Add structural and linguistic features  [first in 46/111 visits that checked it]
more:         5 further checks (E52, E51, E47, E49, E53), load on request
enough when:  top option >= 34% (lower quartile over 250 visits) or >= 8 points ahead; median 2 checks
come back:    after '2 scored steps without a new best' (1/4); after 'other' (1/4); after '4+ scored steps without a new best' (1/4)  [4 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 76% of visits
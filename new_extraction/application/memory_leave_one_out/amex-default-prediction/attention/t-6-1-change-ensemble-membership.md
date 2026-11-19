# [Change ensemble membership › Which membership experiment is most informative now?]   628 visits, 49 experts

options: Compare the best member with the blend (21) | Select ensemble members by ablation (102) | Choose a source of ensemble diversity (115) | Average repeated training variants (53)

check first: E141 A recent member addition regressed or several members appear redundant.  imp 0.55 → +Select ensemble members by ablation  [first in 257/395 visits that checked it]
then:        E142 Current members share highly correlated errors and an unused prediction source is available.  imp 0.75 → +Choose a source of ensemble diversity  [first in 188/355 visits that checked it]
then:        E140 The ensemble has not been compared with its strongest single member.  imp 0.82 → +Compare the best member with the blend  [first in 107/186 visits that checked it]
more:         2 further checks (E143, E144), load on request
enough when:  top option >= 37% (lower quartile over 625 visits) or >= 12 points ahead; median 2 checks
come back:    after 'after a new best' (10/29); after 'other' (6/29); after '4+ scored steps without a new best' (5/29)  [29 returns, 7 improved the score]

scores: LLM-guessed; top option matches the option taken in 62% of visits
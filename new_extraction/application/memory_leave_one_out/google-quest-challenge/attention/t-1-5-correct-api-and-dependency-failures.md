# [Correct API and dependency failures › Which execution contract is violated?]   60 visits, 21 experts

options: Repair imports and artifact paths (10) | Align model and tensor devices (7) | Match the library API (12)

check first: E15 The first failing operation cannot import a module or locate a required file.  imp 0.95 → +Repair imports and artifact paths  [first in 28/56 visits that checked it]
then:        E17 The failing call uses an unsupported method, argument, or type.  imp 0.90 → +Match the library API  [first in 21/45 visits that checked it]
then:        E16 The failing call mixes devices or requests unavailable acceleration.  imp 0.90 → +Align model and tensor devices  [first in 11/54 visits that checked it]
more:         1 further checks (E124), load on request
enough when:  top option >= 89% (lower quartile over 60 visits) or >= 82 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (2/3); after '2 scored steps without a new best' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 93% of visits
# [Choose training examples › Which change to the training population is supported by the available data?]   76 visits, 12 experts

options: Filter or reweight unreliable and shifted examples (9) | Add relevant external labeled data (3) | Train with pseudo-labeled examples (3) | Adjust class or population weights (8) | Generate synthetic training examples (4)

check first: E55 A localized training subset has unreliable labels, duplicates or a distribution unlike the test population.  imp 0.85 → +Filter or reweight unreliable and shifted examples  [first in 31/31 visits that checked it]
then:        E58 The target metric exposes errors concentrated in an underrepresented class or population.  imp 0.75 → +Adjust class or population weights  [first in 24/28 visits that checked it]
then:        E56 Additional labeled examples have compatible labels and usable input formats.  imp 0.75 → +Add relevant external labeled data  [first in 11/18 visits that checked it]
more:         4 further checks (E57, E59, E184, E60), load on request
enough when:  top option >= 45% (lower quartile over 76 visits) or >= 21 points ahead; median 2 checks
come back:    after 'after a new best' (2/4); after '4+ scored steps without a new best' (1/4); after 'regression after a bundled change' (1/4)  [4 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 80% of visits
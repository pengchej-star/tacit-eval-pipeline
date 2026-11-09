# [Choose training augmentation › Which augmentation should I test against the unaugmented baseline?]   13 visits, 2 experts

options: Use mild image perturbations (2) | Mask signal regions (1) | Mix labeled examples (1)

check first: E85 Small image brightness or geometric changes preserve the target semantics.  imp 0.85 → +Use mild image perturbations  [first in 5/5 visits that checked it]
then:        E86 The model relies on narrow time-frequency patches that may be absent at inference.  imp 0.80 → +Mask signal regions  [first in 5/5 visits that checked it]
then:        E87 Targets can be meaningfully mixed and current training overfits individual examples.  imp 0.75 → +Mix labeled examples  [first in 2/3 visits that checked it]
more:         2 further checks (E244, E243), load on request
enough when:  top option >= 69% (lower quartile over 13 visits) or >= 52 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 92% of visits
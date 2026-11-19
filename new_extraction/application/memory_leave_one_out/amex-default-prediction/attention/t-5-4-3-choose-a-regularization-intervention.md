# [Choose a regularization intervention › Which training regularizer fits the input and observed overfitting?]   17 visits, 5 experts

options: Tune head regularization (3) | Use mild image augmentation (2) | Mask temporal or spectral regions (1) | Mix training examples (1)

check first: E131 Small visual intensity or geometric changes preserve the label.  imp 0.78 → +Use mild image augmentation  [first in 5/8 visits that checked it]
then:        E132 Spectral inputs contain locally redundant regions and masking preserves the event label.  imp 0.80 → +Mask temporal or spectral regions  [first in 3/6 visits that checked it]
then:        E130 A high-capacity head overfits while the pretrained representation remains useful.  imp 0.82 → +Tune head regularization  [first in 3/3 visits that checked it]
more:         9 further checks (E361, E133, E362, E364, E134, E358, E360, E363, E359), load on request
enough when:  top option >= 57% (lower quartile over 17 visits) or >= 43 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 100% of visits
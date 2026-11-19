# [Change training augmentation › Which training augmentation is compatible with the task’s invariances?]   13 visits, 2 experts

options: Use mild image perturbations (2) | Mask local signal regions (1) | Blend examples and soft labels (1)

check first: E112 Image intensity varies naturally but strong augmentation has previously distorted useful structure.  imp 0.82 → +Use mild image perturbations  [first in 5/5 visits that checked it]
then:        E113 The model sees spectrograms and should tolerate missing local time-frequency evidence.  imp 0.85 → +Mask local signal regions  [first in 3/11 visits that checked it]
then:        E288 The previous augmentation run did not clearly improve over the non-augmented baseline, so a re-run is needed to distinguish signal from variance.  imp 0.40 → +Use mild image perturbations  [first in 2/13 visits that checked it]
more:         3 further checks (E114, E287, E286), load on request
enough when:  top option >= 79% (lower quartile over 13 visits) or >= 66 points ahead; median 4 checks
come back:    after '4+ scored steps without a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 100% of visits
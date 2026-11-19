# [Change basic feature encoding › Which basic encoding change addresses the observed input problem?]   13 visits, 7 experts

options: Choose model-aware imputation (2) | Reuse fitted categorical mappings (2) | Match input normalization to the learner (5)

check first: E70 Test categories are unseen or encoded differently from training categories.  imp 0.90 → +Reuse fitted categorical mappings  [first in 5/5 visits that checked it]
then:        E71 Input scales differ markedly across features or from the pretrained backbone’s expected distribution.  imp 0.85 → +Match input normalization to the learner  [first in 4/5 visits that checked it]
then:        E69 A selected learner receives NaN or infinite values it cannot handle natively.  imp 0.90 → +Choose model-aware imputation  [first in 3/3 visits that checked it]
more:         2 further checks (E72, E287), load on request
enough when:  top option >= 58% (lower quartile over 13 visits) or >= 31 points ahead; median 2 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 92% of visits
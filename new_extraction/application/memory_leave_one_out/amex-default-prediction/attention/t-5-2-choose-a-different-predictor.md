# [Choose a different predictor › Which alternative predictor addresses the current model’s limitation?]   88 visits, 20 experts

options: Change the learner family (10) | Change the pretrained backbone (10) | Change model capacity (14) | Fit a shallow model on embeddings (2) | Use neighbors as predictive evidence (2)

check first: E103 Repeated variants of the same algorithm have plateaued on the same feature matrix.  imp 0.72 → +Fit a shallow model on embeddings  [first in 27/28 visits that checked it]
then:        E318 A trained variant of a different capacity within the same backbone family has a checkpoint available and can be evaluated standalone.  imp 0.65 → +Change model capacity  [first in 10/39 visits that checked it]
then:        E104 A compatible backbone pretrained on more relevant data or with a different objective is available.  imp 0.78 → +Change the pretrained backbone  [first in 10/15 visits that checked it]
more:         22 further checks (E105, E317, E324, E320, E319, E108, E106, E325, E327, E323, E331, E330, E326, E322, E333, E321, E328, E335, E332, E334, E329, E107), load on request
enough when:  top option >= 35% (lower quartile over 88 visits) or >= 9 points ahead; median 9 checks
come back:    after '4+ scored steps without a new best' (4/6); after '3 scored steps without a new best' (1/6); after 'after a new best' (1/6)  [6 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 72% of visits
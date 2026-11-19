# [Change the training signal › What limits the usefulness of the current labeled training signal?]   98 visits, 13 experts

options: Change training examples (22) | Change target construction (7) | Change training augmentation (4)

check first: E101 Data quantity, label quality, duplication, or imbalance is the observed limitation.  imp 0.90 → +Change training examples  [first in 71/71 visits that checked it]
then:        E102 Censoring or evaluation-group fairness is not represented appropriately by the current target.  imp 0.80 → +Change target construction  [first in 11/13 visits that checked it]
then:        E103 Training overfits despite plausible label-preserving input perturbations being available.  imp 0.85 → +Change training augmentation  [first in 4/4 visits that checked it]
more:         1 further checks (E282), load on request
enough when:  top option >= 81% (lower quartile over 88 visits) or >= 72 points ahead; median 1 checks
come back:    after 'after a new best' (3/3)  [3 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 98% of visits
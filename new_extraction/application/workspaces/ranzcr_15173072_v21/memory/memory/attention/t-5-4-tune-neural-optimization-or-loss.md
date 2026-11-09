# [Tune neural optimization or loss › Which training change should I test?]   37 visits, 15 experts

options: Tune learning rate (7) | Change optimizer or learning-rate schedule (2) | Change training duration or stages (3) | Change the training objective (8) | Make component training cross-validated (5)

check first: E109 The training loss poorly represents the ranking, distribution, or ordinal evaluation objective.  imp 0.75 → +Change the training objective  [first in 14/18 visits that checked it]
then:        E110 A component lacks consistent fold training or reproducible held-out predictions.  imp 0.60 → +Make component training cross-validated  [first in 6/6 visits that checked it]
then:        E295 The response surface around the current best hyperparameter value has been partially mapped, and small perturbations near it are the natural next step.  imp 0.50 → +Tune learning rate  [first in 3/19 visits that checked it]
more:         8 further checks (E299, E106, E108, E296, E294, E107, E297, E298), load on request
enough when:  top option >= 42% (lower quartile over 37 visits) or >= 23 points ahead; median 3 checks
come back:    after 'after a new best' (2/2)  [2 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 57% of visits
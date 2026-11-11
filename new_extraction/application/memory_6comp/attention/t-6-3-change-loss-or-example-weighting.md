# [Change loss or example weighting › Which training objective better reflects the observed task mismatch?]   40 visits, 9 experts

options: Align or compare loss functions (9) | Tune class or subgroup weights (5)

check first: E109 The current loss does not reflect the task’s ranking, distributional, or ordinal target semantics.  imp 0.55 → +Align or compare loss functions  [first in 25/25 visits that checked it]
then:        E110 Class or subgroup imbalance affects errors under the evaluation metric.  imp 0.60 → +Tune class or subgroup weights  [first in 15/25 visits that checked it]
then:        E277 The expert has already swept the weighting parameter through a wide range and is now narrowing into a fine-grained region near the best-performing value.  imp 0.50 → +Tune class or subgroup weights  [first in 0/26 visits that checked it]
more:         8 further checks (E278, E275, E274, E279, E282, E281, E280, E276), load on request
enough when:  top option >= 53% (lower quartile over 40 visits) or >= 7 points ahead; median 4 checks
come back:    after 'other' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 80% of visits
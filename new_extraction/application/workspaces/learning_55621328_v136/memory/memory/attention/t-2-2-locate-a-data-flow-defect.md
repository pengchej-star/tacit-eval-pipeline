# [Locate a data-flow defect › Where should I check for lost or corrupted signal?]   133 visits, 31 experts

options: Restore row and identifier alignment (6) | Restore missing model contributions (14) | Correct aggregation arithmetic (15) | Trace inputs and prediction signal (28) | Repair invalid numerical values (1) | Correct the custom objective implementation (1)

check first: E37 Model or stage outputs are constant, placeholders, or derived from the wrong dataset.  imp 0.75 → +Trace inputs and prediction signal  [first in 51/72 visits that checked it]
then:        E35 Configured model or fold counts exceed the number of accumulated predictions.  imp 0.82 → +Restore missing model contributions  [first in 35/45 visits that checked it]
then:        E36 The blend magnitude or shape changes unexpectedly with member count.  imp 0.65 → +Correct aggregation arithmetic  [first in 21/39 visits that checked it]
more:         3 further checks (E34, E39, E38), load on request
enough when:  top option >= 32% (lower quartile over 130 visits) or >= 10 points ahead; median 1 checks
come back:    after '4+ scored steps without a new best' (2/9); after 'after a new best' (2/9); after '3 scored steps without a new best' (1/9)  [9 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 76% of visits
# [Replace the learned predictor › Which replacement changes the current predictor most appropriately?]   227 visits, 31 experts

options: Select a compatible trained checkpoint (43) | Choose backbone scale or family (27) | Choose the head change (16) | Switch the boosting implementation or variant (12)

check first: E81 Several compatible training runs or stages exist but have not been compared with one fixed inference path.  imp 0.45 → +Select a compatible trained checkpoint  [first in 155/160 visits that checked it]
then:        E82 Checkpoint-only tuning has stalled and available architectures or pretraining sources offer a different representation.  imp 0.80 → +Choose backbone scale or family  [first in 27/105 visits that checked it]
then:        E84 Tabular features are stable and a different boosting method or interface offers the required optimization controls.  imp 0.85 → +Switch the boosting implementation or variant  [first in 25/58 visits that checked it]
more:         2 further checks (E83, E85), load on request
enough when:  top option >= 44% (lower quartile over 227 visits) or >= 15 points ahead; median 2 checks
come back:    after 'regression after a single change' (3/9); after '4+ scored steps without a new best' (3/9); after 'after a new best' (2/9)  [9 returns, 3 improved the score]

scores: LLM-guessed; top option matches the option taken in 87% of visits
# [Choose backbone scale or family › Should the predictor gain capacity, shrink or change its representation family?]   57 visits, 10 experts

options: Increase backbone capacity (9) | Retain or adopt the smaller backbone (9) | Switch backbone family or pretraining (9)

check first: E78 Larger variants fail to beat the established smaller model under matched evaluation.  imp 0.75 → +Retain or adopt the smaller backbone  [first in 14/28 visits that checked it]
then:        E187 Recent checkpoint swaps within the current backbone have shown score degradation.  imp 0.55 → +Retain or adopt the smaller backbone  [first in 9/48 visits that checked it]
then:        E185 A smaller backbone variant is available and could serve as a useful baseline or ensemble complement.  imp 0.50 → +Retain or adopt the smaller backbone  [first in 9/27 visits that checked it]
more:         18 further checks (E188, E79, E189, E199, E80, E190, E77, E191, E195, E194, E201, E200, E186, E196, E192, E197, E198, E193), load on request
enough when:  top option >= 67% (lower quartile over 57 visits) or >= 40 points ahead; median 8 checks
come back:    after '4+ scored steps without a new best' (3/5); after 'after a new best' (1/5); after 'regression after a single change' (1/5)  [5 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 25% of visits
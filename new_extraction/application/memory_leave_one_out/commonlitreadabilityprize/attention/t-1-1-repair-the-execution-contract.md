# [Repair the execution contract › Which observable failure should be repaired first?]   335 visits, 51 experts

options: Restore sample and feature alignment (9) | Load the matching model and preprocessing artifacts (45) | Repair prediction routing and aggregation (39) | Repair API, dependency and device contracts (37) | Run a small end-to-end diagnostic (24)

check first: E04 A traceback identifies an import, callback signature, dataframe operation or device mismatch.  imp 0.95 → +Repair API, dependency and device contracts  [first in 112/206 visits that checked it]
then:        E02 The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration.  imp 0.90 → +Load the matching model and preprocessing artifacts  [first in 92/128 visits that checked it]
then:        E03 Individual models produce varying outputs but the saved submission is constant, partial or duplicates a member.  imp 0.90 → +Repair prediction routing and aggregation  [first in 56/85 visits that checked it]
more:         2 further checks (E05, E01), load on request
enough when:  top option >= 58% (lower quartile over 334 visits) or >= 37 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (8/29); after 'other' (6/29); after '2 scored steps without a new best' (5/29)  [29 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 73% of visits
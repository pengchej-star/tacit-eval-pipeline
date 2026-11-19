# [Change how representations become predictions › Which head or fusion modification should be compared?]   77 visits, 11 experts

options: Change the prediction head (7) | Change feature pooling (5) | Change active input branches (15) | Change branch fusion (3)

check first: E111 A useful modality is available but absent, or an existing branch has uncertain value.  imp 0.85 → +Change active input branches  [first in 49/49 visits that checked it]
then:        E109 The backbone is strong but the head is minimal or labels may need distinct attention.  imp 0.85 → +Change the prediction head  [first in 13/15 visits that checked it]
then:        E112 Equal-sized branch embeddings are averaged even though their information may be distinct.  imp 0.70 → +Change branch fusion  [first in 5/6 visits that checked it]
more:         8 further checks (E336, E110, E340, E341, E338, E113, E337, E339), load on request
enough when:  top option >= 51% (lower quartile over 77 visits) or >= 28 points ahead; median 3 checks
come back:    after 'after a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 94% of visits
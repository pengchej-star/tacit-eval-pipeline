# [Repair silent data flow › Where does the first incorrect intermediate output occur?]   119 visits, 31 experts

options: Align rows and feature columns (5) | Correct ensemble arithmetic and routing (26) | Correct feature and tensor computation (24) | Repair output semantics and export (13)

check first: E06 The first divergent value appears inside feature construction or the model forward pass.  imp 0.72 → +Correct feature and tensor computation  [first in 46/52 visits that checked it]
then:        E05 Some enabled models are skipped, repeated, or assigned the wrong fold or weight.  imp 0.78 → +Correct ensemble arithmetic and routing  [first in 31/37 visits that checked it]
then:        E07 Internal predictions are plausible but the exported values, sign, or schema are wrong.  imp 0.88 → +Repair output semantics and export  [first in 18/26 visits that checked it]
more:         7 further checks (E04, E134, E135, E130, E131, E133, E132), load on request
enough when:  top option >= 41% (lower quartile over 119 visits) or >= 14 points ahead; median 1 checks
come back:    after '4+ scored steps without a new best' (3/8); after 'other' (2/8); after '2 scored steps without a new best' (1/8)  [8 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 78% of visits
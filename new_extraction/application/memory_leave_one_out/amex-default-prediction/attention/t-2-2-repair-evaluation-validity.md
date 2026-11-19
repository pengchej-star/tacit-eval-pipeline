# [Repair evaluation validity › Which source of misleading validation needs correction?]   49 visits, 8 experts

options: Remove label leakage (2) | Align out-of-fold predictions (3) | Check validation credibility (9)

check first: E34 Local model rankings disagree with earlier external results or the public evaluation set is tiny.  imp 0.75 → +Check validation credibility  [first in 30/35 visits that checked it]
then:        E241 The practitioner lacks a proper offline validation setup and is using indirect proxies (filenames, LB submissions) to rank models.  imp 0.85 → +Check validation credibility  [first in 9/42 visits that checked it]
then:        E32 A training feature uses held-out labels or predictions made on its own training rows.  imp 0.90 → +Remove label leakage  [first in 6/7 visits that checked it]
more:         4 further checks (E33, E35, E240, E242), load on request
enough when:  top option >= 79% (lower quartile over 49 visits) or >= 69 points ahead; median 2 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 94% of visits
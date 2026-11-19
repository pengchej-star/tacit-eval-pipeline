# [Repair incorrect predictions › Which failure mechanism should be repaired first?]   281 visits, 44 experts

options: Repair row and feature alignment (12) | Restore checkpoint compatibility (26) | Correct aggregation arithmetic (15) | Repair output semantics and submission wiring (12) | Correct API and dependency failures (29) | Trace the active inference path (40)

check first: E13 Execution stops at an import, file access, device operation, or library call.  imp 0.88 → +Correct API and dependency failures  [first in 89/168 visits that checked it]
then:        E14 Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.  imp 0.90 → +Trace the active inference path  [first in 59/128 visits that checked it]
then:        E10 A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences.  imp 0.75 → +Restore checkpoint compatibility  [first in 51/74 visits that checked it]
more:         3 further checks (E11, E09, E12), load on request
enough when:  top option >= 42% (lower quartile over 279 visits) or >= 19 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (8/32); after 'other' (8/32); after 'regression after a single change' (7/32)  [32 returns, 9 improved the score]

scores: LLM-guessed; top option matches the option taken in 70% of visits
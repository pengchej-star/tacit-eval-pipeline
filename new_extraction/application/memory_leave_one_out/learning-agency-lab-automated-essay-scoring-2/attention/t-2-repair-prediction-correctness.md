# [Repair prediction correctness › Where is there direct evidence that the prediction pipeline is wrong?]   408 visits, 51 experts

options: Repair artifact loading (32) | Repair data and output flow (76) | Repair prediction semantics (23) | Restore a valid end-to-end run (60)

check first: E29 The model runs but rows, features, or executed branches do not match the intended pipeline.  imp 0.85 → +Repair data and output flow  [first in 102/158 visits that checked it]
then:        E28 Failures begin at import, checkpoint resolution, or state loading.  imp 0.90 → +Repair artifact loading  [first in 79/214 visits that checked it]
then:        E31 No usable final output exists or accumulated patches obstruct basic execution.  imp 0.90 → +Restore a valid end-to-end run  [first in 78/220 visits that checked it]
more:         3 further checks (E206, E30, E207), load on request
enough when:  top option >= 52% (lower quartile over 403 visits) or >= 16 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (10/39); after 'regression after a single change' (8/39); after 'other' (8/39)  [39 returns, 5 improved the score]

scores: LLM-guessed; top option matches the option taken in 76% of visits
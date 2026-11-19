# [Change inference averaging › Which inference-pass policy fits the task and current stochastic behavior?]   55 visits, 12 experts

options: Compare valid test-time views (22) | Trial stochastic dropout inference (2) | Make inference deterministic (8)

check first: E181 The task has label-preserving transformations represented by the trained model.  imp 0.85 → +Compare valid test-time views  [first in 28/34 visits that checked it]
then:        E183 Repeated inference changes scores unexpectedly or dropout settings are being tuned while inactive.  imp 0.70 → +Trial stochastic dropout inference  [first in 16/22 visits that checked it]
then:        E336 TTA (e.g., horizontal flip) has shown limited or diminishing marginal gain on recent checkpoints/ensemble compositions, suggesting limited remaining headroom.  imp 0.55 → -Compare valid test-time views  [first in 5/31 visits that checked it]
more:         13 further checks (E338, E182, E344, E347, E345, E348, E343, E341, E340, E342, E346, E337, E339), load on request
enough when:  top option >= 49% (lower quartile over 55 visits) or >= 13 points ahead; median 6 checks
come back:    after 'after a new best' (2/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 64% of visits
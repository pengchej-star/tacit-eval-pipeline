# [Choose repeated inference views › Which label-preserving inference variation is supported?]   53 visits, 10 experts

options: Average deterministic symmetry views (18) | Average crops or resolutions (3) | Average stochastic inference passes (7) | Average model weights (1)

check first: E76 A known spatial or channel symmetry preserves the target.  imp 0.95 → +Average deterministic symmetry views  [first in 33/39 visits that checked it]
then:        E77 Several crops or resolutions retain complementary labeled content.  imp 0.85 → +Average crops or resolutions  [first in 7/14 visits that checked it]
then:        E179 Disabling a currently-enabled TTA is a valid ablation to isolate its contribution to the current setup.  imp 0.45 → +Average stochastic inference passes  [first in 4/31 visits that checked it]
more:         10 further checks (E78, E175, E183, E177, E178, E176, E182, E181, E79, E180), load on request
enough when:  top option >= 55% (lower quartile over 53 visits) or >= 34 points ahead; median 6 checks
come back:    after 'regression after a single change' (1/1)  [1 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 81% of visits
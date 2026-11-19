# [Choose a diagnostic comparison › Which comparison resolves the current uncertainty?]   708 visits, 56 experts

options: Run a controlled ablation (108) | Estimate repeatability (62) | Restore the last verified configuration (36) | Stop a saturated local search (28) | Establish a complete baseline (4) | Bracket a scalar search (6) | Check validation ranking credibility (3) | Replace a weak baseline with a coherent pipeline (1)

check first: E22 Several factors changed in the same scored run.  imp 0.85 → +Run a controlled ablation  [first in 396/689 visits that checked it]
then:        E23 Observed gains are comparable to prior run-to-run variation or the evaluation set is very small.  imp 0.65 → +Estimate repeatability  [first in 198/448 visits that checked it]
then:        E24 A recent change caused a large regression and a verified earlier configuration is recoverable.  imp 0.80 → +Restore the last verified configuration  [first in 62/562 visits that checked it]
more:         5 further checks (E25, E26, E28, E27, E29), load on request
enough when:  top option >= 37% (lower quartile over 708 visits) or >= 12 points ahead; median 4 checks
come back:    after 'after a new best' (12/39); after '4+ scored steps without a new best' (8/39); after 'regression after a single change' (8/39)  [39 returns, 9 improved the score]

scores: LLM-guessed; top option matches the option taken in 51% of visits
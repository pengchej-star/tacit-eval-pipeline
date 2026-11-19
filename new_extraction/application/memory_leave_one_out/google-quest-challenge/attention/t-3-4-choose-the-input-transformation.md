# [Choose the input transformation › Which transformation should change while the model configuration is held fixed?]   179 visits, 22 experts

options: Restore training preprocessing (30) | Sweep image resolution (9) | Adjust text cleaning and formatting (9) | Change imputation or numeric scaling (8) | Tune spectral extraction (13) | Tune temporal or spatial coverage (9) | Adjust signal filtering (4)

check first: E58 Inference transforms differ from those used to train the loaded checkpoint.  imp 0.92 → +Restore training preprocessing  [first in 73/96 visits that checked it]
then:        E62 Spectrograms lose relevant detail or their dynamic range is dominated by artifacts.  imp 0.85 → +Tune spectral extraction  [first in 24/52 visits that checked it]
then:        E59 Image detail is lost at the current resolution or nearby compatible sizes remain untested.  imp 0.80 → +Sweep image resolution  [first in 17/35 visits that checked it]
more:         20 further checks (E63, E60, E61, E179, E64, E176, E173, E165, E168, E164, E170, E171, E169, E175, E177, E166, E172, E167, E174, E178), load on request
enough when:  top option >= 38% (lower quartile over 178 visits) or >= 14 points ahead; median 7 checks
come back:    after 'regression after a single change' (7/15); after 'other' (4/15); after 'after a new best' (3/15)  [15 returns, 6 improved the score]

scores: LLM-guessed; top option matches the option taken in 73% of visits
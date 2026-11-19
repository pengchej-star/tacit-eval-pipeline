# [Map outputs to discrete targets › Which discretization rule should convert the continuous predictions?]   80 visits, 10 experts

options: Optimize global thresholds (26) | Match a supported label distribution (5) | Use group or target-specific cutpoints (5) | Handle degenerate ties explicitly (5)

check first: E83 Labels are ordered discrete values and continuous errors cross meaningful class boundaries.  imp 0.72 → +Optimize global thresholds  [first in 76/80 visits that checked it]
then:        E86 Binning creates constant predictions or many ties in columns scored by a rank metric.  imp 0.60 → +Handle degenerate ties explicitly  [first in 4/25 visits that checked it]
then:        E84 Held-out and expected test label frequencies are stable enough to justify a distribution constraint.  imp 0.65 → +Match a supported label distribution  [first in 0/25 visits that checked it]
more:         1 further checks (E85), load on request
enough when:  top option >= 37% (lower quartile over 80 visits) or >= 9 points ahead; median 2 checks
come back:    after 'regression after a single change' (2/4); after '4+ scored steps without a new best' (1/4); after 'after a new best' (1/4)  [4 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 56% of visits
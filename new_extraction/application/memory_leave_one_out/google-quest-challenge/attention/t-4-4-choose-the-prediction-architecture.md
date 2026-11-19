# [Choose the prediction architecture › How should the representation be converted into predictions?]   42 visits, 10 experts

options: Enrich pooling or attention (11) | Simplify the prediction head (2) | Add auxiliary or ordinal outputs (5) | Fuse complementary branch embeddings (5)

check first: E72 The current pooling or linear head discards useful spatial, temporal, or hidden-layer information.  imp 0.85 → +Enrich pooling or attention  [first in 22/23 visits that checked it]
then:        E75 Multiple aligned input branches provide complementary representations.  imp 0.75 → +Fuse complementary branch embeddings  [first in 8/10 visits that checked it]
then:        E74 Targets are ordered, bounded, or have a useful auxiliary labeling formulation.  imp 0.70 → +Add auxiliary or ordinal outputs  [first in 7/11 visits that checked it]
more:         4 further checks (E73, E180, E182, E181), load on request
enough when:  top option >= 49% (lower quartile over 42 visits) or >= 20 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (2/3); after 'regression after a single change' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 76% of visits
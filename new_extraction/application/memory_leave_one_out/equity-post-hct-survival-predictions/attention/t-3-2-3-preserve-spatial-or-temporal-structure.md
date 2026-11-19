# [Preserve spatial or temporal structure › Which aspect of the spatial or temporal input should change?]   158 visits, 13 experts

options: Change image resolution (11) | Change temporal window or spatial crop (8) | Change time-frequency representation (12) | Change filtering or normalization (10) | Change modalities or channel layout (21)

check first: E42 Unused channels or modalities contain potentially complementary information, or existing branches may be redundant.  imp 0.90 → +Change modalities or channel layout  [first in 64/76 visits that checked it]
then:        E40 Relevant frequency structure is unresolved or blurred by the current transform.  imp 0.70 → +Change time-frequency representation  [first in 30/59 visits that checked it]
then:        E38 Discriminative image detail is lost at the current resolution and the checkpoint supports another size.  imp 0.85 → +Change image resolution  [first in 24/34 visits that checked it]
more:         2 further checks (E39, E41), load on request
enough when:  top option >= 48% (lower quartile over 158 visits) or >= 30 points ahead; median 1 checks
come back:    after 'after a new best' (4/11); after 'other' (2/11); after '4+ scored steps without a new best' (2/11)  [11 returns, 2 improved the score]

scores: LLM-guessed; top option matches the option taken in 91% of visits
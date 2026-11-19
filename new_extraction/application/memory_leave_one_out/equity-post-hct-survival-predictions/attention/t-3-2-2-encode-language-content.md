# [Encode language content › Which text representation should be added or substituted?]   174 visits, 18 experts

options: Change text preparation (15) | Use lexical or latent text features (5) | Use structural and linguistic features (18) | Use frozen pretrained embeddings (18) | Use cross-fitted prediction features (12)

check first: E35 The target depends on document structure or language quality not explicitly represented.  imp 0.85 → +Use structural and linguistic features  [first in 48/62 visits that checked it]
then:        E33 Current text preparation removes informative formatting, truncates relevant text, or introduces inconsistent metadata.  imp 0.60 → +Change text preparation  [first in 44/46 visits that checked it]
then:        E36 The current features lack contextual semantics and suitable pretrained encoders are available.  imp 0.75 → +Use frozen pretrained embeddings  [first in 40/59 visits that checked it]
more:         2 further checks (E37, E34), load on request
enough when:  top option >= 45% (lower quartile over 173 visits) or >= 30 points ahead; median 1 checks
come back:    after 'after a new best' (4/7); after '4+ scored steps without a new best' (1/7); after 'regression after a bundled change' (1/7)  [7 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 88% of visits
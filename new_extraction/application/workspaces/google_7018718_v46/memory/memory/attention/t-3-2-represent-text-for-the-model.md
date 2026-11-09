# [Represent text for the model › Which text representation should I test next?]   129 visits, 15 experts

options: Change text normalization (7) | Change text input structure (5) | Tune sparse n-gram features (3) | Add linguistic or structural statistics (11) | Add pretrained dense representations (13) | Add similarity or auxiliary-task features (7)

check first: E58 Text quality or document organization is relevant but absent from current features.  imp 0.60 → +Add linguistic or structural statistics  [first in 44/64 visits that checked it]
then:        E59 Current features capture counts but lack semantic information.  imp 0.80 → +Add pretrained dense representations  [first in 24/69 visits that checked it]
then:        E55 Cleaning may remove meaningful punctuation, spelling, or pretrained-tokenizer cues.  imp 0.72 → +Change text normalization  [first in 23/27 visits that checked it]
more:         3 further checks (E56, E57, E60), load on request
enough when:  top option >= 33% (lower quartile over 127 visits) or >= 10 points ahead; median 1 checks
come back:    after 'after a new best' (2/5); after '4+ scored steps without a new best' (2/5); after 'regression after a bundled change' (1/5)  [5 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 77% of visits
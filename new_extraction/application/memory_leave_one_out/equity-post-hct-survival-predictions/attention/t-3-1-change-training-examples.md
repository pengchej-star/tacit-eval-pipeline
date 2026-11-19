# [Change training examples › How should the training sample population change?]   96 visits, 12 experts

options: Filter or deduplicate examples (6) | Reweight observed examples (7) | Generate synthetic training examples (4) | Add auxiliary labeled examples (4) | Use pseudo-labeled examples (4) | Alter training augmentation (5)

check first: E24 Rare labels or the test-like subgroup receive little influence under the current loss.  imp 0.72 → +Reweight observed examples  [first in 35/46 visits that checked it]
then:        E23 Training includes duplicates, overlapping windows, low-confidence labels, or a mismatched source.  imp 0.75 → +Filter or deduplicate examples  [first in 16/28 visits that checked it]
then:        E28 Training overfits and label-preserving perturbations are supported by the input semantics.  imp 0.65 → +Alter training augmentation  [first in 15/20 visits that checked it]
more:         5 further checks (E26, E27, E151, E152, E25), load on request
enough when:  top option >= 29% (lower quartile over 96 visits) or >= 10 points ahead; median 2 checks
come back:    after 'after a new best' (2/4); after '4+ scored steps without a new best' (1/4); after 'regression after a bundled change' (1/4)  [4 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 64% of visits
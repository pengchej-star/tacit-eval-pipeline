# [Change what the text encoder sees › Which text-input modification is warranted by the observed examples?]   35 visits, 8 experts

options: Test text cleaning against raw text (7) | Use compatible tokenization (2) | Adjust sequence truncation (1) | Change the encoded text context (5)

check first: E290 A previous version without this text cleaning scored higher than the version with it, suggesting the preprocessing hurts performance.  imp 0.60 → +Test text cleaning against raw text  [first in 9/17 visits that checked it]
then:        E76 Distinct text fields or task metadata are available but omitted from the encoded context.  imp 0.85 → +Change the encoded text context  [first in 7/9 visits that checked it]
then:        E288 A previous implementation of this text-input modification had a code bug that prevented proper evaluation of the idea.  imp 0.65 → +Test text cleaning against raw text  [first in 5/12 visits that checked it]
more:         8 further checks (E291, E292, E74, E73, E289, E75, E77, E293), load on request
enough when:  top option >= 38% (lower quartile over 34 visits) or >= 9 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (2/3); after 'after a new best' (1/3)  [3 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 82% of visits
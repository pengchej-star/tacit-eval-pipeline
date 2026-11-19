# [Repair the prediction path › Which observed failure should I repair first?]   386 visits, 50 experts

options: Restore model compatibility (75) | Repair silent data flow (68) | Isolate the first failing component (34)

check first: E09 The notebook runs but produces implausible, missing, or invariant predictions.  imp 0.65 → +Repair silent data flow  [first in 149/228 visits that checked it]
then:        E08 Failure begins when loading a new artifact or moving to another environment.  imp 0.72 → +Restore model compatibility  [first in 104/141 visits that checked it]
then:        E10 Several new components have never completed an end-to-end run.  imp 0.68 → +Isolate the first failing component  [first in 70/181 visits that checked it]
more:         17 further checks (E109, E110, E112, E117, E111, E115, E107, E113, E120, E121, E114, E119, E122, E108, E118, E116, E123), load on request
enough when:  top option >= 53% (lower quartile over 383 visits) or >= 18 points ahead; median 3 checks
come back:    after '4+ scored steps without a new best' (11/32); after 'other' (8/32); after '2 scored steps without a new best' (5/32)  [32 returns, 4 improved the score]

scores: LLM-guessed; top option matches the option taken in 64% of visits
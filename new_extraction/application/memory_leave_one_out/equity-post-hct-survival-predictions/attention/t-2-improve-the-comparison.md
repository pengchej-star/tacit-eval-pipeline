# [Improve the comparison › What prevents the next experiment from identifying a real improvement?]   824 visits, 54 experts

options: Separate competing explanations (271) | Choose validation membership (18) | Use the actual evaluation metric (14) | Check validation-to-test agreement (2)

check first: E19 Recent score changes cannot be attributed to a single change or exceed neither repeat noise nor a plateau.  imp 0.55 → +Separate competing explanations  [first in 751/764 visits that checked it]
then:        E140 The pipeline contains a runtime error (undefined variable, argument mismatch, missing import, or broken reference) that prevents training or inference from completing.  imp 0.45 → -Separate competing explanations  [first in 26/495 visits that checked it]
then:        E20 The current validation partition leaks related examples or misrepresents the test population.  imp 0.85 → +Choose validation membership  [first in 18/52 visits that checked it]
more:         8 further checks (E21, E22, E139, E136, E138, E141, E142, E137), load on request
enough when:  top option >= 32% (lower quartile over 823 visits) or >= 9 points ahead; median 2 checks
come back:    after '4+ scored steps without a new best' (4/11); after 'other' (3/11); after 'after a new best' (2/11)  [11 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 79% of visits
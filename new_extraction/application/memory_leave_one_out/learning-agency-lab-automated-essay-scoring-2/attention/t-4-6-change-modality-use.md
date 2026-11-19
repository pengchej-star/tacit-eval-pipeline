# [Change modality use › What should change in how input branches supply information?]   56 visits, 6 experts

options: Add derived input channels (4) | Add a complementary model branch (5) | Remove or restore an input branch (7) | Compare concatenation with averaging (5)

check first: E98 A different modality or representation carries information the current branch cannot see.  imp 0.75 → +Add a complementary model branch  [first in 18/24 visits that checked it]
then:        E279 A full-modality baseline score exists to compare the ablation against.  imp 0.40 → +Remove or restore an input branch  [first in 14/55 visits that checked it]
then:        E97 Useful channels are available in the same signal but excluded from the current tensor.  imp 0.85 → +Add derived input channels  [first in 9/10 visits that checked it]
more:         9 further checks (E99, E100, E278, E275, E277, E280, E274, E281, E276), load on request
enough when:  top option >= 39% (lower quartile over 55 visits) or >= 15 points ahead; median 3 checks
come back:    after 'other' (1/4); after '4+ scored steps without a new best' (1/4); after 'regression after a single change' (1/4)  [4 returns, 1 improved the score]

scores: LLM-guessed; top option matches the option taken in 71% of visits
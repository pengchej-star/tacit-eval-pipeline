# [Choose the head change › Should the head be enriched, simplified or changed to fuse inputs?]   35 visits, 7 experts

options: Change the prediction head or feature fusion (10) | Simplify the prediction head (2) | Change how modality embeddings are fused (4)

check first: E73 A strong backbone is followed by only a minimal pooled linear head.  imp 0.75 → +Change the prediction head or feature fusion  [first in 11/17 visits that checked it]
then:        E75 Multiple modality embeddings are available but their current combination discards distinct information.  imp 0.70 → +Change how modality embeddings are fused  [first in 9/15 visits that checked it]
then:        E74 Separate heads or extra normalization layers underperform a simpler shared head.  imp 0.82 → +Simplify the prediction head  [first in 7/8 visits that checked it]
more:         7 further checks (E202, E76, E203, E207, E205, E204, E206), load on request
enough when:  top option >= 52% (lower quartile over 35 visits) or >= 16 points ahead; median 4 checks
come back:    after 'regression after a single change' (1/2); after 'after a new best' (1/2)  [2 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 66% of visits
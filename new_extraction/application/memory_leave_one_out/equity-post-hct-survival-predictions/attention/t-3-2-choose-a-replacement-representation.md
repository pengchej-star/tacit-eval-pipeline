# [Choose a replacement representation › Which representation should I test for the missing signal?]   409 visits, 36 experts

options: Summarize repeated observations (25) | Encode language content (68) | Preserve spatial or temporal structure (62)

check first: E44 The task is driven by text and the current representation misses lexical, semantic, or structural information.  imp 0.90 → +Encode language content  [first in 161/406 visits that checked it]
then:        E45 The input is an image, signal, or spectrogram whose spatial or temporal representation is configurable.  imp 0.85 → +Preserve spatial or temporal structure  [first in 159/408 visits that checked it]
then:        E43 The raw input consists of repeated numeric or categorical observations per entity.  imp 0.90 → +Summarize repeated observations  [first in 88/262 visits that checked it]
more:         1 further checks (E153), load on request
enough when:  top option >= 87% (lower quartile over 409 visits) or >= 74 points ahead; median 3 checks
come back:    after 'after a new best' (1/1)  [1 returns, 0 improved the score]

scores: LLM-guessed; top option matches the option taken in 99% of visits
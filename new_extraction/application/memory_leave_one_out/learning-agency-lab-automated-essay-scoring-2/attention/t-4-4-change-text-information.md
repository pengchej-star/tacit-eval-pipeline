# [Change text information › What text information or formatting should be changed?]   15 visits, 7 experts

options: Change retained text context (2) | Remove harmful custom cleaning (2) | Change text-stream structure (2) | Append structured text metadata (2)

check first: E85 Relevant text lies outside the retained token range or is diluted by unrelated spans.  imp 0.92 → +Change retained text context  [first in 5/6 visits that checked it]
then:        E86 Custom normalization changes text beyond the tokenizer’s training assumptions.  imp 0.75 → +Remove harmful custom cleaning  [first in 3/5 visits that checked it]
then:        E87 Distinct text fields are flattened together despite different roles in the target.  imp 0.82 → +Change text-stream structure  [first in 3/3 visits that checked it]
more:         2 further checks (E269, E88), load on request
enough when:  top option >= 50% (lower quartile over 15 visits) or >= 25 points ahead; median 1 checks
come back:    no returns observed

scores: LLM-guessed; top option matches the option taken in 93% of visits
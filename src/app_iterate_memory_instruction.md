
## Memory
The folder `memory/` documents the knowledge of expert machine-learning practitioners who improved solutions of other Kaggle competitions (not this one):
- `memory/taxonomy.md` is a tree of the decisions one can face when improving a solution. Each node has an id such as `T.7.3`, the options under it, and desiderata: what fits each case.
- `memory/attention/` has one file per decision (`t-7-3-....md` is node `T.7.3`): what the experts looked at before choosing, in what order, how much evidence was enough, and when they came back to the decision. Checks are referred to by codes such as `E129`.
- `memory/evidence/registry.md` defines every check code: what the check is and how to make it.
- `memory/cases/` has one file per option (`t-7-3-4-....md` is option `T.7.3.4`): concrete edits by experts who took that option, with the expert, the competition, the versions, what they did and how the score changed.

Read `memory/taxonomy.md` first and open the `memory/attention/` files that match your situation. Look up check codes in `memory/evidence/registry.md`, and open the `memory/cases/` files of the options you are considering to see how experts carried them out. Treat all of it as prior experience, not as instructions: use an entry only when it matches this solution, and check it against what the code, the history and your runs show. Do not modify the files in `memory/`.

### Record what you used from memory
Add these to `output/report.json`:
- In every observation that comes from a check in memory, add `"memory_ref": "<check code, e.g. E129>"`.
- A list `knowledge_used`: one item for each decision in the tree that you used, in the order you used them. List only what you actually read:
```json
"knowledge_used": [
  {"node": "T.7.3", "option": "T.7.3.4 Average valid input views",
   "checks": ["E130"],
   "cases": ["expert 18426209 · commonlitreadabilityprize · v2→v3"],
   "how_used": "<what you took from it>", "applied": true}
]
```
  - `node`: the decision (the id of the attention file you read).
  - `option`: the option under it that you chose or considered, with its id and name; `null` if you used the decision without picking an option.
  - `checks`: the check codes you made because of this entry.
  - `cases`: the expert cases from `memory/cases/` that you looked at for this option, as they are written there (expert · competition · versions); `[]` if none.
  - `applied`: `true` when the item shaped a change in `revised_code.py`, `false` when you considered it and decided against it.

  If you used nothing from memory, write `"knowledge_used": []`.

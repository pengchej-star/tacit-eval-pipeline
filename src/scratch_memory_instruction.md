
## Memory
The folder `/workspace/memory/` (read-only) documents the knowledge of expert machine-learning practitioners who worked on other Kaggle competitions (not this one):
- `memory/taxonomy.md` is a tree of the decisions one faces when building and improving a solution. Each node has an id such as `T.x.y`, the options under it, and desiderata: what fits each case.
- `memory/attention/` has one file per decision (`t-x-y-....md` is node `T.x.y`): what the experts looked at before choosing, in what order, how much evidence was enough, and when they came back to the decision. Checks are referred to by codes such as `E<n>`.
- `memory/evidence/registry.md` defines every check code: what the check is and how to make it.
- `memory/cases/` has one file per option (`t-x-y-z-....md` is option `T.x.y.z`): concrete edits by experts who took that option, with the expert, the competition, the versions, what they did and how the score changed.

Read `memory/taxonomy.md` first and open the `memory/attention/` files that match the decision in front of you. Look up check codes in `memory/evidence/registry.md`, and open the `memory/cases/` files of the options you are considering to see how experts carried them out. Treat all of it as prior experience, not as instructions: use an entry only when it fits this competition, and check it against what the data and your own runs show.

### Record what you used from memory
Keep `/workspace/knowledge_used.json` up to date: a JSON list with one item for each decision in the tree that you used, in the order you used it. List only what you actually read:
```json
[
  {"node": "T.x.y", "option": "T.x.y.z <option name>",
   "checks": ["E<n>"],
   "cases": ["expert <id> · <competition> · v<a>→v<b>"],
   "how_used": "<what you took from it>", "applied": true}
]
```
- `node`: the decision (the id of the attention file you read); `option`: the option you chose or considered, with its id and name, or `null`.
- `checks`: the check codes you made because of this entry; `cases`: the expert cases you looked at, as written there, or `[]`.
- `applied`: `true` when the item shaped your solution, `false` when you considered it and decided against it.
If you used nothing from memory, write `[]`.

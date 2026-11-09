# Task: build a decision tree of actions, with desiderata, from expert trajectories

## Background
Expert data scientists improved their solutions for machine learning tasks through a series of trials. Their trajectories were cut into *episodes*, and each episode into *items*; each item is one rationale for one change the expert made. Your job is to turn all of these items into a **tree of what one can do to improve the performance of simialr tasks** and, for every decision in that tree, to write the **desiderata**: what a person needs to find out before choosing among the options.

The tree will be used later by an agent that works on a new task. At each decision it will look up the desiderata, go and observe the listed things, and use the answers to pick an option. So the tree must be organised by *decision* (alternatives one chooses between), not by topic.

## Input
`episode_items.jsonl` in the current directory: 856 lines, one episode per line. Each line has:
- `ep_id`, `key_id` (the expert), `comp` (competition), `tier`
- `episode`: `objective`, `lever`, `pattern`, `outcome`, `start_v`, `end_v`, `n_transitions`, `n_scored`
- `items`: a list; the k-th item (counting from 1) has the **item id** `<ep_id>#<k>`, e.g. `13848868:e1#2`. Each item has
  - `instance`: `goal`, `context`, `action` as the expert did it in this competition (specific, with numbers and scores)
  - `general`: the same rationale with the competition removed (`goal` = the question, `context` = when it applies, `action` = what to do)
  - `steps`: the version-to-version edits behind the item

Read the file in pieces or with scripts (python is available); do not try to read it all in one go. No internet access is needed and none should be used. You have no other information about the project; work only from this file.

## What to build

### 1. The tree
- The root is the question "what can I change to improve my solution?". Below it come **decision nodes** (a question, e.g. "How should the validation split be chosen?") whose children are the **options** (alternatives one picks between, e.g. "stratified K-fold" / "group K-fold" / "time-based split"). An option may itself be a decision with its own options. The leaves are **actions**: one concrete, reusable thing to do.
- The similar actions done under similar contexts should be clustered together on the tree, despite their details or expressions are different. Use `general` for clustering; use `instance` as evidence when `general` is vague.
- Children of a decision must be real alternatives (choosing one is a different choice from choosing another), not parts of a sequence and not a topic list.
- Every item must be placed in exactly one leaf. If an item really cannot be placed (for example it is empty or only describes bookkeeping), list it under `unassigned` with a one-line reason. Do not drop items silently and do not assign an item to more than one leaf.
- Names: a decision node gets a `decision` (the question it answers); every node gets a short `name` (what choosing it means) and one-sentence `description`. Write them so that someone who has never seen the data understands them. No competition names or numbers in names; those belong in the evidence.

### 2. The desiderata
For every decision node, write checks.
- A check is a yes/no **statement** about the situation that can be settled **before** choosing, by looking at something the agent can observe (the data, the code, the task description, earlier submissions and their scores, logs and plots).
- Be specific to the decision. Generic checks like "is it worth the cost?" that could sit on any node are not.
- For each check give `how`: the concrete observation that settles it.
- For each check give `pushes`: which child options a YES makes more likely, as `{child id: weight in [-1, 1]}` (negative = less likely). Only list options that really move.
- Base the checks on what the experts in the items actually reacted to (their `context` fields are the best source), supplemented with what is generally needed for the choice.

## Output
Write these files into the directory `output/` (create it) in the current directory:

1. `output/tree.json`, a single JSON object:
```json
{
  "name": ,
  "decision": ,
  "id": "T",
  "children": [
    {
      "id": "T.1",
      "name": "...",
      "description": "...",
      "decision": "...",                // present only if the node has children
      "source": "data",                 // "data" | "prior"
      "children": [ ... ],              // empty list for a leaf
      "items": ["xx", ...]   // item ids; only on leaves
    }
  ],
  "unassigned": [{"item": "<item id>", "reason": "..."}]
}
```
Node ids are `T.<i>.<j>...` following the child position, so they can be referenced from the desiderata. `unassigned` is only at the root.

2. `output/desiderata.json`:
```json
{
  "nodes": {
    "T.1": {
      "groups": [
        {"under": "WHAT FITS THIS CASE?",
         "checks": [{"check": "<yes/no statement>", "how": "<observation>", "pushes": {"T.1.1": 0.8, "T.1.2": -0.5}}]}
      ]
    }
  }
}
```

3. `output/notes.md`: at most one page: how you clustered, what you were unsure about, which decisions you think are poorly defined, and the number of items per top-level branch.

## Before you finish
Write and run a small script that checks `output/`: valid JSON; every item id of the input appears exactly once in the leaves or in `unassigned`; no item id appears that is not in the input; node ids are unique and consistent with the nesting; every node with 2 or more children has desiderata and every id in `pushes` is a child of that node. Fix what it reports. Your final message should only say what you wrote and the counts the check printed (items placed, leaves, decision nodes, checks).

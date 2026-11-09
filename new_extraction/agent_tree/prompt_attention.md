# Task: annotate what experts looked at before each decision and what decision they chose (the "attention map")

## Background
We have a tree of decisions for improving machine-learning solutions. At each decision node, an expert chooses one option. For every decision node there is a list of **checks**: yes/no statements that an expert could settle by looking at some evidence before choosing (the data, earlier submissions and scores, the summaries of earlier changes, and so on).

Each expert submitted many versions of their code for one compitition. Each edit from one version to the next was linked to one or more tree leaves (the *items* of the edit). Each edit is therefore a walk from the root down the tree, and at every decision node on that walk the expert chose one child.

You have the summaries of the changes (not the code) and the leaderboard scores. Your job is to **infer** the attention: at each decision node on each edit's walk, which checks had the expert settled before the edit, with which answer, and in what order. From these annotations you then derive importance weights, "how much evidence is enough" thresholds and "return" patterns.

## Files in the current directory (no other information is available; no internet)
- `jobs.jsonl`: one line per expert edit. Fields: `step_id`, `comp`, `expert`, `tier`, `seq` (version before the edit), `magnitude`, `labels`, `goal`, `change_summary` (what changed; no code), `score_before` (leaderboard score before the edit, may be null), `earlier_edits` (text: this expert's earlier edits, each with goal, change summary and the score after it), and `items`: the intents behind the edit. Each item has `item` (id), `what` (what was done, general wording), `why` (the situation) and `walk`: the decision nodes the edit passes through, root first, each with `node`, `name`, `decision`, `options`, `taken` (the child chosen), `taken_earlier_by_this_expert` (children of this node this expert already took in earlier edits) and `checks` (ids of the checks of this node).
- `desiderata.json`: `checks` (id -> check statement and `how` it is observed) and `nodes` (node id -> groups of check ids, and `guessed_pushes`).
- `tree.json`: the tree (node ids, names, decisions, items on leaves).
- `transitions.json`: per edit of every expert, in order: `step_id`, `key_id`, `comp`, `v_old`, `v_new`, `score_old`, `score_new`, `delta` (positive = improvement for every metric), `new_best`, `magnitude`, `goal`, `change`.
- `competitions.json`: per competition the description of the task and the direction of the metric.

## Step 1: visit records (the inference)
For **every** line of `jobs.jsonl` and for **every** item and every node in its `walk`, produce one **visit** record. For every check of the node decide a state:
- `"yes"` / `"no"`: the expert had enough visible evidence **before** the edit (the task description, the scores and their trend, the summaries of earlier edits, which options were already tried, compute limits seen so far, ...) to settle the statement, and the evidence says yes / no.
- `"not_checked"`: nothing visible shows the expert looked at or could have settled this. This is the default. Do not guess.

Rules:
- Never use the outcome of the edit (the score after it, `delta`, whether it was a new best) as evidence for a check. The change summary may show what the expert looked at or reacted to, but not how it turned out.
- A check must be supported by something in `earlier_edits`, `score_before`, `competitions.json`, or by what the change summary and the item's `what`/`why` show the expert reacted to. Give a short `evidence` (a quote or one sentence) for every yes/no.
- `order`: the plausible order (1, 2, ...) in which the settled checks were looked at at that node; `null` for `not_checked`.
- If the evidence shows that the expert relied on something that **no** listed check of the node captures, record it as a `new_check` of that visit: `{"check": "<yes/no statement specific to this node, observable before choosing, not generic>", "how": "<observation>", "state": "yes|no", "evidence": "...", "order": n}`. Empty is the normal case. After all edits are done, merge the proposals of each node: drop the generic ones, join the ones that mean the same as an existing check or as each other, and add the survivors to the node as new checks with new ids (`N01`, `N02`, ...) in `output/desiderata_extended.json` (same format as `desiderata.json`, with `"origin": "visits"` on the added checks). Then every visit of the nodes that gained checks must be annotated again against the full list so that all visits of a node answer the same checks.

You must make these judgments yourself by reading the text of each edit. Do not replace them by keyword rules, regular expressions or scoring heuristics written in code; code is for splitting the work. The job is large, so work in shards (for example 15 to 25 edits at a time), write each shard's annotations to disk (`work/shard_xxx.json`) as you go so that you can resume, and use parallel sub-agents or workers if you have them. Keep the judging standard the same for all shards: be conservative.

Write `output/visits.json`: a list with one record per (item, node):
```json
{"item": "13848868:e1#2", "step_id": "13848868:1->2", "comp": "...", "expert": "13848868", "tier": "Grandmaster",
 "seq": 1, "node": "T.5.2", "child": "T.5.2.1",
 "checks": {"E17": {"state": "yes", "evidence": "...", "order": 1}, "E18": {"state": "not_checked", "evidence": "", "order": null}},
 "score_old": 0.93, "score_new": 0.94, "delta": 0.01, "effect": "better|worse|flat|unscored",
 "new_best": true, "n_intents": 2}
```
Take `score_old`, `score_new`, `delta`, `new_best` from `transitions.json` (matching `step_id`), `child` = the `taken` of the node, `n_intents` = the number of items of the edit. `effect` is `better` if delta > 1e-4, `worse` if delta < -1e-4, `flat` otherwise and `unscored` if delta is null. Every check of the node (including the added ones) appears in `checks`.

## Step 2: importance and direction of each check
For each decision node with at least one visit, read the node, its options, its checks and at most 10 of its visit records (prefer those with the most checked items), and write for each check an `importance` in [0, 1] (how strongly settling this check decides the choice at this node; 0 = irrelevant) and `pushes`: `{child id: weight in [-1, 1]}`, the direction a YES moves each child (a NO moves it the opposite way). Only list children that really move. Do this as a judgment, not from counts.

Write `output/scores.json`:
```json
{"T.5.2": {"n_visits": 41, "n_experts": 19, "guessed": {"E17": {"importance": 0.7, "pushes": {"T.5.2.1": 0.8, "T.5.2.2": -0.4}}}}}
```
Only checks with importance > 0 and a non-empty `pushes` are listed.

## Step 3: how much evidence is enough, and in what order
Computed with code from steps 5 and 6. For a visit, `z[c] = sum over checked items e (state yes/no) of importance[e] * pushes[e][c] * (+1 if yes, -1 if no)` for each child `c`; the distribution over the children is `softmax(z / 0.5)`. Visits with no scored checked item are not ranked. For each node, `output/enough.json`:
```json
{"T.5.2": {"n_visits": 41, "n_experts": 19, "median_checked": 2.0,
  "enough_top_prob_q25": 0.6, "enough_margin_q25": 0.2, "n_ranked_visits": 30, "top_matches_taken": 0.5,
  "expert_vote_top_prob_q25": 0.55,
  "check_first": [{"check": "E17", "first": 12, "checked": 25}]}}
```
- `median_checked`: median over the node's visits of the number of checks with state yes/no.
- `enough_top_prob_q25`: 25th percentile of the top probability over the ranked visits; `enough_margin_q25`: the same for (top probability minus second probability). Both are `null` if the node has fewer than 4 ranked visits.
- `top_matches_taken`: share of ranked visits where the top child is the `child` taken.
- `expert_vote_top_prob_q25`: first average the top probability per expert, then the 25th percentile over experts; `null` with fewer than 4 experts.
- `check_first`: for each check that was checked at least once, `first` = number of visits where it had the lowest `order`, `checked` = number of visits where it was settled; sorted by `first` descending, then `checked` descending.

## Step 4: returns
A **return** is when an expert comes back to a decision node they had left and takes a child they had passed over: for one expert and one node, sort the visits by the position of the edit in the expert's sequence in `transitions.json`; a visit is a return if (a) the expert took at least one child at this node before, (b) the child taken now is not among the children taken before, and (c) the position gap to the previous visit at that node is more than 1. Record the **trigger**, read off the expert's edits just before the returning edit (the previous edit `prev` in the sequence): 
- `"first step"` if there is no previous edit;
- `"regression after a bundled change"` / `"regression after a single change"` if `prev.delta < -1e-4` (bundled if `prev` had 2 or more items, else single);
- otherwise count the scored edits before this one back to the last `new_best`: if that gap is 2 or more, `"<min(gap,4)>[+ if gap>=4] scored steps without a new best"`;
- `"after a new best"` if `prev.new_best`; otherwise `"other"`.

Write `output/returns.json`:
```json
{"summary": {"total_returns": 0, "experts_with_returns": 0, "triggers": [{"trigger": "...", "n": 0}]},
 "nodes": {"T.5.2": {"n_returns": 0, "triggers": [{"trigger": "...", "n": 0, "share": 0.0}], "n_experts": 0, "improved": 0,
   "returns": [{"expert": "...", "node": "T.5.2", "step_id": "...", "took": "T.5.2.2", "passed_over_for": ["T.5.2.1"], "trigger": "...", "effect": "better", "delta": 0.0}]}}}
```

## Finish
Write `output/notes.md` (at most one page): how you worked, how many edits/visits you annotated, how many new checks you added, where you were unsure, and the share of visits with at least one checked item. Before you finish, run a check script: `visits.json` has one record for every (item, node) of `jobs.jsonl`, all check ids are valid for the node (original or added), states are `yes` / `no` / `not_checked`, every `yes`/`no` has evidence, and the files of steps 6 to 8 are consistent with `visits.json`. Your final message should only say what you wrote and the counts the check printed.

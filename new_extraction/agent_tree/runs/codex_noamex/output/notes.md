# Clustering notes

Read the 770 episodes in indexed batches and manually assigned all 1,498 items by the primary reusable intervention in `general`; consulted `instance` for vague or suspect rationales. Repeated experiments share leaves despite different backbones, scores, or phrasing. Each leaf preserves the original item IDs for evidence lookup. Bundled items have one primary placement, not one copy per mentioned lever.

The tree chooses the **next experiment or repair**. Sibling interventions are alternatives for that next choice, not a prescribed workflow; an agent can revisit another branch afterward. Leaves describe concrete conditional tests rather than treating a trajectory’s winning setting as universal. All populated nodes are data-derived; the exact hierarchy, check wording, and weights are synthesized. Weights are directional heuristics, not fitted probabilities or effect estimates. A negative push does not prohibit an option, and a NO is not automatically the opposite weight.

Uncertainties: coupled edits, inference-only checkpoint swaps, unscored versions, and tiny leaderboard deltas often do not establish causality. Repeated identical submissions estimate execution/artifact variability, not uncertainty from sampling a fixed public test set. Comparisons should use pinned artifacts and representative held-out data. Several accounts conflate rank metrics with calibration: a strictly monotone transform alone cannot improve ranking, although blending, ties, and discretization can change it.

The weakest decisions are coordinated packages versus isolated trials, subgroup-enriched folds, and conditional versus global calibration: the trajectories give limited controlled evidence. Four subgroup-fold items describe overlapping train/validation membership; they remain traceable in the subgroup-fold leaf, whose reusable action requires separate disjoint scoring rather than endorsing leaked CV. The sample-weight item also mentions this rejected evaluation shortcut. Custom objective statistics and target transforms must be fitted without held-out labels. Positive claims about larger models, more folds, extra data, or weaker ensemble members are treated as hypotheses to test. One progress-bar-only item is unassigned.

Items per top-level branch:
- Repair incorrect execution: 197
- Improve the evidence for a change: 283
- Change training evidence: 33
- Change the input representation: 138
- Improve an individual model: 186
- Change how models are combined: 469
- Change inference or final output mapping: 98
- Remove an execution bottleneck: 93

Assigned: 1497; unassigned: 1.

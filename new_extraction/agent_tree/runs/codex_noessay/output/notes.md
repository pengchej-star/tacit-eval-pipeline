# Clustering and interpretation

Read all items through indexed batches of general goals/actions, supplemented by context samples across action clusters and instance evidence for ambiguous cases. Placement follows the principal reusable intervention, not competition, expert, chronology, or incidental code terms. Repeated tests share a leaf even when the winning setting differed. Bundled rationales have one home; their subordinate edits are not duplicated.

The tree chooses the **next intervention**, not a complete workflow: sibling choices are alternative uses of the next experiment. Several may ultimately be useful, but there is no required traversal order. A leaf describes one reusable intervention or controlled comparison, not a claim that it always improves performance. All action leaves have data support; decision wording and diagnostic synthesis are editorial. Positive/negative weights are qualitative routing hints, not fitted probabilities or causal effect sizes. Checks use available data, code, artifacts, or earlier results; missing evidence is not a YES.

Uncertainty is greatest for bundled architecture/preprocessing changes, tiny public-score gains, and unpinned external checkpoints. Identical-code reruns can include artifact changes, so a score shift alone is not proof of stochastic noise. Rank transforms, folds, additional models, filtering, and discretization have conflicting outcomes; the tree retains controlled comparisons and regression paths. Monotone transformations cannot improve a standalone pure rank score without changing ties; their possible effects before blending are different. Local held-out evidence is preferred to repeatedly tuning on a tiny public leaderboard.

The broadest decisions are the root’s bottleneck selection and input-representation selection: independent causes can coexist, so they route the next action rather than identify an exclusive cause. “Recover the last validated configuration” and “Ablate or prune active members” pool many implementations because the decision and context recur. Training-family swaps and coherent multi-change baseline replacements have weaker attribution than single-factor probes. One progress-bar-only item is unassigned as bookkeeping.

## Items per top-level branch

- T.1 — Improve comparison reliability: 217
- T.2 — Repair prediction correctness: 191
- T.3 — Remove execution bottlenecks: 78
- T.4 — Change the input information: 125
- T.5 — Change the training signal: 33
- T.6 — Change the model or fitting procedure: 136
- T.7 — Change prediction combination: 454
- T.8 — Change inference or output adjustment: 77

Total: 1311 placed; 1 unassigned. `validate_output.py` checks exact coverage, structure, references, and check schemas. `build_tree.py` records the reproducible index-to-leaf mapping.

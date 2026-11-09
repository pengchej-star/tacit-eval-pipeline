# Clustering and limitations

Reviewed 856 episodes and 1,674 rationales in bounded batches. Explicit item placements primarily follow `general.goal` and `general.action`, using context and instance evidence for ambiguous or bundled edits. Each item remains intact under its main actionable rationale; leaf IDs reference the original evidence.

The tree selects **the next intervention or controlled experiment**. Siblings are alternative next actions, not a sequence; several may be useful on later visits. Broad routes overlap in applicability. Clusters separate repairs from modeling, replacement from addition, and seed from fold averaging. Unresolved comparisons remain experimental actions, such as comparing rank and raw averaging. All nodes are data-derived; checks supplement observed contexts with methodological requirements. Weights are qualitative directions, not fitted probabilities; omitted pushes assert no effect, and NO does not automatically invert YES.

The least sharply defined decisions are broad intervention routing, mixed-lever experiments, and checkpoint versus membership changes. A separate bundle action preserves coordinated-change rationales without claiming causal attribution. Tiny public leaderboards, nondeterminism, and confounded edits weaken many source conclusions. Repeated items establish recurring practice, not independent proof; strong claims become comparisons requiring held-out evidence.

The subgroup-allocation leaf retains five rationales advocating overlapping training and validation rows. That procedure leaks information: its local scores must not be treated as generalization estimates. The leaf and checks require a separate disjoint evaluation and discourage overlapping allocation. Similarly, tokenizer changes, inference preprocessing changes, rank ties, and output scaling require compatibility and metric checks; source claims about gains are not assumed true.

All items have an actionable rationale, including engineering changes that enable valid performance comparisons; none were discarded as bookkeeping. `validate_output.py` independently checks source coverage, positional IDs, schema, and all decision/check references.

| Top-level choice | Items |
|---|---:|
| T.1 — Improve the evidence for choosing changes | 307 |
| T.2 — Repair incorrect or mismatched predictions | 186 |
| T.3 — Change the information presented to the model | 183 |
| T.4 — Change training examples or targets | 42 |
| T.5 — Change the learned model | 131 |
| T.6 — Change the prediction pool | 360 |
| T.7 — Change prediction combination or output mapping | 309 |
| T.8 — Make useful experiments feasible | 156 |

# Clustering notes

The tree chooses the next intervention, not an entire workflow. Sibling options are alternative experiments or implementations at that point; an agent may return later to choose another intervention. All leaves have input evidence, and all nodes are marked `data`; no unsupported prior-only action branches were added.

Clustering used the generalized goals and actions, with contexts distinguishing superficially similar interventions. I reviewed all item goals in batches, assigned items explicitly, then checked representative full rationales and lexical outliers within clusters. Selected instance records resolved ambiguous cases. Checkpoint replacement, compatibility repair, fold averaging, seed averaging, stochastic inference, and weight averaging remain separate. Compound items belong once to their primary actionable rationale; membership does not claim that the leaf reproduces every edit.

Checks describe observable pre-choice conditions. Their `how` fields point to data, code, artifacts, existing predictions, or trial records. Push weights are directional judgment, not calibrated probabilities or estimated effect sizes. A failed trial supports testing or rejecting an action in context, not a universal performance claim.

The least sharply defined boundaries are component replacement versus membership ablation, representation changes versus model changes, and regression recovery versus controlled experimentation. Broad bundled items are assigned by the dominant action rather than split or duplicated. Many ensemble items rely on noisy leaderboard feedback; repeated scores and local validation are therefore explicit alternatives to further tuning. Source-specific fold manipulation is also uncertain: some instances put rows in both training and validation. Those observations are retained under fold-membership control, but shared rows must not be interpreted as independent held-out evidence.

Three items are unassigned with explicit reasons: preserving a parameter block as comments, removing diagnostic displays, and changing progress-bar rendering. None specifies a modeling, evaluation, or prediction-validity change.

Items per top-level branch (1,550 placed; 3 unassigned):

- T.1 — Repair prediction validity: 255
- T.2 — Improve the evidence for choosing a change: 355
- T.3 — Change examples or supervision: 31
- T.4 — Change the information presented to the model: 178
- T.5 — Change the fitted learner: 95
- T.6 — Change how the model is trained: 72
- T.7 — Change the prediction ensemble: 499
- T.8 — Change prediction decoding or calibration: 65

`validate.py` checks JSON parsing, exact item coverage and uniqueness, positional node IDs, decision/leaf structure, all decision checks, immediate-child push targets, and finite nonzero weights within bounds.

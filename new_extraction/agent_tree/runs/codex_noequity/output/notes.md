# Clustering and limitations

The tree treats each traversal as choosing the **next intervention**; interventions may be combined in later iterations. Its branches are alternatives for the current bottleneck, not a prescribed sequence. I grouped generalized goals, contexts, and actions, then reviewed placements and consulted specific evidence where the generalized question obscured the actual edit. Wording, model names, resolutions, scores, and competition identities do not define clusters.

Each item has one home at its principal reusable action. Bundled rationales remain indivisible: for example, an item changing both resolution and fold count is placed with the principal input-resolution intervention. The leaf description generalizes the action; the linked input item retains the exact experiment and outcome. Repeated rationales remain separate evidence items rather than being deduplicated.

Checks use observable failure signatures, input structure, artifact compatibility, prior ablations, learning curves, or evaluation history. They are statements to settle before selecting a child. Push weights are qualitative routing strengths, not learned probabilities or estimates of improvement. A check may favor several alternatives; a NO does not mechanically negate its weights. All leaves have input evidence.

The least sharply separated choices are checkpoint selection versus ensemble membership, feature extraction versus stacking, and rollback versus fault diagnosis. I distinguished changing one saved predictor from changing the member set; representation features from fitted output combinations; and restoring a baseline from repairing a known defect. Sample filtering and validation-population choices can interact, but are separated by whether training membership or the scored validation population changes.

Many experts relied on small, noisy public evaluations and bundled edits. Their reported improvements are evidence for testing a choice, not proof of a universal winner. The checks therefore include reproducibility, population alignment, and matched comparisons. Validation choices and weight averaging have much thinner evidence than ensemble composition; no time-split or unrelated target-transformation branch was invented to fill gaps.

Two items are unassigned with individual reasons: exploratory profiling without a solution change, and progress-bar display bookkeeping.

| Top-level choice | Items |
|---|---:|
| T.1 — Repair the prediction path | 177 |
| T.2 — Improve the comparison | 305 |
| T.3 — Change the learning information | 235 |
| T.4 — Change the fitted predictor | 167 |
| T.5 — Change how predictors are combined | 408 |
| T.6 — Change prediction interpretation | 58 |
| T.7 — Make a viable experiment cheaper | 115 |

Total: 1,465 placed items; 2 unassigned; 1,467 input items across 743 episodes.

# Clustering and limitations

The input contains 739 episodes and 1,449 items. I inspected the inventory in batches, formed candidate clusters from `general.goal`, `general.action` and `general.context`, then reviewed every item question and corrected assignments; representative full rationales and ambiguous cases were read in detail. Item IDs link back to the original instance evidence. Repeated actions are merged across experts and competitions. Multi-lever items appear once under their primary reusable recommendation, not once per edit.

The root chooses the **next intervention**. Its branches are competing uses of the next trial, not a sequential workflow. Lower decisions choose concrete interventions or policies (for example, native missingness versus imputation, raw versus rank averaging, and equal versus tuned weights). Comparative items that support testing both options are placed under the principal intervention; an assignment does not claim that option won. Checks use observable input structure, saved configurations, prior ablations and score variation. Their signed weights are qualitative routing preferences, not learned probabilities or guarantees. All decisions are grounded in observed choices; any action without supporting items is marked `prior`.

Uncertainty is greatest for checkpoint choice, arbitrary feature additions, preprocessing changes and member/weight searches guided only by public scores. These usually need a controlled local comparison; the file does not establish a universal winner. Several items confound resolution, architecture, fold count or weights, and many infer stochasticity from reruns without proving its source. Some source generalizations overstate causal effects (including monotone scaling on rank-only metrics); the checks preserve metric invariance and require independent evidence. The overlapping-fold diagnostic explicitly retains four problematic source recommendations, but never treats their contaminated validation scores as evidence of generalization: an untouched holdout is required. Population-aware disjoint validation remains a separate option.

One item that only removes diagnostic output is unassigned with a reason. Operational repairs are otherwise retained where they affect correct predictions, reproducibility or feasible experimentation. Broad head/fusion, objective/target and execution-repair decisions remain less sharply defined because some source items bundle interventions.

Items per top-level branch:

- Repair or accelerate execution: 278
- Improve the evidence for choosing changes: 363
- Change the information supplied to learning: 229
- Change how the model is fitted: 77
- Replace the learned predictor: 98
- Combine existing predictions: 324
- Change the final prediction mapping: 79

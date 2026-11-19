# Clustering notes

The tree chooses the **next intervention** at every level. Siblings are competing responses to the current evidence; they need not be incompatible forever. It contains no prescribed workflow sequence. I grouped generalized goals, contexts and actions, consulted instance details for ambiguous items, and assigned each multi-change rationale to its dominant intervention. Failed trials belong to the action they tested, not a separate failure topic. Leaf evidence quotes the input; item IDs link every placement to its complete original rationale.

Checks describe observable conditions before selecting an action. Existing ablations and prediction files can settle them; when that evidence does not exist, the evidence-building branch is the appropriate next choice. Weights are qualitative routing strengths, not estimated probabilities. Negative weights express displacement of sibling choices. Basic validity, leakage and held-out evaluation checks supplement the recorded contexts.

Uncertainty: many trajectories confound checkpoint, preprocessing and blend changes, and often only public scores are available. Those results support experiments, not universal claims that more folds, larger backbones or additional features help. Generic debugging and broad baseline items have less precise causal attribution. Feature-count versus regularization tuning, fold selection versus checkpoint selection, and raw/rank averaging versus output calibration have interacting boundaries; each item nevertheless has exactly one home.

The subgroup-fold construction decision is particularly weak: some experts duplicated rows into training and validation. The leaf preserves that evidence and explicitly calls for a disjoint audit rather than endorsing leakage. Other supplemental checks distinguish target-frequency assumptions, metric-preserving transformations and unbiased stacking from unsupported leaderboard heuristics. No time-based validation branch was invented without trajectory support. Two bookkeeping-only items remain unassigned.

Items by top-level branch:

- Repair the pipeline: 194
- Make comparisons trustworthy: 212
- Change the input signal: 185
- Change the learner or fitting rule: 146
- Combine predictive signals: 337
- Calibrate final outputs: 67
- Make the next experiment feasible: 83

# Construction notes

Clustered all 1,539 rationales from 782 episodes by the intervention proposed in `general.goal`, `general.action`, and the applicable context. Candidate text matches were reviewed by cluster and corrected for misleading vocabulary (for example, an ensemble item whose action repairs row alignment). `instance` and episode evidence resolve ambiguous or bundled edits; item IDs retain the original evidence without copying competition-specific names into nodes. No internet or external project information was used.

The root chooses the next intervention; it is not a sequential workflow. Lower decisions choose competing repairs, representations, split designs, predictors, or aggregation strategies. A sweep or ablation is itself a concrete action when the trajectories do not establish one universally preferred setting. Multi-lever items are assigned once to their principal rationale; secondary levers are intentionally not duplicated. Operational fixes are retained when they enable correct predictions or reliable experiments. All items have a reusable rationale, so unassigned is empty.

Uncertainty: many trials bundle changes, omit local validation, or depend on changing external checkpoints. Reported gains therefore do not establish causality. Items include unsuccessful probes and reversions; leaf membership is evidence of an action, not an endorsement of every conclusion. Checks use observable conditions and prior results, supplemented by prerequisites such as leak-free out-of-fold features and compatible checkpoint inputs. Push weights are qualitative routing preferences, not fitted probabilities or measured effect sizes. All nodes have data support; no prior-only action leaves were needed.

Less sharply defined decisions: broad next-intervention choices are compatible over multiple iterations; member replacement versus checkpoint selection depends on whether the rationale concerns the full blend or one predictor. Validation fold count versus inference fold count, input representation versus model diversity, and calibration versus aggregation sometimes overlap. Recovery is separated from ablation by whether restoring a verified configuration is the main purpose. These are forced single placements, not claims that an item addresses only one lever.

Items per top-level branch:

- T.1 Repair incorrect predictions: 134
- T.2 Improve the experiment evidence: 285
- T.3 Change the information supplied: 254
- T.4 Change the predictor: 93
- T.5 Change how the predictor is fitted: 74
- T.6 Change prediction combination: 520
- T.7 Change the output mapping: 42
- T.8 Change execution to enable useful experiments: 137

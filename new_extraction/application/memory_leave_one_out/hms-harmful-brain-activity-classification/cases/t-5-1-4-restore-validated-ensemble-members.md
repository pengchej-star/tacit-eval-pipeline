# Restore validated ensemble members  `T.5.1.4`   4 edits, 0 experts
4 scored cases (improvement signed by each competition's direction), median +0.00780, 4 improved


- expert 17616127 · commonlitreadabilityprize · v115→v117   Restore the full set of diverse model predictions that were present in the best-scoring configuration, then fine-tune which aggregated prediction (e.g., a meta-learner's output vs. a simple average) occupies each slot in the final weighted blend. This two-step approach—first restore membership, then
    evidence: ✓ Removing or disabling previously validated members caused a regression. | ✓ Several compatible trained checkpoints differ in seed, recipe or training stage.
    leaderboard score 0.45552 → 0.44809 (lower is better; improved by 0.00742)
- expert 17616127 · commonlitreadabilityprize · v139→v141   Restore all previously working component predictions and meta-learner inputs to the last known good configuration before re-attempting any pruning. Ensure the meta-learner aggregation mode (e.g., returning the mean across folds) matches what produced the best prior score. Treat the restored full ens
    evidence: ✓ Removing or disabling previously validated members caused a regression.
    leaderboard score 0.46975 → 0.44790 (lower is better; improved by 0.02184)
- expert 75145694 · equity · v16→v17   Restore all previously contributing members to recover the baseline, then simultaneously add a new diverse model (e.g., a pretrained neural network with different preprocessing) into the blend. This combines recovery with incremental improvement in a single step, and the net gain over the pre-prunin
    evidence: ✓ Removing or disabling previously validated members caused a regression.
    leaderboard score 0.68867 → 0.69070 (higher is better; improved by 0.00203)
- expert 15164527 · ranzcr · v43→v44   Re-enable all verified components simultaneously and combine them with rank-based blending. Expect the reassembled ensemble to exceed the previous best if the new components are genuinely additive, since the debugging phase likely fixed subtle errors that were previously degrading some members' cont
    evidence: ✓ Removing or disabling previously validated members caused a regression.
    leaderboard score 0.96052 → 0.96832 (higher is better; improved by 0.00780)
# Cross-expert knowledge

295 episode-level items from 70 kernels / 7 competitions; 111 rules supported by >= 2 kernels, covering 248 items. Lever vocabulary: 48 categories.

## 1. revert_and_redirect_on_regression  [L3]  —  6 kernels, 4 comps, 6 items

- **Context:** When exploring hyperparameters, model configurations, ensemble member swaps, augmentation strategies, or lever variants and a change produces a score regression compared to the current baseline.
- **Action:** Do not persist with the regressing configuration. Revert the regressing change before trying the next modification. Change only one thing per submission and measure each change against a fixed baseline. Do not stack untested changes—if two things changed and the score dropped, you cannot attribute the cause. Try a different candidate or approach in the next submission. If two or three consecutive attempts from the same lever regress, abandon that lever and switch to a qualitatively different approach (e.g., new model family, different blending method, ensembling, or diagnostic investigation).
- **Exceptions:** 60264017: after second regression the author moved to a new approach rather than reverting and trying another swap, suggesting candidate exhaustion can also trigger stopping. 15372370: author did not submit the intermediate revert, so incremental revert wasn't fully LB-validated. In 29588171, the author failed to revert regressions before trying the next change, making attribution impossible and prolonging the regression. In 28984551, model-family switching only partially recovered; real recovery came from ensembling rather than single-model tuning.
- **Support:** kernels 15372370, 18757376, 27825577, 28984551, 29588171, 60264017; comps amex-default-prediction, commonlitreadabilityprize, learning-agency-lab-automate, ranzcr-clip-catheter-line-cl; tiers {'Expert': 3, 'Contributor': 1, 'Master': 2}; episode reached new best: {'yes': 3, 'no': 3}
- **Cells:** L3/explore/new_idea, L3/explore/regression
- **Examples:**
  - `15372370:e5#1` (ranzcr-clip-catheter, Expert; steps 15372370:9->10, 15372370:10->11): Revert the changes incrementally rather than all at once: remove the most aggressive/novel component first, test, then remove remaining novel components. This isolates which change caused the regression. If the score still hasn't recovered after partial revert, continue removing until you return to baseline behavior.
  - `18757376:e4#1` (commonlitreadability, Expert; steps 18757376:4->5, 18757376:5->6): After a regression from ensemble changes, re-enable previously disabled strong models, disable suspected weak contributors one at a time, and adjust blend weights between raw averaging and stacked predictions. Use OOF RMSE to identify which members to keep. Submit after each change to confirm improvement before making the next.
  - `27825577:e5#2` (amex-default-predict, Expert; steps 27825577:14->15, 27825577:17->18, 27825577:19->20): After two submitted regressions from the same lever, limit further exploration to at most two more unsubmitted CV checks. If no CV improvement is found, abandon the lever and switch to a diagnostic or entirely different approach rather than continuing to permute the same options.
  - `28984551:e3#1` (amex-default-predict, Contributor; steps 28984551:3->4, 28984551:5->6): Try a different model family (e.g., CatBoost vs LightGBM) with comparable regularization settings. If the alternative partially recovers but doesn't beat the original baseline, revert to the original family with a small hyperparameter adjustment. If neither recovers the baseline after 2-3 attempts, stop single-model tuning and move to ensembling.
  - `29588171:e5#1` (amex-default-predict, Master; steps 29588171:36->37, 29588171:38->39, 29588171:39->40): Change only one hyperparameter per submission. If a change regresses, revert it before trying the next parameter. Maintain a fixed baseline configuration and measure each change against it. Do not stack untested changes—if two things changed and the score dropped, you cannot attribute the cause.
  - `60264017:e2#3` (learning-agency-lab-, Master; steps 60264017:2->3, 60264017:3->4, 60264017:5->6): Do not persist with the regressing configuration. Instead, revert the problematic member and try a different candidate in the next submission. If two consecutive swaps regress from the best, stop the membership search and consider a qualitatively different approach (e.g., adding a new model family or changing the blending method).

## 2. stop_sweep_after_bracketing_optimum  [L3]  —  6 kernels, 4 comps, 6 items

- **Context:** When perturbations in both directions of a hyperparameter or knob yield scores worse than or within noise of the current best (a 3-point bracket confirms a local optimum), and 3+ attempts produce scores within a narrow band with no monotonic improvement trend.
- **Action:** Stop tuning that parameter. Accept the best configuration found and pivot to a qualitatively different lever (e.g., feature engineering, model architecture, ensembling, adding new models) rather than continuing to permute the same parameter or refining it with smaller step sizes. Do not continue refining the same parameter unless score differences are within leaderboard noise.
- **Exceptions:** 55431616:e4#2 notes the author combined the revert with new features rather than testing independently.
- **Support:** kernels 27656049, 53762022, 55431616, 58527792, 77276039, 77347591; comps amex-default-prediction, equity-post-hct-survival-pre, hms-harmful-brain-activity-c, learning-agency-lab-automate; tiers {'Expert': 3, 'Contributor': 2, 'Grandmaster': 1}; episode reached new best: {'yes': 1, 'no': 5}
- **Cells:** L3/sweep/new_idea/part1, L3/sweep/new_idea/part2
- **Examples:**
  - `27656049:e8#3` (amex-default-predict, Expert; steps 27656049:26->27): Stop a hyperparameter sweep when you have tested values on both sides of the current best and all score worse. If the differences are within noise (~0.0003 on this metric), accept the best configuration and move to a different lever (e.g., feature engineering or model architecture).
  - `53762022:e7#2` (hms-harmful-brain-ac, Contributor; steps 53762022:14->15, 53762022:15->16, 53762022:16->17): Stop tuning when 3+ attempts produce scores within a narrow band around the best and no monotonic improvement trend is visible. The remaining variation is likely leaderboard noise rather than true signal. Move to a different lever (e.g., adding models, changing architecture) instead.
  - `55431616:e4#2` (learning-agency-lab-, Grandmaster; steps 55431616:14->15, 55431616:15->16): Accept the current parameter value and pivot to a qualitatively different lever (e.g., adding new feature types or changing the model). Do not continue refining the same parameter with smaller steps unless the score differences are very small relative to leaderboard noise.
  - `58527792:e2#1` (learning-agency-lab-, Contributor; steps 58527792:2->3, 58527792:3->4): If a single round-trip perturbation of hyperparameters (increase then revert) fails to improve the score, abandon the hyperparameter sweep and invest effort in a different lever such as adding new features or a different model family. Do not continue exploring nearby values.
  - `77276039:e2#2` (equity-post-hct-surv, Expert; steps 77276039:8->9, 77276039:9->10): If sweeping a single knob across a reasonable range (both directions from baseline) fails to improve the metric, stop tuning that knob. Submit the best configuration as a checkpoint, then pivot to a higher-impact lever such as target transformation, feature engineering, or model architecture changes.
  - `77347591:e9#1` (equity-post-hct-surv, Expert; steps 77347591:22->23, 77347591:23->24, 77347591:24->25, 77347591:25->26): After 3–4 submissions that return effectively the same score (within noise), stop sweeping that lever. The leaderboard resolution cannot distinguish the variants, so further submissions waste budget without information gain. Move to a structurally different lever (new model, new features, new loss) instead.

## 3. stop_sweep_after_consistent_regression  [L3]  —  6 kernels, 4 comps, 6 items

- **Context:** When 3+ submitted attempts along the same lever (e.g., checkpoint swaps, weight variants, architecture changes, feature variants) all regress from or fail to match the baseline, with none matching or exceeding the best score on both CV and LB.
- **Action:** Stop the sweep and change strategy. Revert to the prior best configuration and move to a qualitatively different approach (e.g., ensembling the best configurations, adding new diverse models, different feature family, or changing the lever entirely). Preserve the best-scoring configuration as a component for future use. Do not continue micro-tuning the underperforming idea.
- **Exceptions:** 15082684 author ran 11 swaps instead of stopping at 3, suggesting some practitioners over-explore. 27836972:e9#2 notes that CV scores close to the best may justify a bit more exploration. 55621328:e16#3 notes one large-model variant came close, but the author correctly prioritized the more reliable path.
- **Support:** kernels 13848868, 15082684, 15173072, 27836972, 55621328, 6803050; comps amex-default-prediction, google-quest-challenge, learning-agency-lab-automate, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 1, 'Master': 3, 'Contributor': 1, 'Expert': 1}; episode reached new best: {'no': 4, 'yes': 2}
- **Cells:** L3/sweep/new_idea/part1, L3/sweep/new_idea/part2
- **Examples:**
  - `13848868:e6#3` (ranzcr-clip-catheter, Grandmaster; steps 13848868:27->28): After testing 3 variants of a new component and none comes within ~0.1-0.2% of the baseline, abandon the direction. Do not continue fine-tuning a clearly inferior component; revert to the prior best and try a different lever.
  - `15082684:e2#1` (ranzcr-clip-catheter, Master; steps 15082684:3->4, 15082684:4->5, 15082684:5->6, 15082684:6->7): Submit a handful of checkpoints spanning different training runs and epochs. If none beat the current best after ~5-6 tries and the CV-to-LB correlation appears weak (high CV doesn't yield high LB), stop the sweep and change approach rather than exhaustively testing all checkpoints. Track the best LB explicitly and revert to it before moving on.
  - `15173072:e5#2` (ranzcr-clip-catheter, Contributor; steps 15173072:27->28): Revert to the exact configuration that produced the best score so far, making only minimal simplifications (e.g., cleaner blend formula). Submit to confirm recovery. If the reverted version matches or exceeds the previous best, stop the sweep and move on to a different lever entirely.
  - `27836972:e9#2` (amex-default-predict, Expert; steps 27836972:48->49, 27836972:54->55): After exploring 3-4 meaningfully different configurations of a feature idea without any variant matching or exceeding the baseline on both CV and LB, abandon the idea and move to a structurally different feature engineering approach. Do not keep micro-tuning which columns to include.
  - `55621328:e16#3` (learning-agency-lab-, Master; steps 55621328:40->41, 55621328:41->42, 55621328:42->43, 55621328:44->45): Do not persist with larger models after 2-3 attempts show them underperforming the smaller variant. Return to the smaller model and invest effort in ensembling (more folds, more seeds) rather than scaling up model size. The ensemble of a well-trained smaller model often beats a single larger model.
  - `6803050:e10#2` (google-quest-challen, Master; steps 6803050:41->42, 6803050:47->48, 6803050:48->49): After 3+ submitted attempts that all regress from the baseline along the same lever, stop the sweep and change strategy. Move to a qualitatively different approach such as combining the best configurations via weighted blending rather than continuing to test individual variants. Preserve the best-scoring configuration as a component for future ensembles rather than discarding it.

## 4. ablate_after_bundled_regression  [L3]  —  5 kernels, 5 comps, 5 items

- **Context:** When a commit that introduced multiple changes (new layer/component + hyperparameter change, new data source + config tweak) causes a regression, and you need to identify the culprit.
- **Action:** Revert the most novel or structurally risky component first (e.g., new architectural layer) while keeping the simpler changes (e.g., fold count). If performance recovers, that component was harmful—do not re-introduce it. If it does not fully recover, suspect other concurrent changes. After at most two diagnostic submissions, if baseline is not recovered, revert all bundled changes to restore the known-good baseline and pursue a different lever entirely. Submit only after confirming recovery.
- **Exceptions:** When the regression is tiny (within noise), it may not be worth diagnosing at all—just move on (59253662:e6#2). Partial recovery may indicate multiple interacting causes (77276039:e4#2).
- **Support:** kernels 17371717, 49576186, 59253662, 7240226, 77276039; comps commonlitreadabilityprize, equity-post-hct-survival-pre, google-quest-challenge, hms-harmful-brain-activity-c, learning-agency-lab-automate; tiers {'Master': 1, 'Expert': 2, 'Contributor': 2}; episode reached new best: {'no': 4, 'yes': 1}
- **Cells:** L3/probe/new_idea/part2, L3/probe/new_resource
- **Examples:**
  - `17371717:e3#1` (commonlitreadability, Master; steps 17371717:6->7): Before reverting to the previous best, inspect the new code for initialization bugs and forward-pass logic errors. Fix the most likely issues (e.g., parameter initialization, gradient flow through softmax) and resubmit once. If the fix recovers most of the gap, continue iterating; if not, revert or pivot.
  - `49576186:e24#2` (hms-harmful-brain-ac, Expert; steps 49576186:151->152, 49576186:153->154, 49576186:154->155, 49576186:156->157): After a bundled change regresses, try one more variant that modifies the most suspicious component (here, extra-data filtering). If that also fails, revert all bundled changes to recover the baseline score, then pursue a completely different lever. Do not spend more than two submissions diagnosing a failed bundle.
  - `59253662:e6#2` (learning-agency-lab-, Contributor; steps 59253662:28->29): If a bundled change produces even a small regression and you have alternative ideas, move on rather than debugging which component caused the drop. Time is better spent on orthogonal improvements. Only revisit if you run out of other levers.
  - `7240226:e3#2` (google-quest-challen, Contributor; steps 7240226:8->9, 7240226:9->10): When combining a new layer/component with a hyperparameter change causes a regression, comment out or remove the new component first while keeping other changes. If performance recovers, the component was harmful. Do not re-introduce it. Submit only after confirming recovery.
  - `77276039:e4#2` (equity-post-hct-surv, Expert; steps 77276039:16->17): Remove the most easily toggled recent addition first (e.g., a new ensemble member) and resubmit. If the score partially recovers, confirm that addition was harmful. If it does not fully recover, suspect other concurrent changes and investigate them next.

## 5. ablate_joint_changes_to_isolate_contributions  [L3]  —  5 kernels, 4 comps, 6 items

- **Context:** When a combined change of two or more factors produced a score improvement, but it is unclear which factor contributed, and each submission is cheap enough to test individual reversions.
- **Action:** Revert one variable back to its previous value while keeping the other fixed. If the score stays the same or improves, the reverted variable's new value was unnecessary or harmful. Repeat for the other variable. In subsequent iterations, change only one factor at a time. Do not change multiple factors simultaneously again in the next step. This isolates contributions with minimal submissions.
- **Exceptions:** 7253130:e5#1 notes the author didn't do a clean single-variable ablation. 7018718:e9#1 notes the author sometimes still changed two factors at once.
- **Support:** kernels 15372370, 27656049, 7018718, 7253130, 77129691; comps amex-default-prediction, equity-post-hct-survival-pre, google-quest-challenge, ranzcr-clip-catheter-line-cl; tiers {'Expert': 3, 'Contributor': 2, 'Master': 1}; episode reached new best: {'yes': 5, 'no': 1}
- **Cells:** L3/sweep/new_idea/part1, L3/sweep/new_idea/part2
- **Examples:**
  - `15372370:e3#2` (ranzcr-clip-catheter, Expert; steps 15372370:5->6): When a combined change improves the score, do not simultaneously modify multiple factors in the next iteration. Isolate each factor: first try removing TTA alone, then try changing weights alone. Changing multiple factors at once makes regressions uninterpretable—you cannot tell which change caused the drop.
  - `27656049:e8#2` (amex-default-predict, Expert; steps 27656049:25->26, 27656049:26->27): After a successful multi-parameter change, test individual parameter reversions or perturbations one at a time. If reverting a single parameter hurts, keep the original. If two consecutive single-param changes both regress, the multi-param configuration is likely near a local optimum — stop the sweep.
  - `7018718:e9#1` (google-quest-challen, Expert; steps 7018718:27->28, 7018718:28->29, 7018718:29->30, 7018718:30->31): After a new best from a combined change, isolate factors by first testing a different checkpoint with preprocessing disabled, then re-enable preprocessing options one at a time. If no combination beats the original, stop after 3-4 attempts and try a different lever entirely. Always submit each variant to get leaderboard signal.
  - `7253130:e2#2` (google-quest-challen, Contributor; steps 7253130:4->5): After a joint change improves the score, revert one variable back to its previous value while keeping the other fixed. If the score stays the same or improves, the reverted variable's new value was unnecessary or harmful. Repeat for the other variable if needed. This isolates contributions with minimal submissions.
  - `7253130:e5#1` (google-quest-challen, Contributor; steps 7253130:10->11, 7253130:11->12): Partially revert one or both changes toward their previous values to isolate which change drove the improvement. If the partial revert hurts, restore the better-performing combination and vary a different lever. Use the regression as evidence for which setting to keep.
  - `77129691:e3#2` (equity-post-hct-surv, Master; steps 77129691:8->9): After bracketing an optimum on one hyperparameter, revert it to the best-known value and change only the second hyperparameter. Never change two hyperparameters simultaneously when the expected effect size is small, because a regression cannot be attributed. If you do change two and regress, revert both to the last-known-good state before continuing.

## 6. stop_same_lever_after_consecutive_regressions  [L3]  —  5 kernels, 4 comps, 6 items

- **Context:** 3-4 consecutive submissions tuning the same lever (e.g., blend weights, augmentation strength, a single hyperparameter) all regress from the known best score, with no upward trend.
- **Action:** Stop tuning that lever and switch to a qualitatively different lever (e.g., from weight tuning to adding a new model, from augmentation to loss function). The consecutive regressions signal the current lever is not the binding constraint. If you must continue, try at most one more alternative configuration before abandoning the lever entirely.
- **Exceptions:** 13542132:e3#1 shows the author tried one more step after 3 regressions before stopping, suggesting the threshold may be 4 rather than 3 in some cases. 58130512:e30#1 shows the author did NOT follow this rule and suffered 5 consecutive regressions. If the auxiliary model is much weaker, a narrow micro-weight sweep (1-2% region, ~8 trials max) may still be worthwhile before stopping (29588171:e1#1).
- **Support:** kernels 13542132, 15203842, 18350823, 29588171, 58130512; comps amex-default-prediction, commonlitreadabilityprize, learning-agency-lab-automate, ranzcr-clip-catheter-line-cl; tiers {'Master': 3, 'Grandmaster': 2, 'Expert': 1}; episode reached new best: {'no': 3, 'yes': 3}
- **Cells:** L3/sweep/none_visible, L3/sweep/plateau
- **Examples:**
  - `13542132:e3#1` (ranzcr-clip-catheter, Master; steps 13542132:12->13): After 3-4 consecutive regressions from tuning the same lever, stop and switch to a fundamentally different lever (e.g., loss function, architecture, learning schedule). The diminishing returns signal that the current lever is not the binding constraint on performance.
  - `15203842:e1#1` (ranzcr-clip-catheter, Grandmaster; steps 15203842:1->2, 15203842:4->5): Start near equal weighting (e.g., 0.45/0.55) based on which source has slightly better validation. Submit, then try equal weighting (0.50/0.50). If the gain from a 5-percentage-point shift is negligible (<0.001), stop tuning weights and invest effort elsewhere (e.g., adding a third source or improving individual models).
  - `15203842:e1#2` (ranzcr-clip-catheter, Grandmaster; steps 15203842:4->5): Abandon the sweep after one or two steps if the improvement is negligible (e.g., <0.0001 on AUC). Switch to a qualitatively different lever—such as adding new models, changing architectures, or improving individual model quality—rather than continuing fine-grained weight tuning.
  - `18350823:e4#1` (commonlitreadability, Expert; steps 18350823:8->9, 18350823:9->10, 18350823:10->11, 18350823:11->12): If adjusting blend weights across existing model predictions fails to beat the baseline after 3-4 submissions, stop tuning weights and instead add a new, architecturally diverse model to the ensemble. Weight tuning has diminishing returns when component predictions are too correlated.
  - `29588171:e1#1` (amex-default-predict, Master; steps 29588171:1->2, 29588171:2->3, 29588171:3->4, 29588171:4->5): Start with a very small weight for the weak model (1-2%). Sweep in increments of ~0.5% around that region. Submit a few points, reverse direction immediately after any score drop, and stop once you have bracketed the optimum within ~0.5%. Do not invest more than ~8 trials on micro-weight tuning; if gains plateau, switch to improving the weak model itself.
  - `58130512:e30#1` (learning-agency-lab-, Master; steps 58130512:91->92, 58130512:92->93, 58130512:93->94, 58130512:94->95): Change only one knob per submission so you can attribute gains or losses. If you change multiple knobs simultaneously and regress, you cannot tell which change hurt. After a regression, revert to the last-best configuration before trying a different knob. If 2-3 consecutive submissions all regress, stop the sweep and try a qualitatively different approach.

## 7. isolate_single_change_per_submission  [L3]  —  5 kernels, 4 comps, 5 items

- **Context:** When testing multiple new ideas (e.g., new checkpoint + hyperparameter change, new feature + new metric, checkpoint swap + architecture hyperparameter change) and each leaderboard submission is costly or limited.
- **Action:** Change only one lever per submission so regressions can be attributed. When swapping a pretrained checkpoint, first submit with the original hyperparameters to isolate the checkpoint effect; only after confirming the checkpoint works, change one hyperparameter at a time. If you bundled changes and regressed, partially revert the most suspicious change first. If two consecutive bundled submissions both regress, revert fully to the last known best before trying anything else.
- **Exceptions:** When submission budget is very tight and one change is expected to dominate the effect (e.g., major hyperparameter overhaul vs. minor feature cleanup), bundling is acceptable per 27836972:e13#2.
- **Support:** kernels 27656049, 52551258, 53762022, 59253662, 7240226; comps amex-default-prediction, google-quest-challenge, hms-harmful-brain-activity-c, learning-agency-lab-automate; tiers {'Expert': 2, 'Contributor': 3}; episode reached new best: {'no': 4, 'yes': 1}
- **Cells:** L3/probe/new_idea/part2
- **Examples:**
  - `27656049:e5#1` (amex-default-predict, Expert; steps 27656049:16->17, 27656049:17->18): When probing a new idea, change only one lever per submission so regressions can be attributed. If you bundle changes and regress, partially revert the most suspicious change first. If two consecutive submissions both regress from the baseline, abandon the new ideas and revert fully before trying something else.
  - `52551258:e5#1` (hms-harmful-brain-ac, Expert; steps 52551258:7->8, 52551258:8->9): Probe one alternative model variant at a time against your current best. If the first variant regresses, do not combine it into an ensemble—revert and try a structurally different alternative. If two consecutive probes both regress, abandon this family of variants and move to a different model architecture or ensemble strategy.
  - `53762022:e2#1` (hms-harmful-brain-ac, Contributor; steps 53762022:5->6, 53762022:6->7): When substituting a new checkpoint, first submit with the original hyperparameters to isolate the checkpoint effect. Only after confirming the checkpoint works, change one hyperparameter at a time. Never change both checkpoint and architecture hyperparameters without intermediate validation, as a regression becomes undiagnosable.
  - `59253662:e7#1` (learning-agency-lab-, Contributor; steps 59253662:29->30, 59253662:30->31): Treat it as a single probe: apply the change, submit once, and if the leaderboard score regresses, abandon the idea immediately and revert. Do not tune the resampling parameters—if the direction is wrong, parameter tuning won't save it. Bundle the change with minimal other modifications so the signal is attributable.
  - `7240226:e3#2` (google-quest-challen, Contributor; steps 7240226:8->9, 7240226:9->10): When combining a new layer/component with a hyperparameter change causes a regression, comment out or remove the new component first while keeping other changes. If performance recovers, the component was harmful. Do not re-introduce it. Submit only after confirming recovery.

## 8. revert_to_best_before_trying_new_direction  [L3]  —  5 kernels, 3 comps, 6 items

- **Context:** A submission regresses from the known best score (due to hyperparameter changes, ensemble weight changes, or multiple simultaneous modifications), and you want to try a different configuration next.
- **Action:** Fully revert to the exact last-best configuration before trying a different knob or direction. Do not chain changes on top of a regressed configuration. Never stack untested changes on top of a regression. Change only one knob per submission to maintain attribution. Test one parameter (or one component) at a time against the baseline to isolate effects. If partial rollback is attempted, keep only 1-2 changes you have strongest reason to believe are beneficial.
- **Exceptions:** 18426209:e7#1 shows the author did NOT revert to the known-best 0.5/0.5 after regression, instead trying a different blend—deviating from strict revert-on-regression. 58130512:e30#1 shows the author changed multiple knobs per step and never reverted, resulting in inability to isolate causes. In 60759531, the author only partially reverted while changing other parameters simultaneously, which prevented isolation but did not completely block progress. In 77450317, the regression was due to stale component models rather than HP changes, so the fix was upgrading components rather than reverting HPs.
- **Support:** kernels 18426209, 55591012, 58130512, 60759531, 77450317; comps commonlitreadabilityprize, equity-post-hct-survival-pre, learning-agency-lab-automate; tiers {'Expert': 3, 'Grandmaster': 2, 'Master': 1}; episode reached new best: {'no': 4, 'yes': 2}
- **Cells:** L3/sweep/plateau, L3/sweep/regression
- **Examples:**
  - `18426209:e7#2` (commonlitreadability, Expert; steps 18426209:9->10, 18426209:10->11): After a regression on a noisy leaderboard, try one alternative configuration before concluding the direction is unproductive. If the alternative also fails or looks unpromising locally, revert to the known best and move on to a different lever entirely. Do not submit configurations that look worse locally.
  - `55591012:e12#1` (learning-agency-lab-, Grandmaster; steps 55591012:41->42, 55591012:45->46, 55591012:46->47, 55591012:47->48): Start with coarse steps to identify the direction of improvement. When a step causes regression, reverse direction and halve the step size. When two consecutive submissions differ by less than noise (e.g., 0.0000 delta), declare the optimum bracketed and stop sweeping that parameter. Move to a qualitatively different lever.
  - `58130512:e30#1` (learning-agency-lab-, Master; steps 58130512:91->92, 58130512:92->93, 58130512:93->94, 58130512:94->95): Change only one knob per submission so you can attribute gains or losses. If you change multiple knobs simultaneously and regress, you cannot tell which change hurt. After a regression, revert to the last-best configuration before trying a different knob. If 2-3 consecutive submissions all regress, stop the sweep and try a qualitatively different approach.
  - `60759531:e2#1` (learning-agency-lab-, Expert; steps 60759531:2->3, 60759531:3->4, 60759531:4->5, 60759531:5->6): Before tuning, snapshot the exact baseline configuration. If the first change regresses, fully revert to baseline before trying the next change. Never stack untested changes on top of a regression. Test one parameter at a time against the known-good baseline to isolate effects.
  - `60759531:e3#1` (learning-agency-lab-, Expert; steps 60759531:9->10, 60759531:10->11): Revert most of the changes back toward the previous best configuration while keeping one or two modifications you believe are promising. Submit to check recovery. If score partially recovers, continue adjusting the remaining changed parameters individually or in small groups.
  - `77450317:e11#1` (equity-post-hct-surv, Grandmaster; steps 77450317:22->23, 77450317:25->26): When ensemble blend tuning regresses, upgrade the underlying component model predictions (retrained or improved versions) rather than continuing to tune weights on stale predictions. Retune blend weights jointly with the new components. Verify with a submission before iterating further.

## 9. isolate_changes_on_regression  [L3]  —  4 kernels, 4 comps, 5 items

- **Context:** A submission that bundled multiple changes (e.g., new checkpoints across all folds, feature selection, hyperparameters, post-processing) caused a score regression, and you cannot attribute the cause to a single change.
- **Action:** Revert to the last known-good configuration, then re-apply changes one at a time with a submission after each to isolate which factor caused the regression. Revert the most speculative changes first (novel post-processing, hyperparameter tweaks) while keeping the structural addition under test. For checkpoint swaps: use per-fold CV to identify which folds improved and construct a mixed list. For hyperparameters: fix all but one variable and sweep it before moving to the next. Only combine changes once each is validated individually. Submit 3-5 systematic partial-configuration submissions to layer additional changes back in.
- **Exceptions:** Per-fold cherry-picking across checkpoint sources may introduce distribution mismatch (18426209 counter_evidence: mixed selection still didn't beat original). In practice, authors sometimes succeed by combining multiple changes in a single submission (e.g., 60197293 v130), so strict one-at-a-time isolation may be relaxed when submission budget is tight and the combined changes are well-understood.
- **Support:** kernels 18426209, 27389424, 60197293, 75584724; comps amex-default-prediction, commonlitreadabilityprize, equity-post-hct-survival-pre, learning-agency-lab-automate; tiers {'Expert': 3, 'Grandmaster': 1, 'Master': 1}; episode reached new best: {'no': 2, 'yes': 3}
- **Cells:** L3/sweep/new_resource, L3/sweep/pipeline_gap
- **Examples:**
  - `18426209:e6#1` (commonlitreadability, Expert; steps 18426209:7->8, 18426209:8->9): First test the new checkpoint source by swapping all folds at once. If the score regresses, use per-fold CV scores to identify which folds improved and which worsened, then construct a mixed checkpoint list keeping the best fold from whichever source has the lower fold-level error. Hard-code the paths to make the selection explicit and reproducible.
  - `27389424:e7#1` (amex-default-predict, Grandmaster; steps 27389424:57->58, 27389424:58->59, 27389424:59->60, 27389424:60->61): Start at a low value, then sweep upward in roughly doubling steps (10%→20%→25%→33%→50%→75%), submitting every 1–2 steps to get leaderboard signal. When the score drops after an increase, the optimum is bracketed between the last two submitted values. Stop and move on rather than bisecting further if the gain is small.
  - `60197293:e18#2` (learning-agency-lab-, Expert; steps 60197293:126->127, 60197293:127->128, 60197293:128->129): When a combined change regresses, revert the most speculative changes first (e.g., hyperparameter changes, novel post-processing) while keeping the structural addition you are testing. Then submit the simpler variant to isolate the effect of the new feature. Only after confirming the feature's value, layer on hyperparameter tuning.
  - `60197293:e18#3` (learning-agency-lab-, Expert; steps 60197293:125->126, 60197293:126->127, 60197293:128->129, 60197293:129->130): After a long development phase, submit partial configurations (feature on/off, selection on/off) to build evidence about which components help before combining everything. Use 3-5 submissions with systematic toggling rather than one big submission. The final combination should include only components that showed positive signal individually or in small groups.
  - `75584724:e6#2` (equity-post-hct-surv, Master; steps 75584724:11->12, 75584724:12->13, 75584724:13->14): After a regression from bundled changes, revert one variable at a time while keeping others fixed. Submit after each single change to isolate which factor caused the regression. Once the beneficial change is identified, re-apply the other change on top of it to check for interaction.

## 10. weight_stronger_model_higher_in_initial_blend  [L2]  —  4 kernels, 4 comps, 4 items

- **Context:** You have multiple models with known individual scores (from CV or solo LB submissions) and need to set initial blend weights.
- **Action:** Assign higher initial weight (e.g., 70–80%) to the model with the best solo score. Test each new model solo first to establish standalone quality. Then combine, using solo scores to inform weight allocation. Start from this informed prior and sweep outward rather than starting from equal weights. Exception: when models have very similar CV scores from the same architecture, start with equal weights instead.
- **Exceptions:** 15173072:e5#3 shows that when models have similar CV scores and the same architecture, equal weighting is preferred and unequal weights don't help.
- **Support:** kernels 15173072, 18423958, 55591012, 73671444; comps commonlitreadabilityprize, equity-post-hct-survival-pre, learning-agency-lab-automate, ranzcr-clip-catheter-line-cl; tiers {'Contributor': 1, 'Master': 1, 'Grandmaster': 2}; episode reached new best: {'yes': 4}
- **Cells:** L2/ensemble_blend_weight_tuning
- **Examples:**
  - `15173072:e5#3` (ranzcr-clip-catheter, Contributor; steps 15173072:21->22, 15173072:27->28): Start with equal-weight averaging (50/50). Unequal weights rarely help when models have similar CV scores from the same architecture. If you try unequal weights and they don't improve over equal weights, revert to equal weighting. The fold with the highest CV score is the best candidate to pair with your primary model.
  - `18423958:e4#1` (commonlitreadability, Master; steps 18423958:9->10): Start by assigning higher weight to the model you believe is strongest based on individual scores. If you have reason to believe a different model is actually stronger (e.g., from CV), swap the dominant weight to that model while keeping other weights fixed. Submit after each change. Stop once you achieve a new best score.
  - `55591012:e12#2` (learning-agency-lab-, Grandmaster; steps 55591012:45->46, 55591012:46->47, 55591012:47->48): Fix model training and sweep blend weights in ~0.05 increments around the suspected optimum. After identifying the best coarse value, refine with 0.01 increments. If two adjacent values give identical LB scores, the optimum is found. Avoid changing blend weights and model hyperparameters simultaneously—when you must, attribute gains by testing each independently afterward.
  - `73671444:e5#1` (equity-post-hct-surv, Grandmaster; steps 73671444:12->13, 73671444:13->14, 73671444:14->15, 73671444:15->16): First test each new model solo (weight=1.0) to establish its standalone quality. Then combine the best-performing models with a multi-way blend. Use the solo scores to inform initial weight allocation: give more weight to better solo performers. Iterate weights in coarse steps (e.g., 0.1–0.2 increments) rather than fine-tuning, since leaderboard noise dominates at small deltas.

## 11. sweep_blend_weights_one_knob_at_a_time  [L2]  —  4 kernels, 3 comps, 4 items

- **Context:** You have 2+ pretrained models combined via blend weights, and you are tuning weights using leaderboard or CV feedback.
- **Action:** Change only one knob (blend weight) per submission so score changes can be attributed. Sweep in coarse steps (~0.05–0.1) first, then refine with finer increments (~0.01) around the best value. Do not simultaneously change blend weights and model hyperparameters or other corrections (e.g., additive bias). If single-knob sweeps show no signal after a few steps, the models may be too correlated for weight tuning to help.
- **Exceptions:** In 55591012:e12#2 the author sometimes changed blend weights and reg_alpha simultaneously, slowing attribution. In 7823861:e7#2, weight tuning yielded no improvement, suggesting effort should shift to model diversity.
- **Support:** kernels 55591012, 55987255, 77347591, 7823861; comps equity-post-hct-survival-pre, google-quest-challenge, learning-agency-lab-automate; tiers {'Grandmaster': 1, 'Master': 1, 'Expert': 1, nan: 1}; episode reached new best: {'yes': 1, 'no': 3}
- **Cells:** L2/ensemble_blend_weight_tuning
- **Examples:**
  - `55591012:e12#2` (learning-agency-lab-, Grandmaster; steps 55591012:45->46, 55591012:46->47, 55591012:47->48): Fix model training and sweep blend weights in ~0.05 increments around the suspected optimum. After identifying the best coarse value, refine with 0.01 increments. If two adjacent values give identical LB scores, the optimum is found. Avoid changing blend weights and model hyperparameters simultaneously—when you must, attribute gains by testing each independently afterward.
  - `55987255:e29#1` (learning-agency-lab-, Master; steps 55987255:174->175, 55987255:175->176, 55987255:176->177, 55987255:177->178): Sweep the blend weight in steps of ~0.05 across the plausible range, submitting each to the leaderboard. Start near the current value, walk in one direction, and once you pass the peak (score drops on both sides), return to the best value and confirm. If the landscape is noisy, bracket the optimum from both sides before committing.
  - `77347591:e9#2` (equity-post-hct-surv, Expert; steps 77347591:25->26, 77347591:28->29): Vary only one knob per submission so you can attribute any score change. If single-knob sweeps show no signal after a few steps, do not combine changes—the joint space is also flat. Instead, validate locally with a reliable CV metric before spending submissions.
  - `7823861:e7#2` (google-quest-challen, nan; steps 7823861:27->28, 7823861:28->29): Start from equal weights (0.5/0.5), then try shifting toward the stronger model in increments of 0.1. Test at most 2-3 values. If no improvement over the baseline, the models may be too correlated for weight tuning to help, and effort is better spent on model diversity or post-processing.

## 12. prune_weak_ensemble_members  [L2]  —  4 kernels, 3 comps, 4 items

- **Context:** When an ensemble (stacking or weighted blend) includes a model whose OOF performance is noticeably worse than other members, or when adding a new model caused a score regression.
- **Action:** Remove the weakest model entirely rather than relying on the optimizer/stacker to downweight it. Re-run the ensemble and verify on LB. Even with optimized weights, a weak member can inject noise the optimizer cannot fully suppress. If removal improves the score, continue pruning the next weakest; if it worsens, restore and try removing a different member.
- **Exceptions:** In larger ensembles or with highly diverse architectures, even weaker members can help through diversity (18757376 notes this for larger data). Also, ordering of removals matters—removing the wrong member first can worsen the score (18550705 counter_evidence).
- **Support:** kernels 18550705, 18757376, 7548275, 75924487; comps commonlitreadabilityprize, equity-post-hct-survival-pre, google-quest-challenge; tiers {'Master': 2, 'Expert': 2}; episode reached new best: {'yes': 4}
- **Cells:** L2/ensemble_composition
- **Examples:**
  - `18550705:e2#2` (commonlitreadability, Master; steps 18550705:6->7, 18550705:7->8, 18550705:8->9): Remove the model you have least confidence in first (e.g., the one with the most different architecture or worst standalone CV). Submit after each removal. If score improves, continue pruning the next weakest. If score worsens, restore that member and try removing a different one instead.
  - `18757376:e4#2` (commonlitreadability, Expert; steps 18757376:5->6): In a transformer stacking ensemble, compare OOF RMSE of each backbone group. If a weaker backbone group degrades the blend, remove it entirely rather than downweighting it. Fewer but stronger members often outperform more diverse but noisier ones on small datasets.
  - `7548275:e5#1` (google-quest-challen, Expert; steps 7548275:19->20): Remove the weakest model from the ensemble entirely (don't just rely on the optimizer to zero its weight). Re-run and check LB. Even with weight optimization, removing a bad model can yield large gains because the optimizer may not fully suppress it across all targets/folds.
  - `75924487:e1#1` (equity-post-hct-surv, Master; steps 75924487:1->2): Examine per-model OOF performance and inter-model correlation. Curate a subset that drops weak or highly redundant members. Apply the filter before the ensembler trains. Verify with a single submission; if positive, keep and move on rather than iterating further on the subset.

## 13. test_new_model_with_minimal_other_changes  [L3]  —  4 kernels, 3 comps, 4 items

- **Context:** Introducing a new model architecture, backbone, or checkpoint variant into an existing pipeline.
- **Action:** Swap only the model/checkpoint while keeping all other pipeline components (post-processing, ensemble weights, preprocessing) identical. Submit to get a clean signal. If it regresses, try one alternative checkpoint before reverting the architecture entirely. Do not combine the model swap with other untested changes.
- **Exceptions:** 13848868:e5#1 notes that post-processing preferences may not transfer across models, so after the clean model swap, also test toggling post-processing on/off for the new model.
- **Support:** kernels 13848868, 50496431, 6803050, 7018718; comps google-quest-challenge, hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 2, 'Master': 1, 'Expert': 1}; episode reached new best: {'yes': 2, 'no': 2}
- **Cells:** L3/probe/new_idea/part1
- **Examples:**
  - `13848868:e5#1` (ranzcr-clip-catheter, Grandmaster; steps 13848868:16->17, 13848868:17->18, 13848868:18->19, 13848868:19->20): When swapping in a new model, first submit with the simpler post-processing (off/raw probabilities). If the score is promising, toggle the post-processing on and compare. Always test both states for each new model before concluding which is better. Do not assume the post-processing preference transfers across model changes.
  - `50496431:e55#1` (hms-harmful-brain-ac, Grandmaster; steps 50496431:214->215, 50496431:215->216, 50496431:216->217, 50496431:217->218): When probing a new model or feature, first test it in isolation or with minimal other changes to get a clean signal. If the first submission regresses significantly (>10% worse), do not continue varying multiple axes simultaneously—instead either revert entirely or isolate the single most promising change. Limit probe attempts to 2-3 submissions before abandoning if no improvement is seen.
  - `6803050:e7#1` (google-quest-challen, Master; steps 6803050:23->24): Swap all fold checkpoints to the alternative variant in a single submission, keeping all other pipeline components identical. If the score regresses, immediately revert to the original checkpoints rather than debugging the new variant. Do not combine the new variant with other untested changes.
  - `7018718:e8#1` (google-quest-challen, Expert; steps 7018718:25->26, 7018718:26->27): Before reverting an architectural change that regressed, try at least one alternative checkpoint with the same architecture. A regression may be due to the specific checkpoint rather than the architecture itself. Only revert the architecture if multiple checkpoints consistently underperform.

## 14. revert_confounded_changes_before_continuing  [L3]  —  4 kernels, 3 comps, 4 items

- **Context:** A submission regresses sharply after changing two or more variables simultaneously (e.g., backbone + resolution, checkpoint + preprocessing, architecture + data split).
- **Action:** Revert entirely to the last known-good configuration. Then re-explore by changing only one variable at a time, submitting after each change. Do not attempt to salvage the new combination or fix individual parameters within the failed bundle.
- **Exceptions:** 13577502:e3#2 notes the revert was partial (different dropout/augmentation), not clean. 7670859:e5#3 suggests an alternative: vary non-data changes first while holding data fixed, then revert data if needed.
- **Support:** kernels 13577502, 49576186, 7670859, 7823861; comps google-quest-challenge, hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Expert': 2, 'Contributor': 1, nan: 1}; episode reached new best: {'yes': 3, 'no': 1}
- **Cells:** L3/sweep/new_idea/part2
- **Examples:**
  - `13577502:e3#2` (ranzcr-clip-catheter, Expert; steps 13577502:8->9): Revert to the configuration that produced the best score, then change only one variable at a time. Do not attempt to salvage the new combination—return to the known-good baseline first, then re-explore incrementally.
  - `49576186:e6#1` (hms-harmful-brain-ac, Expert; steps 49576186:34->35, 49576186:36->37, 49576186:37->38, 49576186:38->39): When sweeping multiple interacting dimensions and scores regress, do not continue changing multiple things at once. Instead, revert to the last best configuration and change only one dimension at a time. If three consecutive multi-factor changes all regress, stop the sweep and try a structurally different approach.
  - `7670859:e5#3` (google-quest-challen, Contributor; steps 7670859:28->29, 7670859:29->30, 7670859:30->31): When a bundle of changes causes regression, first vary the non-data changes (hyperparameters, architecture) while holding the data change fixed. If those variations show no improvement, revert the data change. This identifies whether the regression came from reduced data or from the model change, without fully reverting everything at once.
  - `7823861:e5#2` (google-quest-challen, nan; steps 7823861:22->23, 7823861:23->24): When a multi-parameter change causes a large regression, revert entirely to the last known-good version rather than attempting to fix individual parameters. Then re-apply changes one at a time or in small groups, submitting after each, to isolate which change caused the regression. Never change more parameters in one step than you changed in your best-performing step.

## 15. ensemble_sweep_one_member_at_a_time  [L3]  —  4 kernels, 3 comps, 4 items

- **Context:** You have a small set of candidate models or checkpoints for an ensemble and want to find the best combination using leaderboard feedback.
- **Action:** Establish a baseline blend. Then vary one dimension at a time: add/remove a single member, or change one weight. When removing a component worsens the score, keep it. When adding members, continue until gains plateau. Do not change multiple members or weights simultaneously. Stop after all candidates are tested or consecutive improvements drop below noise level.
- **Exceptions:** 15173072:e5#1 notes the author did change multiple things simultaneously in several steps, undermining attribution.
- **Support:** kernels 15173072, 17616127, 18523075, 49524919; comps commonlitreadabilityprize, hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Contributor': 2, 'Expert': 1, 'Grandmaster': 1}; episode reached new best: {'yes': 4}
- **Cells:** L3/sweep/new_idea/part2
- **Examples:**
  - `15173072:e5#1` (ranzcr-clip-catheter, Contributor; steps 15173072:21->22, 15173072:22->23, 15173072:23->24, 15173072:24->25): After finding a good ensemble pair, systematically try each alternative member one at a time while noting scores. If all alternatives score worse than the original, revert to the original configuration. Do not change multiple things (checkpoint + weight + normalization) simultaneously, as it confounds the signal. Limit the sweep to the number of available candidates plus a few weight variations.
  - `17616127:e10#1` (commonlitreadability, Contributor; steps 17616127:35->36, 17616127:37->38, 17616127:38->39, 17616127:39->40): First establish a baseline blend. Then vary one dimension at a time: add/remove a member, or change weights. When removing a component worsens the score, add it back. When adding members improves the score, keep adding until gains plateau. Separate structurally different prediction sources (e.g., meta-learner vs. direct models) into groups, average within groups, then weight across groups. Stop when consecutive improvements drop below ~0.001.
  - `18523075:e6#1` (commonlitreadability, Expert; steps 18523075:11->12, 18523075:12->13, 18523075:13->14, 18523075:14->15): First add the new member while disabling several existing members to create headroom. Submit to verify the new member works. Then re-enable disabled members one at a time, submitting after each, to find the best subset. Stop when all candidates have been tried. Keep the configuration that achieved the best score.
  - `49524919:e33#1` (hms-harmful-brain-ac, Grandmaster; steps 49524919:148->149, 49524919:149->150, 49524919:150->151, 49524919:151->152): Disable all model groups except one (using skip/continue flags), submit each group's standalone predictions to the leaderboard, cycle through all groups to rank them, then re-enable all groups for the final blended submission. This reveals which groups are strong standalone and confirms the blend outperforms any individual member.

## 16. add_diverse_model_when_weight_tuning_plateaus  [L3]  —  4 kernels, 3 comps, 4 items

- **Context:** Blend-weight tuning across existing models has failed to improve the score after 2-4 attempts, the ensemble score is plateaued, and the component model predictions have not been updated recently.
- **Action:** Stop tuning weights on stale predictions and instead upgrade or add a new, architecturally diverse model to the ensemble. Weight tuning has diminishing returns when component predictions are too correlated or stale. Before submitting the new model's ensemble, verify it doesn't break the pipeline via local CV. Then retune blend weights jointly with the new components. Only submit after confirming CV is reasonable.
- **Exceptions:** The stopping threshold is flexible—75145694 continued for 3 declining submissions past the peak rather than stopping at 2.
- **Support:** kernels 18350823, 55591012, 75145694, 77450317; comps commonlitreadabilityprize, equity-post-hct-survival-pre, learning-agency-lab-automate; tiers {'Expert': 2, 'Grandmaster': 2}; episode reached new best: {'no': 1, 'yes': 3}
- **Cells:** L3/sweep/plateau, L3/sweep/regression
- **Examples:**
  - `18350823:e4#1` (commonlitreadability, Expert; steps 18350823:8->9, 18350823:9->10, 18350823:10->11, 18350823:11->12): If adjusting blend weights across existing model predictions fails to beat the baseline after 3-4 submissions, stop tuning weights and instead add a new, architecturally diverse model to the ensemble. Weight tuning has diminishing returns when component predictions are too correlated.
  - `55591012:e12#3` (learning-agency-lab-, Grandmaster; steps 55591012:39->40, 55591012:40->41): When integrating a new component, first run locally without submitting to verify it doesn't break the pipeline and check CV. Only submit after confirming CV is reasonable. If the new component doesn't help on CV, revert it before spending a submission.
  - `75145694:e14#1` (equity-post-hct-surv, Expert; steps 75145694:46->47, 75145694:47->48, 75145694:49->50, 75145694:50->51): Run your local optimizer to produce a candidate weight set, submit it, and compare LB to your best. If LB improves, record it and continue exploring nearby configurations. If LB declines for 2-3 consecutive attempts with different configurations, stop sweeping weights and instead add a new diverse model to the pool before resuming.
  - `77450317:e11#1` (equity-post-hct-surv, Grandmaster; steps 77450317:22->23, 77450317:25->26): When ensemble blend tuning regresses, upgrade the underlying component model predictions (retrained or improved versions) rather than continuing to tune weights on stale predictions. Retune blend weights jointly with the new components. Verify with a submission before iterating further.

## 17. limit_submissions_on_failed_external_data_or_component  [L3]  —  3 kernels, 3 comps, 4 items

- **Context:** Adding external data or a new component (external model predictions, auxiliary dataset) shows regression or no improvement after initial submissions, and alternative levers exist.
- **Action:** Allow at most two submission attempts with variations (e.g., different filtering, different integration). If both fail to improve over baseline, revert all related changes and move to an orthogonal lever. Do not continue tuning the failed addition's parameters.
- **Exceptions:** More sophisticated approaches (pseudo-labeling, careful filtering) might eventually help, so this rule trades potential gains for time efficiency (49576186 counter_evidence).
- **Support:** kernels 49576186, 59253662, 77276039; comps equity-post-hct-survival-pre, hms-harmful-brain-activity-c, learning-agency-lab-automate; tiers {'Expert': 3, 'Contributor': 1}; episode reached new best: {'no': 4}
- **Cells:** L3/probe/new_resource
- **Examples:**
  - `49576186:e24#1` (hms-harmful-brain-ac, Expert; steps 49576186:150->151, 49576186:152->153, 49576186:154->155): Test external data inclusion with aggressive filtering (remove ambiguous classes, deduplicate, keep only high-confidence labels). If two successive submissions show no improvement over baseline, revert the external data changes and move to a different lever rather than continuing to tune the filtering criteria.
  - `49576186:e24#2` (hms-harmful-brain-ac, Expert; steps 49576186:151->152, 49576186:153->154, 49576186:154->155, 49576186:156->157): After a bundled change regresses, try one more variant that modifies the most suspicious component (here, extra-data filtering). If that also fails, revert all bundled changes to recover the baseline score, then pursue a completely different lever. Do not spend more than two submissions diagnosing a failed bundle.
  - `59253662:e6#2` (learning-agency-lab-, Contributor; steps 59253662:28->29): If a bundled change produces even a small regression and you have alternative ideas, move on rather than debugging which component caused the drop. Time is better spent on orthogonal improvements. Only revisit if you run out of other levers.
  - `77276039:e4#1` (equity-post-hct-surv, Expert; steps 77276039:15->16, 77276039:16->17): Submit the ensemble both with and without the candidate member. Compare LB scores directly. If the candidate hurts performance, exclude it. Do not spend more than two submissions on this binary test before moving on.

## 18. simplify_model_when_small_data_or_invariant_model  [L2]  —  3 kernels, 3 comps, 3 items

- **Context:** When model complexity (extra preprocessing layers, larger hidden layers, or multi-layer stacking heads) is not yielding performance gains, and either (a) the training set is small (<10K rows) suggesting overfitting risk, or (b) the model family is inherently invariant to the removed steps (e.g., tree models handle missingness and are scale-invariant).
- **Action:** Simplify the pipeline: remove unnecessary preprocessing (scaling, imputation, outlier removal) for invariant models; reduce stacking heads to simple weighted averages for small datasets; shrink MLP depth/width when capacity increases show no gain. Verify on LB that simplification does not hurt. If it degrades, revert. Change only one component at a time to correctly attribute effects.
- **Exceptions:** 28093671:e8#3 notes that post-aggregation cleanup (imputation of NaN aggregates) may still be needed even when raw-feature imputation is removed. 18550705:e5#2 warns that changing multiple components simultaneously (e.g., stacking head and ensemble membership) prevents proper attribution of any degradation.
- **Support:** kernels 18550705, 28093671, 7670859; comps amex-default-prediction, commonlitreadabilityprize, google-quest-challenge; tiers {'Master': 1, 'Contributor': 2}; episode reached new best: {'no': 1, 'yes': 2}
- **Cells:** L2/model_architecture_simplification
- **Examples:**
  - `18550705:e5#2` (commonlitreadability, Master; steps 18550705:11->12): Replace a multi-layer stacking head with a learnable softmax-weighted average of base model predictions. If this degrades performance, the original head was not overfitting, and you should revert. Do not change the stacking head and the ensemble membership simultaneously, as you cannot attribute the effect.
  - `28093671:e8#3` (amex-default-predict, Contributor; steps 28093671:34->35): Remove scaling, imputation, and outlier removal from the GBDT pipeline. Let the model handle missing values natively. Submit to confirm that removing these steps does not hurt (and likely helps by preserving more data and signal).
  - `7670859:e5#2` (google-quest-challen, Contributor; steps 7670859:28->29, 7670859:29->30): If increasing model capacity shows no gain, suspect the bottleneck is data volume rather than model expressiveness. Simplify the architecture (fewer layers) and restore full training data before concluding the model family is inadequate. With small datasets (<10K rows), a single hidden layer MLP often suffices and adding layers mainly adds overfitting risk.

## 19. match_inference_preprocessing_to_training  [L2]  —  3 kernels, 3 comps, 3 items

- **Context:** When running inference with a trained checkpoint and the inference pipeline's preprocessing parameters (resolution, normalization, scaling, frequency cropping, etc.) may differ from what the model was trained with.
- **Action:** Before tuning model architecture or ensembling, verify that all inference preprocessing exactly matches training: input resolution, normalization mean/std, spectrogram parameters (n_fft, win_length, hop_length, scaling), frequency crops, and any dataset-specific transforms. Fix all mismatches in one pass. If the training config is unknown, test first without extra preprocessing, then with it. Do not change preprocessing parameters at inference time unless the model was trained with those exact parameters; if experimenting, change only one parameter at a time and expect regressions from mismatches.
- **Exceptions:** none
- **Support:** kernels 15082684, 50496431, 7018718; comps google-quest-challenge, hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Master': 1, 'Grandmaster': 1, 'Expert': 1}; episode reached new best: {'yes': 1, 'no': 2}
- **Cells:** L2/preprocessing_alignment
- **Examples:**
  - `15082684:e4#1` (ranzcr-clip-catheter, Master; steps 15082684:16->17, 15082684:17->18): Before tuning model architecture or ensembling, verify that inference preprocessing exactly matches training: check input resolution, normalization mean/std, and any dataset-specific transforms. Fix all mismatches in one pass, as each alone may not fully explain the gap. This is especially important for medical imaging where pixel statistics differ substantially from ImageNet.
  - `50496431:e55#2` (hms-harmful-brain-ac, Grandmaster; steps 50496431:214->215, 50496431:216->217): Do not change spectrogram generation parameters (n_fft, win_length, hop_length, scaling/normalization, frequency cropping) at inference time unless the model was trained with those exact parameters. If you must experiment, change only one parameter at a time and expect regressions if training/inference mismatch.
  - `7018718:e9#2` (google-quest-challen, Expert; steps 7018718:27->28, 7018718:28->29, 7018718:29->30): Match preprocessing flags to what the checkpoint was trained with. If you don't know the training config, test the checkpoint first without preprocessing, then with it. Expect that preprocessing helps only checkpoints trained to expect it. Abandon a checkpoint after 2 toggle tests if it underperforms.

## 20. ensemble_membership_selection_by_incremental_swap  [L3]  —  3 kernels, 3 comps, 3 items

- **Context:** You have multiple trained model variants/checkpoints and want to find the best ensemble combination, with limited submission budget or noisy leaderboard signal.
- **Action:** Evaluate candidate models individually first to establish standalone quality. Then build the ensemble incrementally: add or swap one member at a time, submit, and compare. If the score improves, keep the change; if it regresses, revert that member and try a different candidate. When uniform averaging dilutes a strong model, switch to weighted blending. Stop when consecutive swaps regress or candidates are exhausted.
- **Exceptions:** 60264017: author did not always fully revert before trying the next swap, suggesting partial revert plus forward exploration can also work. 52860091: a weak model can still help in ensemble (v0+v1 beat both alone), but this doesn't always hold (v0+v2 was worse than v2 alone).
- **Support:** kernels 18550705, 52860091, 60264017; comps commonlitreadabilityprize, hms-harmful-brain-activity-c, learning-agency-lab-automate; tiers {'Master': 2, 'Grandmaster': 1}; episode reached new best: {'yes': 3}
- **Cells:** L3/explore/new_idea
- **Examples:**
  - `18550705:e2#1` (commonlitreadability, Master; steps 18550705:3->4, 18550705:5->6, 18550705:6->7, 18550705:7->8): First expand the ensemble aggressively by adding multiple diverse models in one or two steps. If the expanded ensemble improves, keep it as baseline. Then prune one model at a time, removing the most suspect member (e.g., weakest backbone or most recently added). Use CV scores as primary signal; treat small LB movements as noisy. Stop pruning when removing any remaining member worsens CV.
  - `52860091:e5#1` (hms-harmful-brain-ac, Grandmaster; steps 52860091:17->18, 52860091:19->20, 52860091:20->21, 52860091:21->22): First evaluate each candidate model variant in isolation to establish its standalone quality. Then test pairwise and higher-order combinations. If adding a variant worsens the ensemble despite being decent alone, try weighted blending before discarding it. If a variant is much stronger solo than others, test it alone before averaging — uniform averaging can dilute a strong model. Stop uniform-weight search when adding members hurts, and switch to weighted blending.
  - `60264017:e2#1` (learning-agency-lab-, Master; steps 60264017:2->3, 60264017:3->4, 60264017:4->5, 60264017:5->6): Swap one ensemble member at a time against the current best blend, submit, and compare. If the score improves, keep the change and try the next swap. If it regresses, revert that member and try a different candidate. Pre-compute per-member rounding thresholds offline via CV before submitting. Stop when available candidates are exhausted or consecutive swaps regress.

## 21. revert_and_isolate_after_multi_change_regression  [L3]  —  3 kernels, 3 comps, 3 items

- **Context:** Multiple changes (e.g., architecture + hyperparameters, optimizer + bug fix, checkpoint + kernel size) were bundled in one submission and the leaderboard score regressed.
- **Action:** Revert to the last known good configuration. Then re-apply each change individually in separate submissions to isolate the cause. Prioritize reverting the most disruptive/speculative change first while keeping clearly correct fixes. Do not continue building on the regressed version. Limit to 2-3 isolation submissions before deciding.
- **Exceptions:** When one change is clearly beneficial (e.g., a bug fix) and another is speculative, you can selectively revert only the speculative component rather than reverting everything (77129691:e11#1).
- **Support:** kernels 53762022, 77129691, 7823861; comps equity-post-hct-survival-pre, google-quest-challenge, hms-harmful-brain-activity-c; tiers {'Contributor': 1, 'Master': 1, nan: 1}; episode reached new best: {'no': 2, 'yes': 1}
- **Cells:** L3/probe/new_idea/part1
- **Examples:**
  - `53762022:e2#2` (hms-harmful-brain-ac, Contributor; steps 53762022:6->7): After a large regression from multiple simultaneous changes, revert to the last known good configuration and re-test each change individually. Do not continue building on the regressed version. Submit intermediate versions even if they seem minor, to maintain a diagnostic trail.
  - `77129691:e11#1` (equity-post-hct-surv, Master; steps 77129691:21->22): Revert only the speculative component while keeping the clearly correct fix. Use the revert as an opportunity to also tune related hyperparameters that the new component may have disrupted. If the revert recovers or exceeds the previous best, confirm the speculative component was harmful and move on.
  - `7823861:e7#1` (google-quest-challen, nan; steps 7823861:29->30, 7823861:30->31): Revert the most disruptive change (architecture) while keeping the simpler changes (hyperparameters), then resubmit to isolate the effect. If the score partially recovers, the reverted component was harmful. Avoid bundling architectural changes with hyperparameter changes in a single experiment.

## 22. single_probe_before_ensemble_integration  [L3]  —  3 kernels, 3 comps, 3 items

- **Context:** A new model or new model artifacts are available and their standalone quality is unknown, and you want to decide whether to add them to an existing ensemble or stacking pipeline.
- **Action:** Test the new component in isolation first (standalone score or single-change submission). If standalone performance is far worse than existing components, do not integrate. If integrated as a single probe and LB regresses or fails to improve, abandon the addition quickly rather than tuning integration details. Limit to at most two submissions on this binary include/exclude test.
- **Exceptions:** A weak standalone model can still help through diversity (17616127 counter_evidence), so this heuristic may discard useful diverse members. Also, confounded changes (59253662) can mask the true signal.
- **Support:** kernels 17616127, 59253662, 77276039; comps commonlitreadabilityprize, equity-post-hct-survival-pre, learning-agency-lab-automate; tiers {'Contributor': 2, 'Expert': 1}; episode reached new best: {'no': 3}
- **Cells:** L3/probe/new_resource
- **Examples:**
  - `17616127:e12#1` (commonlitreadability, Contributor; steps 17616127:45->46, 17616127:46->47, 17616127:48->49): Before integrating new model artifacts into a complex ensemble, first test a single fold or single model alone to establish a standalone baseline. If the standalone score is far worse than existing components, averaging all folds of that model family is unlikely to close the gap enough to help the ensemble. Abandon the direction if the full-fold average still underperforms existing individual components.
  - `59253662:e6#1` (learning-agency-lab-, Contributor; steps 59253662:26->27, 59253662:28->29): Treat adding a new stacking member as a single probe: integrate it in one change, submit, and compare against baseline. If the leaderboard score regresses or fails to improve, abandon the idea quickly rather than tuning integration details. A small regression suggests the new predictions add noise or redundancy rather than complementary signal.
  - `77276039:e4#1` (equity-post-hct-surv, Expert; steps 77276039:15->16, 77276039:16->17): Submit the ensemble both with and without the candidate member. Compare LB scores directly. If the candidate hurts performance, exclude it. Do not spend more than two submissions on this binary test before moving on.

## 23. use_unsubmitted_runs_to_narrow_search  [L3]  —  3 kernels, 3 comps, 3 items

- **Context:** When exploring a continuous parameter space and submission budget is limited.
- **Action:** Use local validation or unsubmitted runs to narrow the search space cheaply. Only submit when you have converged on a promising region or want to verify a candidate. After a score drop, reverse direction and try multiple candidate values without submitting before spending another submission.
- **Exceptions:** 53747598 found that CV-guided selection did not transfer to LB for blend weights, so local validation may mislead for post-processing parameters.
- **Support:** kernels 27825577, 53747598, 77386286; comps amex-default-prediction, equity-post-hct-survival-pre, hms-harmful-brain-activity-c; tiers {'Expert': 2, 'Master': 1}; episode reached new best: {'yes': 2, 'no': 1}
- **Cells:** L3/sweep/new_idea/part1
- **Examples:**
  - `27825577:e3#2` (amex-default-predict, Expert; steps 27825577:6->7, 27825577:7->8, 27825577:8->9, 27825577:9->10): After a regression from moving a parameter in one direction, explore the opposite direction with a large step to establish bounds (overshoot deliberately). Use fast validation (not LB submission) for these exploratory runs. Once both directions have been probed, narrow in on the best region and submit only the refined candidate. This brackets the optimum with minimal LB submissions.
  - `53747598:e8#1` (hms-harmful-brain-ac, Master; steps 53747598:30->31, 53747598:31->32, 53747598:32->33, 53747598:33->34): Evaluate candidate weight vectors on local CV/OOF first without submitting. Try 3-5 diverse vectors (near-equal, skewed toward each model, CV-guided). Only submit the best CV candidate to the leaderboard. If the submitted score doesn't beat the previous best, stop the sweep—the gain from weight tuning alone is likely exhausted.
  - `77386286:e2#2` (equity-post-hct-surv, Expert; steps 77386286:5->6, 77386286:6->7, 77386286:7->8, 77386286:8->9): After a score drop, reverse direction and try multiple candidate values without submitting (saving versions). Only submit when you have converged on a promising region or want to verify. Use unsubmitted runs to narrow the search space cheaply before spending a submission.

## 24. blend_weight_tuning_stop_criterion  [L3]  —  3 kernels, 3 comps, 3 items

- **Context:** You are tuning continuous blend weights for a small ensemble (2-4 models) using leaderboard feedback, and the leaderboard may be noisy.
- **Action:** Try 3-5 perturbations around the current best weights in steps of 0.05-0.15. If the first perturbation worsens, move in the opposite direction. If after ~4 attempts none beats the baseline, stop—the weights are near-optimal. On very noisy leaderboards (few evaluation rows), make only 2-3 structurally distinct attempts rather than fine-grained sweeps.
- **Exceptions:** 77386286:e2#1 notes the author did not follow a strictly systematic grid and some jumps were large.
- **Support:** kernels 18837555, 53762022, 77386286; comps commonlitreadabilityprize, equity-post-hct-survival-pre, hms-harmful-brain-activity-c; tiers {'Expert': 2, 'Contributor': 1}; episode reached new best: {'yes': 2, 'no': 1}
- **Cells:** L3/sweep/new_idea/part2
- **Examples:**
  - `18837555:e5#2` (commonlitreadability, Expert; steps 18837555:13->14, 18837555:14->15, 18837555:15->16): Make a small number of structurally distinct attempts (2-3) rather than fine-grained sweeps. After finding a configuration that improves, try one refinement. If the refinement regresses, accept the previous best and stop. Do not chase small score differences on a noisy leaderboard.
  - `53762022:e7#1` (hms-harmful-brain-ac, Contributor; steps 53762022:13->14, 53762022:14->15, 53762022:15->16, 53762022:16->17): Try 3-5 perturbations around the current best weights, varying by steps of 0.05-0.15. If the first perturbation worsens, move in the opposite direction. If after ~4 attempts none beats the baseline, stop—the weights are likely near-optimal and further tuning yields noise-level differences.
  - `77386286:e2#1` (equity-post-hct-surv, Expert; steps 77386286:2->3, 77386286:3->4, 77386286:4->5, 77386286:5->6): Start by swapping weights of the two non-dominant models to identify which direction helps. Then increase the weight of the best-contributing model in steps of ~0.05-0.10 while decreasing others. When a change causes a drop, reverse direction. When two consecutive improvements are marginal (<0.001), bracket the optimum and stop. Submit only the most promising configurations to conserve submission budget.

## 25. evaluate_checkpoints_individually_then_combine  [L3]  —  3 kernels, 3 comps, 3 items

- **Context:** Multiple trained checkpoint sets (from different training runs, architectures, or sources) are available, and swapping checkpoints in the inference pipeline is cheap (e.g., a path change).
- **Action:** Evaluate each checkpoint set individually via separate submissions. Discard any set that causes a large regression. Then combine the top-performing sets into one ensemble. If the combined result doesn't beat the individual best or the pre-existing baseline, revert to the previous best. Prioritize swapping to a clearly superior checkpoint before tuning inference-time settings around it.
- **Exceptions:** none
- **Support:** kernels 13521245, 18426209, 52551258; comps commonlitreadabilityprize, hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 1, 'Expert': 2}; episode reached new best: {'yes': 1, 'no': 2}
- **Cells:** L3/sweep/new_resource
- **Examples:**
  - `13521245:e2#3` (ranzcr-clip-catheter, Grandmaster; steps 13521245:6->7): Prioritize swapping to the best available checkpoint before tuning any inference parameters. Make the checkpoint switch and resolution adjustment together if the new model expects a different input size. Then sweep resolution in small steps around the expected optimum.
  - `18426209:e6#1` (commonlitreadability, Expert; steps 18426209:7->8, 18426209:8->9): First test the new checkpoint source by swapping all folds at once. If the score regresses, use per-fold CV scores to identify which folds improved and which worsened, then construct a mixed checkpoint list keeping the best fold from whichever source has the lower fold-level error. Hard-code the paths to make the selection explicit and reproducible.
  - `52551258:e13#1` (hms-harmful-brain-ac, Expert; steps 52551258:22->23, 52551258:23->24, 52551258:24->25, 52551258:25->26): Try each checkpoint set individually first to identify which ones perform well. If a set causes a large regression, immediately discard it. Then combine the top-performing sets into one ensemble. If the combined result doesn't beat the individual best or the pre-existing baseline, stop and revert to the previous best approach.

## 26. fold_count_increase_diminishing_returns  [L2]  —  3 kernels, 2 comps, 3 items

- **Context:** When tuning the number of CV folds on a moderately-sized dataset (roughly 6K–17K samples) and you already have a working fold count that produces good scores.
- **Action:** Increase fold count modestly (e.g., 5→10 or 10→15) rather than aggressively (e.g., 15→20 or 5→30). If increasing folds causes leaderboard regression on two or more attempts, revert to the lower count. Excessively high fold counts can produce validation sets too small for reliable metric estimation and noisier individual models that hurt the ensemble. On very small datasets, moderate increases help by giving more training data per fold.
- **Exceptions:** On very small datasets (~6K), larger fold increases (e.g., 10→15) can yield meaningful gains because marginal training examples matter more (7253130:e5#2). The optimal fold count is dataset- and metric-dependent.
- **Support:** kernels 58130512, 60197293, 7253130; comps google-quest-challenge, learning-agency-lab-automate; tiers {'Master': 1, 'Expert': 1, 'Contributor': 1}; episode reached new best: {'no': 2, 'yes': 1}
- **Cells:** L2/cv_fold_strategy
- **Examples:**
  - `58130512:e30#2` (learning-agency-lab-, Master; steps 58130512:91->92, 58130512:94->95, 58130512:95->96): If increasing fold count (e.g., 15→20) causes a leaderboard regression on two separate attempts while other settings are similar, keep the lower fold count. More folds can overfit to training data or produce noisier individual models that hurt the ensemble on the public test set.
  - `60197293:e5#3` (learning-agency-lab-, Expert; steps 60197293:29->30): Try increasing fold count substantially (e.g., 5→30) and check whether OOF QWK stabilizes. If runtime becomes prohibitive or validation sets become too small for reliable metric estimation, reduce to an intermediate value (e.g., 10). Do not submit until you have confirmed CV improvement.
  - `7253130:e5#2` (google-quest-challen, Contributor; steps 7253130:11->12): After exhausting easy gains from dropout and learning rate, increase the number of CV folds (e.g., from 10 to 15). This simultaneously increases per-fold training set size and ensemble diversity. Expect meaningful gains on small datasets where the marginal training examples matter.

## 27. discretize_predictions_to_match_target_levels  [L2]  —  3 kernels, 2 comps, 3 items

- **Context:** Model outputs continuous predictions but ground-truth labels take only a few discrete values (e.g., crowd-rating averages, ordinal scores), and the metric is rank-based or ordinal (Spearman, QWK).
- **Action:** Post-process predictions by snapping/rounding them to the known discrete target levels using optimized thresholds rather than naive uniform midpoints. Start with columns/targets that have the most discrete structure (binary or few-level). Expand one column at a time, validating via OOF metric. If a batch of changes causes regression, revert to the last known-good version rather than attempting incremental fixes.
- **Exceptions:** Not all target columns benefit equally from discretization; scaling all columns at once can hurt (7548275:e6#1 v24 regression). Aggressive intermediate binning or too many simultaneous threshold changes can cause large regressions (7823861:e5#1 v22→v23).
- **Support:** kernels 55621328, 7548275, 7823861; comps google-quest-challenge, learning-agency-lab-automate; tiers {'Master': 1, 'Expert': 1, nan: 1}; episode reached new best: {'no': 1, 'yes': 2}
- **Cells:** L2/postprocessing_calibration
- **Examples:**
  - `55621328:e44#3` (learning-agency-lab-, Master; steps 55621328:133->134): Always use OOF-optimized rounding thresholds rather than naive uniform midpoints. The v134 experiment with [1.5,2.5,3.5,4.5,5.5] dropped from 0.82503 to 0.80343, a ~0.02 QWK loss, demonstrating that optimized thresholds are critical for ordinal regression in skewed distributions.
  - `7548275:e6#1` (google-quest-challen, Expert; steps 7548275:21->22, 7548275:23->24, 7548275:24->25, 7548275:25->26): Start by applying discretization/scaling to columns with the most discrete target distributions (e.g., binary or few-level columns). Test scaling all columns; if it regresses, revert to a curated subset. Expand the subset one or a few columns at a time, using per-column OOF Spearman comparisons to decide which columns benefit. Stop when marginal gains become negligible.
  - `7823861:e5#1` (google-quest-challen, nan; steps 7823861:17->18, 7823861:18->19, 7823861:19->20, 7823861:22->23): For each target column, examine the distribution of raw predictions and the known discrete levels. Set thresholds to snap predictions to the nearest discrete level, starting with the most binary/sparse columns (where most values are 0 or 1). Apply conservative thresholds first (only snap extreme values), submit, then gradually add intermediate bins. If a batch of changes causes regression, revert to the last good version rather than trying to fix individual thresholds incrementally.

## 28. probe_class_reweighting_carefully_for_imbalanced_targets  [L2]  —  3 kernels, 2 comps, 3 items

- **Context:** Binary or ordinal classification with class imbalance, where the competition metric weights classes asymmetrically or is rank-sensitive (e.g., normalized Gini, QWK), and a GBDT or AutoML model is already performing well.
- **Action:** Probe class/sample reweighting in isolation (one parameter at a time). For GBDT, sweep scale_pos_weight exponent in small steps and submit each. If the custom metric already guides model selection or the model's native ranking ability handles the asymmetry, revert weights when OOF/LB does not improve. Avoid naive oversampling (e.g., SMOTE) for ordinal targets—prefer threshold optimization or loss-based weighting instead.
- **Exceptions:** For GBDT scale_pos_weight, sweeping the exponent did yield improvement in one case (27656049), so the revert-if-no-gain guidance mainly applies when the metric is already used for model selection (27502740) or when the reweighting method doesn't respect target structure (59253662:SMOTE on ordinal).
- **Support:** kernels 27502740, 27656049, 59253662; comps amex-default-prediction, learning-agency-lab-automate; tiers {'Grandmaster': 1, 'Expert': 1, 'Contributor': 1}; episode reached new best: {'no': 2, 'yes': 1}
- **Cells:** L2/training_data_balancing
- **Examples:**
  - `27502740:e2#1` (amex-default-predict, Grandmaster; steps 27502740:2->3, 27502740:4->5): Probe sample weights matching the metric's class asymmetry on a single run. If OOF or LB score does not improve, revert weights but keep the custom metric for model selection. The ranking-based component of metrics like normalized Gini is often better served by the model's native ranking ability than by loss reweighting.
  - `27656049:e8#1` (amex-default-predict, Expert; steps 27656049:23->24, 27656049:25->26): Sweep the exponent in small steps (e.g., 1/2, 1/3, 1/4) around the current value. Submit each to leaderboard. If increasing the weight hurts and decreasing also hurts, the current exponent is near-optimal. Do not change other hyperparameters simultaneously during this sweep.
  - `59253662:e7#2` (learning-agency-lab-, Contributor; steps 59253662:29->30, 59253662:30->31): Avoid SMOTE for ordinal regression tasks scored by QWK. SMOTE interpolates features without respecting ordinal target structure, and gradient boosting already handles moderate imbalance well via its loss function. Prefer threshold optimization or sample weighting instead.

## 29. binary_toggle_test_for_uncertain_config  [L3]  —  3 kernels, 2 comps, 3 items

- **Context:** A single binary configuration choice (filter, preprocessing toggle, post-processing on/off) is in question and its effect is uncertain.
- **Action:** Disable the setting, submit, compare to the previous score. If the score regresses, immediately re-enable and submit to confirm recovery. Two submissions answer the question definitively. For binary toggles, evaluate locally (OOF) first if possible; submit both variants to leaderboard only if local signal is ambiguous.
- **Exceptions:** 75584724:e5#1 notes that local OOF signal may be insufficient for noisy metrics, requiring LB confirmation of both states.
- **Support:** kernels 13848868, 75584724, 75924487; comps equity-post-hct-survival-pre, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 1, 'Master': 2}; episode reached new best: {'yes': 2, 'no': 1}
- **Cells:** L3/probe/new_idea/part1
- **Examples:**
  - `13848868:e5#1` (ranzcr-clip-catheter, Grandmaster; steps 13848868:16->17, 13848868:17->18, 13848868:18->19, 13848868:19->20): When swapping in a new model, first submit with the simpler post-processing (off/raw probabilities). If the score is promising, toggle the post-processing on and compare. Always test both states for each new model before concluding which is better. Do not assume the post-processing preference transfers across model changes.
  - `75584724:e5#1` (equity-post-hct-surv, Master; steps 75584724:8->9, 75584724:9->10, 75584724:10->11): For a binary preprocessing toggle, first evaluate locally (OOF) without submitting. If local results are ambiguous, submit both variants to the leaderboard. If neither variant beats the prior best, abandon the idea and move on rather than iterating further on the same lever.
  - `75924487:e4#1` (equity-post-hct-surv, Master; steps 75924487:6->7, 75924487:7->8): Disable the setting, submit, compare to the previous score. If the score regresses, immediately re-enable and submit to confirm recovery. Two submissions answer the question definitively. Do not explore further variants if the toggle clearly resolves the question.

## 30. revert_before_layering_on_regression  [L3]  —  3 kernels, 2 comps, 3 items

- **Context:** When a change (checkpoint swap, feature removal, new component) causes a leaderboard regression and you want to test an orthogonal new idea.
- **Action:** Test the new idea on top of the last-known-best configuration, not on top of the regressed version. Stacking an unproven change on an already-regressed baseline makes attribution impossible. Revert first, then apply the new idea in isolation.
- **Exceptions:** none
- **Support:** kernels 17371717, 55621328, 55987255; comps commonlitreadabilityprize, learning-agency-lab-automate; tiers {'Master': 3}; episode reached new best: {'no': 3}
- **Cells:** L3/probe/new_idea/part2
- **Examples:**
  - `17371717:e3#1` (commonlitreadability, Master; steps 17371717:6->7): Before reverting to the previous best, inspect the new code for initialization bugs and forward-pass logic errors. Fix the most likely issues (e.g., parameter initialization, gradient flow through softmax) and resubmit once. If the fix recovers most of the gap, continue iterating; if not, revert or pivot.
  - `55621328:e44#2` (learning-agency-lab-, Master; steps 55621328:130->131, 55621328:133->134): When a change regresses, test your new idea on top of the last-known-best configuration first, not on top of the regressed one. Stacking an unproven post-processing step on an already-regressed checkpoint makes it impossible to attribute gains or losses. If you must iterate, revert to the best baseline before adding the new transformation.
  - `55987255:e24#2` (learning-agency-lab-, Master; steps 55987255:151->152): If ablation confirms a feature's value (removal causes regression), revert to the version with the feature before exploring other changes. Only abandon a confirmed-valuable component if you have a concrete replacement hypothesis ready. Changing multiple things simultaneously (removing features + changing other settings) makes it impossible to attribute the regression cleanly.

## 31. do_not_greedily_revert_small_regressions_in_noisy_lb  [L3]  —  3 kernels, 2 comps, 3 items

- **Context:** When the leaderboard metric is noisy (few public test rows, or observed run-to-run variance is high) and a regression from a change is small (within the noise margin).
- **Action:** Do not immediately revert a small regression. Continue the sweep to cover all candidate configurations. After the full sweep, select the best-scoring configuration rather than greedily reverting each individual regression. This avoids being misled by noise on single submissions.
- **Exceptions:** none
- **Support:** kernels 13542132, 13702907, 18523075; comps commonlitreadabilityprize, ranzcr-clip-catheter-line-cl; tiers {'Master': 1, 'Contributor': 1, 'Expert': 1}; episode reached new best: {'no': 1, 'yes': 2}
- **Cells:** L3/sweep/new_idea/part1
- **Examples:**
  - `13542132:e2#1` (ranzcr-clip-catheter, Master; steps 13542132:4->5, 13542132:5->6, 13542132:7->8): Before concluding a change helped or hurt, re-run the identical notebook at least once to estimate submission noise. If the variance across identical runs exceeds the observed delta from the change, do not trust a single regression as evidence the change is harmful. Only accept a change if it consistently outperforms across multiple runs.
  - `13702907:e8#2` (ranzcr-clip-catheter, Contributor; steps 13702907:21->22, 13702907:22->23): When a new-best score is achieved, re-run at least twice with no code changes to estimate the noise floor. Only count an improvement as real if it exceeds 2× the observed run-to-run variance. Do not chase small regressions from cosmetic or no-op changes.
  - `18523075:e6#2` (commonlitreadability, Expert; steps 18523075:13->14, 18523075:14->15): Do not immediately revert a small regression. Continue the sweep to cover all candidate members. After the sweep, select the best-scoring configuration rather than greedily reverting each regression. This avoids being misled by noise on individual submissions.

## 32. add_diverse_backbone_and_rebalance_weights  [L2]  —  3 kernels, 1 comps, 3 items

- **Context:** You have a working multi-model ensemble of pretrained transformer backbones and want to improve it further, especially when existing members share similar architecture families or the score has plateaued.
- **Action:** Add a new member from a different architecture family or training run. Start with a modest initial blend weight (e.g., 0.1 or roughly uniform). Submit to confirm it doesn't hurt. Then re-optimize blend weights using OOF predictions, down-weighting members that contribute least. If the new member yields only marginal or no improvement, consider replacing the weakest existing member with a stronger backbone rather than continuing to tune weights.
- **Exceptions:** Gains from backbone diversity can be modest (e.g., 0.00079 RMSE or flat). In 18851026, the author later replaced the diverse backbone (T5) with more variants of the dominant family (RoBERTa), suggesting backbone diversity alone isn't always decisive. In 18350823, adding a fourth member with modest weight produced essentially no improvement.
- **Support:** kernels 18350823, 18523075, 18851026; comps commonlitreadabilityprize; tiers {'Expert': 2, 'Master': 1}; episode reached new best: {'no': 1, 'yes': 2}
- **Cells:** L2/ensemble_member_addition
- **Examples:**
  - `18350823:e9#1` (commonlitreadability, Expert; steps 18350823:19->20): Add the new member's predictions as a separate array, assign it a modest initial blend weight (e.g., 0.1), reduce weights of weaker existing members proportionally, and submit to check for improvement. If the new member doesn't help, remove it before trying other levers.
  - `18523075:e1#1` (commonlitreadability, Expert; steps 18523075:1->2, 18523075:2->3): First add the new member with roughly uniform weights and submit to confirm it doesn't hurt. Then use OOF predictions to re-optimize blend weights, down-weighting members that contribute least. If weight tuning doesn't yield meaningful gains, consider replacing the weakest member with a stronger backbone rather than continuing to tune weights.
  - `18851026:e4#1` (commonlitreadability, Master; steps 18851026:9->10): Integrate a pretrained model from a different architecture family (e.g., T5 when you already have RoBERTa). Extract embeddings using the same stacking pipeline (SVR/Ridge on embeddings), then blend with existing predictions. Start with a high weight on the new component to test its contribution, then adjust.

## 33. sweep_resolution_around_canonical_for_fine_detail_tasks  [L2]  —  3 kernels, 1 comps, 3 items

- **Context:** When the task involves fine spatial detail (e.g., medical imaging with catheters/lines) and the model architecture accepts variable or multiple input resolutions, and you want to push accuracy beyond a working baseline.
- **Action:** Start at the model's canonical or training resolution, then sweep in steps (one step above and below for EfficientNet variants, or ~100px steps for fully convolutional models). Submit each, pick the resolution that scores best. Two to three trials bracket the optimum. If a higher-resolution checkpoint exists, switch both weights and resolution simultaneously. Expect diminishing returns and possible degradation past a peak; stop when both neighbors of the current best are worse.
- **Exceptions:** Changing both model architecture and resolution simultaneously confounds the signal (13577502:e3#1 v8). Single confirmation runs may not distinguish signal from noise when variance is ~0.002 (13702907:e8#1). The resolution effect may be small relative to model/training differences.
- **Support:** kernels 13521245, 13577502, 13702907; comps ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 1, 'Expert': 1, 'Contributor': 1}; episode reached new best: {'yes': 3}
- **Cells:** L2/input_resolution_selection
- **Examples:**
  - `13521245:e2#1` (ranzcr-clip-catheter, Grandmaster; steps 13521245:6->7, 13521245:8->9): Start with the canonical resolution for the model variant, then try one step above and one below. Pick the resolution that scores best. For EfficientNet B7, the canonical resolution is 600; try 528 and 600 and keep the winner. Two or three trials suffice to bracket the optimum.
  - `13577502:e3#1` (ranzcr-clip-catheter, Expert; steps 13577502:6->7, 13577502:9->10, 13577502:10->11, 13577502:11->12): Start well above the training resolution (e.g., 1.5–2×), submit, then sweep upward in ~100px steps. If a step regresses or fails (OOM), step back one notch. Stop when you have tried one step above and one below the current best and both are worse. Expect diminishing returns and possible degradation past a peak.
  - `13702907:e8#1` (ranzcr-clip-catheter, Contributor; steps 13702907:20->21, 13702907:21->22): Increase input resolution to the next available checkpoint size, update both the decoder target size and the model weights path simultaneously, then submit. If the score improves, re-run once to confirm it is not noise. If confirmed, lock in that resolution.

## 34. tta_must_match_training_augmentation  [L2]  —  2 kernels, 2 comps, 3 items

- **Context:** You have a trained model and want to apply test-time augmentation (TTA) using transformations (shifted crops, geometric augmentations) that the model may or may not have seen during training.
- **Action:** Only apply TTA with transformations the model was trained on or that are deterministic/invertible (e.g., horizontal flip). If the model was trained with temporal crop augmentation, use multi-crop TTA (left/center/right) and average softmax outputs. If the model was trained only on center crops or without heavy geometric augmentation, avoid stochastic or out-of-distribution TTA (shifted windows, random rotations) as these likely add noise. Test TTA on one model group first; if score does not improve, revert rather than tuning TTA weights.
- **Exceptions:** Earlier in 53424936 history, TTA helped even with models not explicitly trained on shifted crops, suggesting model architecture/capacity may sometimes compensate. The rule is model-dependent.
- **Support:** kernels 15372370, 53424936; comps hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Expert': 1, 'Master': 2}; episode reached new best: {'yes': 2, 'no': 1}
- **Cells:** L2/test_time_augmentation
- **Examples:**
  - `15372370:e5#2` (ranzcr-clip-catheter, Expert; steps 15372370:8->9, 15372370:10->11): For medical image classification where spatial position is semantically meaningful, prefer deterministic geometric TTA (horizontal flip with explicit averaging) over stochastic augmentation TTA. Stochastic rotations/shifts at test time can corrupt position-dependent features and degrade performance even when averaged over multiple runs.
  - `53424936:e3#1` (hms-harmful-brain-ac, Master; steps 53424936:8->9, 53424936:11->12): Enable inference on all available temporal crops (e.g., left/center/right), softmax each independently, then average the probability distributions before ensembling across models. First enable on one model group with debug prints to verify crop predictions are reasonable, then extend to all groups.
  - `53424936:e9#1` (hms-harmful-brain-ac, Master; steps 53424936:24->25, 53424936:25->26): Enable TTA on one model group first and submit. If the score does not improve, the shifted views likely add noise for models not trained on them. Revert and move on rather than tuning TTA weights. Do not combine TTA removal with other large changes (like removing model groups) in the same submission, or you cannot attribute the score change.

## 35. verify_ensemble_integrity_before_modifying  [L3]  —  2 kernels, 2 comps, 3 items

- **Context:** You have a large ensemble at a known best score and want to either prune members or refactor the pipeline. Individual components may score worse than the ensemble.
- **Action:** Before making algorithmic changes, verify the current ensemble reproduces the baseline score. When pruning, remove members in small batches and submit; if score worsens, reverse rather than pruning further. When refactoring infrastructure, submit to confirm no regression before proceeding to new experiments. Keep pruning/refactoring and experimentation in separate submissions.
- **Exceptions:** When the public LB has very few samples (e.g., ~7 rows), even small-batch pruning results are noisy and hard to attribute; one-at-a-time removal is more informative but costlier in submissions.
- **Support:** kernels 18550705, 52200959; comps commonlitreadabilityprize, hms-harmful-brain-activity-c; tiers {'Master': 3}; episode reached new best: {'no': 3}
- **Cells:** L3/consolidate/new_idea
- **Examples:**
  - `18550705:e5#1` (commonlitreadability, Master; steps 18550705:11->12, 18550705:12->13): Remove a small batch of suspected weak members and submit. If the score worsens, reverse the pruning rather than pruning further. Do not prune aggressively in a single step when the evaluation metric is noisy (few public LB samples), because you cannot reliably attribute the regression to specific removals.
  - `52200959:e5#1` (hms-harmful-brain-ac, Master; steps 52200959:23->24): When decomposing an ensemble for refactoring, record each component's standalone score. To reassemble, use all components weighted by inverse error (or inverse LB score). Verify the reassembled ensemble matches the original score before moving on. Do not drop components that seem weak individually — they may contribute diversity.
  - `52200959:e5#2` (hms-harmful-brain-ac, Master; steps 52200959:24->25, 52200959:25->26): After recovering a target score, submit refactoring changes to verify they don't regress. Only proceed to new experiments (new architectures, new data) once the refactored pipeline reproduces the baseline score exactly. Keep refactoring and experimentation in separate submissions.

## 36. systematic_inference_pipeline_debugging_on_near_random_score  [L3]  —  2 kernels, 2 comps, 3 items

- **Context:** Leaderboard score is drastically lower than expected (near random) despite a model with strong training/CV metrics, indicating a pipeline bug rather than a weak model.
- **Action:** Systematically check each inference pipeline stage: (1) correct checkpoint loaded, (2) model in eval mode, (3) correct input normalization, (4) no weight-loading conflicts (e.g., strict=False masking errors, pretrained flag overwriting checkpoint), (5) prediction value scaling matches submission format. Print raw prediction statistics (min, max, mean) and compare against sample submission ranges. Fix one thing per submission to isolate the cause.
- **Exceptions:** AUC is theoretically scale-invariant, so prediction scaling fixes may indicate a platform-specific issue rather than a true scaling problem.
- **Support:** kernels 15173072, 7573212; comps google-quest-challenge, ranzcr-clip-catheter-line-cl; tiers {'Contributor': 3}; episode reached new best: {'yes': 3}
- **Cells:** L3/fix/bug_or_error
- **Examples:**
  - `15173072:e2#1` (ranzcr-clip-catheter, Contributor; steps 15173072:7->8, 15173072:8->9, 15173072:10->11, 15173072:11->12): Systematically check each stage of the inference pipeline in order: (1) correct checkpoint loaded, (2) model in eval mode, (3) correct input normalization, (4) no weight-loading conflicts (strict=False masking errors, pretrained flag overwriting checkpoint), (5) prediction scaling matches submission format. Fix one thing per submission to isolate the cause. Inspect raw prediction values before writing submission.
  - `15173072:e2#3` (ranzcr-clip-catheter, Contributor; steps 15173072:11->12): Before submitting, compare your raw prediction statistics (min, max, mean) against the sample submission's value ranges. If the sample submission has values in [0,100] and your predictions are in [0,1], scale accordingly. Always print prediction summaries as a sanity check.
  - `7573212:e1#1` (google-quest-challen, Contributor; steps 7573212:1->2, 7573212:2->3): Fix all identified bugs in one pass, then immediately attempt to run the notebook. If a new error surfaces, fix it in a minimal follow-up edit before submitting. Do not submit until the notebook executes cleanly end-to-end.

## 37. fix_all_bugs_then_verify_end_to_end_before_submit  [L3]  —  2 kernels, 2 comps, 3 items

- **Context:** Adapting or refactoring a notebook that has multiple correctness issues (variable name mismatches, dead code paths, indentation errors, missing dependencies).
- **Action:** Fix all identified bugs in one pass, then immediately run the notebook end-to-end before submitting. After moving code out of conditional blocks, verify indentation matches the surrounding scope. After removing package dependencies, verify the model can still be deserialized. If a new error surfaces, fix it in a minimal follow-up edit. Do not submit until the notebook executes cleanly.
- **Exceptions:** none
- **Support:** kernels 13521245, 7573212; comps google-quest-challenge, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 1, 'Contributor': 2}; episode reached new best: {'no': 1, 'yes': 2}
- **Cells:** L3/fix/bug_or_error
- **Examples:**
  - `13521245:e4#1` (ranzcr-clip-catheter, Grandmaster; steps 13521245:11->12, 13521245:12->13): Before removing a custom package dependency, verify that the saved model can be deserialized without it by checking for custom_objects references. If the model was saved with custom layers, you must either supply those layers at load time or re-export the model in a format that doesn't need them. Do not remove the package and submit blind — test locally first.
  - `7573212:e1#1` (google-quest-challen, Contributor; steps 7573212:1->2, 7573212:2->3): Fix all identified bugs in one pass, then immediately attempt to run the notebook. If a new error surfaces, fix it in a minimal follow-up edit before submitting. Do not submit until the notebook executes cleanly end-to-end.
  - `7573212:e1#2` (google-quest-challen, Contributor; steps 7573212:2->3): After moving code out of a conditional block, verify that the indentation matches the surrounding scope before running. If the notebook is not submitted, catch the error locally and fix in a minimal follow-up edit.

## 38. probe_baseline_with_repeated_submissions  [L3]  —  2 kernels, 2 comps, 3 items

- **Context:** When starting with a pipeline whose true leaderboard performance is unknown—either because the training algorithm is stochastic (e.g., DART dropout) or because the pipeline depends on external artifacts with no local validation score.
- **Action:** Submit the unchanged pipeline multiple times (at least 2–3, up to 5–10 for highly stochastic methods) to establish a reliable baseline and measure run-to-run variance. Use the observed score range as the noise floor / minimum detectable effect size. Only treat subsequent changes as improvements if they exceed this noise band. Stop re-submitting once 3+ consecutive scores converge.
- **Exceptions:** For DART-based models, 9 re-submissions may be excessive; 4–5 may suffice once scores stabilize (28834369 counter_evidence).
- **Support:** kernels 13577502, 28834369; comps amex-default-prediction, ranzcr-clip-catheter-line-cl; tiers {'Expert': 1, 'Grandmaster': 2}; episode reached new best: {'yes': 3}
- **Cells:** L3/probe/none_visible
- **Examples:**
  - `13577502:e1#1` (ranzcr-clip-catheter, Expert; steps 13577502:1->2, 13577502:3->4): Submit the unchanged pipeline at least twice to establish a reliable baseline and measure run-to-run variance. If scores vary by more than ~1% with no code change, suspect non-determinism or external-asset differences. Use the range of observed scores, not a single run, as the true baseline before deciding whether to iterate or replace the pipeline.
  - `28834369:e1#1` (amex-default-predict, Grandmaster; steps 28834369:1->2, 28834369:2->3, 28834369:3->4, 28834369:4->5): Before tuning, submit the same unchanged notebook multiple times (5–10) and record the LB spread. Continue until scores stabilize. Use the observed range as the minimum detectable effect size; only treat HP changes as improvements if they exceed this noise band.
  - `28834369:e1#2` (amex-default-predict, Grandmaster; steps 28834369:6->7, 28834369:7->8, 28834369:8->9, 28834369:9->10): Stop re-submitting once you see 3+ consecutive identical scores. Treat the converged value as your baseline and the full observed range as your noise estimate. Then proceed to actual experimentation.

## 39. swap_backbone_when_current_architecture_plateaus  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** Performance has plateaued or regressed after tuning the current model's components (features, head architecture), and gains from incremental changes are diminishing or negative.
- **Action:** Swap the model backbone (e.g., different boosting framework, different CNN/vision backbone) rather than continuing to tune the current one. Isolate the backbone change from other modifications, reduce iteration cost (e.g., fewer CV folds), and evaluate on CV before submitting. If a head simplification caused regression, try a stronger backbone with the simpler head before reverting.
- **Exceptions:** In 55431616 the backbone swap was never submitted, so CV-competitiveness was not confirmed; the probe may have been abandoned, suggesting the swap does not always help.
- **Support:** kernels 13848868, 55431616; comps learning-agency-lab-automate, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 2}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L2/backbone_model_swap
- **Examples:**
  - `13848868:e5#2` (ranzcr-clip-catheter, Grandmaster; steps 13848868:16->17, 13848868:18->19): If simplifying the model head causes a regression, try pairing the simplified head with a stronger or different backbone before abandoning the simpler architecture. The backbone change may dominate the head design effect. Evaluate backbone swaps before reverting head changes.
  - `55431616:e6#1` (learning-agency-lab-, Grandmaster; steps 55431616:20->21, 55431616:21->22, 55431616:22->23, 55431616:23->24): When probing an alternative boosting framework: (1) first ensure the environment runs (device/dependency fixes), (2) reduce CV folds to speed iteration, (3) adapt the custom metric callback to the new library's signature, (4) configure early stopping to monitor and maximize the competition metric with save_best, (5) isolate the new model's output by disabling ensemble blending, (6) evaluate on CV before submitting. Do not submit until CV confirms competitiveness.

## 40. checkpoint_ensembling_when_single_model_plateaus  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** Multiple trained checkpoints (different epochs, architectures, or hyperparameters) are available, individual checkpoint scores are comparable with no single variant clearly dominating, and inference budget allows additional forward passes.
- **Action:** Rather than selecting the single best checkpoint, average predictions from the top 2-3 diverse checkpoint variants and re-normalize. First test each individually; if neither clearly dominates, combine them. This typically yields a larger gain than further single-checkpoint search.
- **Exceptions:** The ensembling benefit is inferred from trajectory in 52860091 rather than directly observed within that episode; rule assumes inference cost of extra forward passes is acceptable.
- **Support:** kernels 52860091, 7573212; comps google-quest-challenge, hms-harmful-brain-activity-c; tiers {'Grandmaster': 1, 'Contributor': 1}; episode reached new best: {'yes': 2}
- **Cells:** L2/checkpoint_ensembling
- **Examples:**
  - `52860091:e2#3` (hms-harmful-brain-ac, Grandmaster; steps 52860091:7->8): After identifying the top 2-3 individual checkpoints via a sweep, average their predicted probability distributions and re-normalize. This typically yields a larger gain than further single-checkpoint search.
  - `7573212:e7#1` (google-quest-challen, Contributor; steps 7573212:12->13): Rather than selecting the single best checkpoint variant, include predictions from all available checkpoint variants in the ensemble average. This adds diversity at low cost since the model architecture is already loaded. Test both individually first; if neither clearly dominates, combine them.

## 41. swap_checkpoints_with_matched_config_and_verify  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** You have multiple trained checkpoints (from different epochs, folds, or experiments) and want to select the best one(s) for inference without retraining.
- **Action:** Swap in candidate checkpoints that show better validation metrics, but ensure inference-time architecture settings (e.g., dropout rate) match each checkpoint's training configuration. Verify each swap on the leaderboard before committing, as better validation metrics do not always transfer to better LB scores.
- **Exceptions:** 49524919:e33#2 shows that checkpoints with better per-fold validation scores can yield worse LB (ConvNeXt at v150 scored 0.265), so always verify externally.
- **Support:** kernels 13702907, 49524919; comps hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Contributor': 1, 'Grandmaster': 1}; episode reached new best: {'yes': 2}
- **Cells:** L2/checkpoint_selection
- **Examples:**
  - `13702907:e6#1` (ranzcr-clip-catheter, Contributor; steps 13702907:15->16): When swapping a model checkpoint, also update the inference-time architecture (e.g., dropout rate) to match the training configuration of that checkpoint. Change both together since they are coupled; a mismatched dropout rate will degrade the checkpoint's predictions.
  - `49524919:e33#2` (hms-harmful-brain-ac, Grandmaster; steps 49524919:148->149, 49524919:149->150, 49524919:151->152, 49524919:153->154): Swap checkpoint files to variants with better per-fold validation scores, test the model group in isolation on the leaderboard, and only then incorporate into the full blend. Prefer checkpoints where the validation metric in the filename is lower (better) across most folds.

## 42. verify_cv_locally_before_submitting  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When changing CV infrastructure (fold count, model family, or averaging logic) in a competition pipeline.
- **Action:** Run a non-submitted validation pass to confirm local CV scores are reasonable before submitting, to avoid wasting submission quota on infrastructure bugs. When changing fold count, update all downstream averaging code to match the new count. When increasing folds substantially, confirm that OOF metrics stabilize before committing to the new configuration.
- **Exceptions:** none
- **Support:** kernels 28984551, 60197293; comps amex-default-prediction, learning-agency-lab-automate; tiers {'Contributor': 1, 'Expert': 1}; episode reached new best: {'no': 2}
- **Cells:** L2/cv_fold_strategy
- **Examples:**
  - `28984551:e3#2` (amex-default-predict, Contributor; steps 28984551:4->5): When changing CV folds (e.g., 5→4), update all downstream averaging code to match the new fold count. Use a non-submitted run to verify local validation before submitting, to avoid wasting submission quota on infrastructure bugs.
  - `60197293:e5#3` (learning-agency-lab-, Expert; steps 60197293:29->30): Try increasing fold count substantially (e.g., 5→30) and check whether OOF QWK stabilizes. If runtime becomes prohibitive or validation sets become too small for reliable metric estimation, reduce to an intermediate value (e.g., 10). Do not submit until you have confirmed CV improvement.

## 43. prefer_balanced_weights_over_cv_extreme_weights  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** CV-optimal blend weights heavily downweight or nearly zero out one model, but LB feedback suggests more balanced weights perform better.
- **Action:** Prefer weights closer to uniform or to the last LB-validated configuration rather than aggressively trusting CV. Extreme weight skew (nearly zeroing a model) risks overfitting to CV folds and losing diversity that helps on unseen data. When CV and LB disagree, use the more balanced weighting as default.
- **Exceptions:** Evidence is limited; when CV is highly reliable (many folds, large dataset), trusting CV may be correct.
- **Support:** kernels 15173072, 53747598; comps hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Contributor': 1, 'Master': 1}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L2/ensemble_blend_weight_tuning
- **Examples:**
  - `15173072:e5#3` (ranzcr-clip-catheter, Contributor; steps 15173072:21->22, 15173072:27->28): Start with equal-weight averaging (50/50). Unequal weights rarely help when models have similar CV scores from the same architecture. If you try unequal weights and they don't improve over equal weights, revert to equal weighting. The fold with the highest CV score is the best candidate to pair with your primary model.
  - `53747598:e8#2` (hms-harmful-brain-ac, Master; steps 53747598:31->32, 53747598:33->34): When CV and LB disagree on blend weights, prefer weights closer to uniform or to the last LB-validated weights rather than aggressively trusting CV. Extreme weight skew (nearly zeroing out a model) risks overfitting to CV folds and losing diversity that helps on unseen data.

## 44. diminishing_returns_from_adding_models_without_cv_weight_optimization  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** You are adding a third or fourth model to an existing blend and tuning weights via leaderboard submissions without reliable local CV for weight optimization.
- **Action:** Be cautious: adding more models with coarse LB-based weight tuning often yields diminishing or negative returns compared to a simpler 2-model blend. Before adding models, verify each new model improves the blend in local CV. If no reliable CV exists, test the new model solo first, then try a simple equal-weight addition. If the expanded blend doesn't beat the simpler one, revert.
- **Exceptions:** none
- **Support:** kernels 73671444, 7823861; comps equity-post-hct-survival-pre, google-quest-challenge; tiers {'Grandmaster': 1, nan: 1}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L2/ensemble_blend_weight_tuning
- **Examples:**
  - `73671444:e5#1` (equity-post-hct-surv, Grandmaster; steps 73671444:12->13, 73671444:13->14, 73671444:14->15, 73671444:15->16): First test each new model solo (weight=1.0) to establish its standalone quality. Then combine the best-performing models with a multi-way blend. Use the solo scores to inform initial weight allocation: give more weight to better solo performers. Iterate weights in coarse steps (e.g., 0.1–0.2 increments) rather than fine-tuning, since leaderboard noise dominates at small deltas.
  - `7823861:e7#2` (google-quest-challen, nan; steps 7823861:27->28, 7823861:28->29): Start from equal weights (0.5/0.5), then try shifting toward the stronger model in increments of 0.1. Test at most 2-3 values. If no improvement over the baseline, the models may be too correlated for weight tuning to help, and effort is better spent on model diversity or post-processing.

## 45. allow_negative_weights_when_positive_blend_underperforms  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** An Optuna-tuned or grid-searched weighted ensemble with positive-only normalized weights underperforms a Ridge or linear meta-learner that can assign negative/unnormalized coefficients.
- **Action:** Expand the weight search range to include negative values (e.g., [-1, 1]) and remove the sum-to-one normalization constraint. This makes the blend more expressive, approaching a linear meta-learner. If this still underperforms Ridge, the meta-learner's regularization is providing additional value beyond signed weights.
- **Exceptions:** In 73937748:e16#2, even negative weights didn't match Ridge stacking, suggesting regularization matters beyond weight sign flexibility.
- **Support:** kernels 55591012, 73937748; comps equity-post-hct-survival-pre, learning-agency-lab-automate; tiers {'Grandmaster': 1, 'Master': 1}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L2/ensemble_blend_weight_tuning
- **Examples:**
  - `55591012:e12#2` (learning-agency-lab-, Grandmaster; steps 55591012:45->46, 55591012:46->47, 55591012:47->48): Fix model training and sweep blend weights in ~0.05 increments around the suspected optimum. After identifying the best coarse value, refine with 0.01 increments. If two adjacent values give identical LB scores, the optimum is found. Avoid changing blend weights and model hyperparameters simultaneously—when you must, attribute gains by testing each independently afterward.
  - `73937748:e16#2` (equity-post-hct-surv, Master; steps 73937748:49->50): Expand the Optuna weight search range to include negative values (e.g., [-1, 1]) and remove the sum-to-one normalization constraint. This makes the weighted blend more expressive, approaching what a linear meta-learner can do. If this still underperforms Ridge, the meta-learner's regularization is likely providing value beyond just signed weights.

## 46. alternative_averaging_space_for_ensemble  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When probability-based ensemble averaging has plateaued or component models have different calibration scales, and raw logits or rank information is available.
- **Action:** Try averaging in an alternative space: either convert predictions to ranks before weighted averaging (to normalize calibration differences), or average raw logits before applying softmax (to preserve confidence magnitudes). Keep existing blend weights initially to isolate the effect of the space change, then re-tune weights under the new method if it matches or beats the baseline.
- **Exceptions:** Improvements may be modest and confounded with simultaneous weight changes (53747598:e4#1). Rank-based averaging may only tie probability-based until weights are re-tuned (15164527:e4#2).
- **Support:** kernels 15164527, 53747598; comps hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Expert': 1, 'Master': 1}; episode reached new best: {'yes': 2}
- **Cells:** L2/ensemble_blending_method
- **Examples:**
  - `15164527:e4#2` (ranzcr-clip-catheter, Expert; steps 15164527:12->13, 15164527:13->14, 15164527:14->15): After optimizing probability-based blend weights, try converting each model's predictions to ranks (argsort of argsort) before weighted averaging. Keep the same weights initially to isolate the effect of the method change. If it matches or beats probability averaging, re-tune weights under the new method.
  - `53747598:e4#1` (hms-harmful-brain-ac, Master; steps 53747598:15->16, 53747598:19->20, 53747598:20->21): Extract raw logits from each component model, then compute a weighted average in logit space before applying softmax to produce final probabilities. This preserves relative confidence magnitudes that softmax compression destroys. Build the infrastructure incrementally: first verify logit extraction works for each component, then implement the averaging and softmax in one final step before submitting.

## 47. swap_variants_in_fixed_ensemble_slot  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When you have multiple checkpoint variants or training configurations of the same base architecture (e.g., different training procedures, different fine-tuning configs) and need to choose one for an ensemble slot.
- **Action:** Try each variant in the same ensemble slot while keeping all other members fixed. Submit each configuration and keep the variant that yields the best LB score. This is higher-signal than including both variants, which may introduce correlated noise. Vary one factor at a time to avoid confounding.
- **Exceptions:** none
- **Support:** kernels 60264017, 6803050; comps google-quest-challenge, learning-agency-lab-automate; tiers {'Master': 2}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L2/ensemble_composition
- **Examples:**
  - `60264017:e2#2` (learning-agency-lab-, Master; steps 60264017:4->5): Try each variant in the same ensemble slot while keeping all other members fixed. The variant that yields the best leaderboard score wins the slot. This is higher-signal than adding both, which may introduce correlated noise. In this case, the cope variant outperformed the scale variant by +0.0017 QWK.
  - `6803050:e10#1` (google-quest-challen, Master; steps 6803050:39->40, 6803050:40->41, 6803050:41->42, 6803050:42->43): First test each checkpoint family as a homogeneous ensemble (all folds from one family). If none beats the baseline, try mixing families. Also try varying ensemble size (more folds vs. selected subset). Submit sparingly — inspect raw outputs first and only submit configurations that look promising. If no variant beats the baseline after exhaustive sweep, abandon pure checkpoint swapping and move to blending or weighting strategies.

## 48. select_dominant_member_via_lb_verification  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When two strong models alternate as the top-weighted or dominant member across local CV runs, and you cannot resolve which is better from CV alone.
- **Action:** Test each candidate as the dominant ensemble member with its best companion weights, submit both configurations, and keep the one with higher LB. Do not rely solely on CV when the candidates are close—LB verification breaks the tie. If the best pre-episode configuration used the other candidate, the advantage may be configuration-dependent.
- **Exceptions:** When submission budget is limited, use OOF correlation analysis to pre-filter before spending submissions (75924487).
- **Support:** kernels 6803050, 75145694; comps equity-post-hct-survival-pre, google-quest-challenge; tiers {'Master': 1, 'Expert': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L2/ensemble_composition
- **Examples:**
  - `6803050:e10#1` (google-quest-challen, Master; steps 6803050:39->40, 6803050:40->41, 6803050:41->42, 6803050:42->43): First test each checkpoint family as a homogeneous ensemble (all folds from one family). If none beats the baseline, try mixing families. Also try varying ensemble size (more folds vs. selected subset). Submit sparingly — inspect raw outputs first and only submit configurations that look promising. If no variant beats the baseline after exhaustive sweep, abandon pure checkpoint swapping and move to blending or weighting strategies.
  - `75145694:e14#2` (equity-post-hct-surv, Expert; steps 75145694:49->50, 75145694:50->51, 75145694:51->52): Test each candidate as the top-weighted member with its best-fitting companion weights, submit both, and keep the one with higher LB. In this episode, nn-exp-04 dominant + catboost-exp-05 base consistently outperformed nn-exp-06 dominant configurations on LB (0.69315 vs 0.69291, 0.69286).

## 49. ensemble_blend_weights_update_strategy  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When blending multiple diverse models (different architectures or different model versions) and updating the ensemble composition by adding or swapping a component model.
- **Action:** If the new component is architecturally diverse or substantially different, retune blend weights jointly across all components, weighting stronger standalone models more heavily. If the swap is a minor incremental upgrade of an existing component, first try keeping blend coefficients fixed—only retune if the score does not improve. Adding a third diverse model can beat a two-model blend even if individually weaker.
- **Exceptions:** Marginal gains from adding weaker diverse models may be negligible (e.g., 0.0004 improvement); the fixed-coefficient strategy for incremental upgrades was only validated in one case and may not generalize.
- **Support:** kernels 18423958, 77450317; comps commonlitreadabilityprize, equity-post-hct-survival-pre; tiers {'Master': 1, 'Grandmaster': 1}; episode reached new best: {'yes': 2}
- **Cells:** L2/ensemble_composition_and_weights_joint
- **Examples:**
  - `18423958:e5#2` (commonlitreadability, Master; steps 18423958:12->13): Combine at least 2-3 architecturally diverse transformer backbones (e.g., encoder-only, encoder-decoder, distilled) with fold-averaged predictions per backbone. Weight stronger standalone models more heavily (e.g., 0.6) and weaker ones less (0.4). Adding a third diverse model often beats a two-model blend even if the third model is individually weaker.
  - `77450317:e11#3` (equity-post-hct-surv, Grandmaster; steps 77450317:22->23, 77450317:25->26): When swapping to a substantially different model version, retune blend coefficients jointly. When upgrading to a nearby incremental version, try keeping blend coefficients fixed first—if the score improves, the coefficients are still adequate. Only retune if the score doesn't improve.

## 50. ensemble_seed_fold_averaging  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** A trained model (neural network or transformer) scores well but predictions are noisy, and multiple checkpoints from different random seeds or CV folds are available without changing the training recipe.
- **Action:** Average predictions across all available fold checkpoints first for a meaningful variance-reduction gain, then add additional seed/repeat runs incrementally. Sweep the repeat count upward in small increments while score improves; when a step regresses, treat the previous value as the optimum and stop. Do not change other hyperparameters simultaneously, as confounded changes make regressions uninterpretable.
- **Exceptions:** Changing multiple knobs (e.g., architecture settings and repeat count) at once can cause large regressions that are hard to diagnose (77129691 v8→v9).
- **Support:** kernels 55621328, 77129691; comps equity-post-hct-survival-pre, learning-agency-lab-automate; tiers {'Master': 2}; episode reached new best: {'yes': 2}
- **Cells:** L2/ensemble_seed_fold_averaging
- **Examples:**
  - `55621328:e16#2` (learning-agency-lab-, Master; steps 55621328:44->45, 55621328:45->46): Average predictions across all k fold checkpoints first (expect a meaningful gain from variance reduction). Then add full-train checkpoints from different random seeds to the average. Each addition should yield diminishing but positive returns. Keep the same rounding thresholds unless local validation suggests otherwise.
  - `77129691:e3#1` (equity-post-hct-surv, Master; steps 77129691:4->5, 77129691:5->6, 77129691:6->7, 77129691:7->8): Sweep the repeat count upward in small increments (+1 or +2) while score improves. When a step regresses, treat the previous value as the optimum and stop. Do not change other hyperparameters simultaneously when searching for the optimal repeat count, because confounded changes make regression uninterpretable.

## 51. incremental_feature_config_sweep  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When hyperparameters are already tuned or the model is established, and you suspect the feature configuration (e.g., vocabulary size, aggregation functions) is suboptimal relative to dataset characteristics.
- **Action:** Change one feature-configuration lever at a time (e.g., one max_features value or one aggregation function). Submit or check CV after each change. If the new setting degrades score, revert before trying the next option. Avoid stacking multiple untested feature changes simultaneously, as confounding makes it hard to isolate which change helped or hurt.
- **Exceptions:** Both source items note that authors sometimes changed two things at once (alpha + max_features; var + removing 'last'), confounding results. The rule is aspirational—strict isolation is not always followed in practice.
- **Support:** kernels 27825577, 7676170; comps amex-default-prediction, google-quest-challenge; tiers {'Expert': 1, 'Contributor': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L2/feature_aggregation_config
- **Examples:**
  - `27825577:e5#1` (amex-default-predict, Expert; steps 27825577:14->15, 27825577:15->16, 27825577:16->17, 27825577:17->18): Try adding one aggregation at a time (sum, var) and toggling existing ones (removing 'last' for categoricals). Submit only after checking CV. If the new aggregation degrades both CV and LB, revert it before trying the next. Do not stack multiple untested aggregations simultaneously.
  - `7676170:e1#1` (google-quest-challen, Contributor; steps 7676170:1->2, 7676170:2->3, 7676170:3->4, 7676170:4->5): Sweep max_features downward aggressively (halving or more) until LB score stops improving, then do a fine-grained search around the best value. Expect the optimum to be very small (tens of features) for small datasets with linear models. Reverse immediately when score drops and bracket the optimum from both sides.

## 52. explicit_interactions_redundant_for_gbdt_with_rich_features  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When using a GBDT model on a tabular dataset with many available features, and considering adding explicit pairwise interaction features (e.g., differences, ratios) or handcrafted domain features on top of an already rich feature representation.
- **Action:** Treat explicit interaction/handcrafted features as low-priority since GBDTs and transformer embeddings already capture such interactions internally. If you try them, add as a single probe submission and compare CV/LB. Expect diminishing or negative returns. Be prepared to revert quickly rather than investing many iterations in narrowing subsets.
- **Exceptions:** When the model uses a very small feature subset or lacks the capacity to learn the interaction, explicit features may still help (see 28093671:e8#1 where expanding features helped).
- **Support:** kernels 27836972, 58130512; comps amex-default-prediction, learning-agency-lab-automate; tiers {'Expert': 1, 'Master': 1}; episode reached new best: {'no': 2}
- **Cells:** L2/feature_engineering
- **Examples:**
  - `27836972:e9#1` (amex-default-predict, Expert; steps 27836972:44->45, 27836972:46->47, 27836972:48->49, 27836972:49->50): Start with a broad set of interaction pairs, submit or validate, then systematically narrow: remove columns that hurt CV one at a time, try both raw-level and aggregated-level (last, mean) variants separately, and compare CV. If the broad set doesn't beat baseline, try subsets before abandoning. Keep only the minimal set that improves CV.
  - `58130512:e34#2` (learning-agency-lab-, Master; steps 58130512:105->106): When a tree model already consumes transformer embeddings, treat handcrafted linguistic features as low-priority. If you try them, add them as a single probe submission. Expect diminishing or negative returns because transformers already encode most of the same signal. Be prepared to revert quickly.

## 53. drop_high_na_or_redundant_columns_before_engineering  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When a block of raw features is either predominantly missing or represents the same underlying concept at multiple granularities (e.g., matching scores at different resolutions), and downstream aggregations or models inherit this redundancy/noise.
- **Action:** Remove the entire block of high-NA or redundant-resolution raw columns before computing derived features (aggregations, encodings). This eliminates multiple noisy derived features at once, reducing memory and noise. Verify via validation before submitting. This is complementary to post-hoc importance-based pruning.
- **Exceptions:** If the redundant columns are only used in a subset of model components (e.g., removed from one sub-model but kept in another), the benefit may be partial.
- **Support:** kernels 27799930, 77347591; comps amex-default-prediction, equity-post-hct-survival-pre; tiers {'Contributor': 1, 'Expert': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L2/feature_selection
- **Examples:**
  - `27799930:e11#2` (amex-default-predict, Contributor; steps 27799930:71->72): Identify raw columns with very high missing rates and drop them before computing aggregations (last, mean, std, diff, etc.). This eliminates multiple derived features at once, reducing noise and memory. Verify improvement via validation before submitting. This is complementary to post-hoc feature importance pruning.
  - `77347591:e3#2` (equity-post-hct-surv, Expert; steps 77347591:4->5): Remove the entire block of redundant resolution-variant features from the numeric feature set rather than selecting individual columns. Submit to verify the effect. If positive, keep the removal and move on to other levers.

## 54. stop_gbdt_hyperparam_tuning_at_plateau  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** GBDT hyperparameter tuning has been attempted and scores have plateaued (no improvement after one or two adjustment rounds), whether after extensive feature engineering or after a hyperparameter sweep.
- **Action:** Make at most one final micro-adjustment to confirm the plateau. If no improvement, stop tuning hyperparameters and switch to a different lever (e.g., new features, model architecture, or ensembling). Continuing to search the same hyperparameter space yields diminishing or negative returns.
- **Exceptions:** When feature engineering has plateaued but hyperparameters have never been tuned (as in 27836972), an initial substantial change (e.g., increasing tree depth, lowering learning rate, adding regularization) can still yield a meaningful gain before the hyperparameter plateau sets in.
- **Support:** kernels 27836972, 60759531; comps amex-default-prediction, learning-agency-lab-automate; tiers {'Expert': 2}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L2/gbdt_hyperparameter_tuning
- **Examples:**
  - `27836972:e13#1` (amex-default-predict, Expert; steps 27836972:70->71): Increase tree depth substantially (e.g., 4→7), lower learning rate (0.05→0.03), add strong regularization (high lambda, gamma, min_child_weight), and reduce column sampling to compensate for depth increase. Submit once and evaluate before further tuning.
  - `60759531:e3#2` (learning-agency-lab-, Expert; steps 60759531:13->14): Make one final micro-adjustment (±1 on integer params, ±0.1 on float params) to confirm the plateau. If the score does not improve, stop the sweep on this lever and consider a different lever (e.g., features, model architecture, or ensembling strategy) rather than continuing to search the same space.

## 55. keep_inference_behavior_consistent_with_training  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** During inference, adaptive or dynamic settings (e.g., dropout rate, dynamic input shapes) differ from what was used at training time, and score improvements are absent or inconsistent.
- **Action:** Revert inference-time settings to match training-time configuration. Disable dynamic/adaptive features (dropout, dynamic shapes, adaptive batching) during inference. If deterministic inference (e.g., dropout=0) doesn't help, stop searching other inference-time variations of that setting — the lever is unproductive.
- **Exceptions:** none
- **Support:** kernels 18350823, 50376011; comps commonlitreadabilityprize, hms-harmful-brain-activity-c; tiers {'Expert': 1, 'Grandmaster': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L2/inference_dropout_settings
- **Examples:**
  - `18350823:e4#3` (commonlitreadability, Expert; steps 18350823:8->9, 18350823:10->11): Keep inference-time dropout consistent with training-time settings. If you must experiment, test dropout=0 first (deterministic inference), and if it doesn't help, do not continue searching other dropout values at inference time — the lever is not productive.
  - `50376011:e31#2` (hms-harmful-brain-ac, Grandmaster; steps 50376011:180->181): Explicitly disable dynamic configuration flags (e.g., dynamic input shapes, adaptive batch sizing) when running in non-standard inference modes. These features are designed for training flexibility but can introduce non-determinism or errors during constrained inference.

## 56. lb_probing_when_cv_unreliable_for_selection  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** You have a small number of model variants or checkpoints to choose from, and local CV scores are either unavailable or do not reliably predict leaderboard performance (e.g., CV-LB rank discordance observed, or no local metric available).
- **Action:** Submit each variant individually to the leaderboard and record scores. Select the best performer based on LB rather than CV alone. After identifying the best single variant, consider ensembling the top LB performers. Expect small but meaningful score differences between variants.
- **Exceptions:** When the number of variants is large, exhaustive LB probing may waste submissions. Also, if other pipeline variables are not controlled between submissions, single-checkpoint LB comparisons can be unreliable (as seen in 7606235 where the same fold yielded different scores across versions).
- **Support:** kernels 52200959, 7606235; comps google-quest-challenge, hms-harmful-brain-activity-c; tiers {'Master': 2}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L2/leaderboard_probing_validation
- **Examples:**
  - `52200959:e4#2` (hms-harmful-brain-ac, Master; steps 52200959:20->21, 52200959:21->22, 52200959:22->23): Do not trust CV rankings alone for multi-input model variants — the generalization gap can vary across input types. Evaluate each variant on LB before deciding ensemble composition or weights. Expect that the variant with best CV may not win on LB.
  - `7606235:e2#1` (google-quest-challen, Master; steps 7606235:9->10, 7606235:10->11, 7606235:11->12, 7606235:12->13): Exhaustively submit each checkpoint individually to the leaderboard. Record scores for all, then select the best. Expect small score differences between folds. After identifying the best single checkpoint, consider ensembling the top performers.

## 57. scale_iterations_inversely_with_learning_rate  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When reducing the learning rate of a gradient boosting model that uses early stopping, and the maximum number of boosting rounds (n_estimators) or early_stopping_rounds have not been proportionally adjusted.
- **Action:** Increase n_estimators by at least the inverse ratio of the learning rate reduction (e.g., halving LR → at least double n_estimators). Also increase early_stopping_rounds to allow enough rounds for convergence at the lower LR. When increasing LR substantially, consider increasing max_depth by 1 to give more capacity per round; when decreasing LR, reduce depth back. Verify via validation curves that the model has converged before submitting.
- **Exceptions:** 60759531:e2#2 shows that even with increased n_estimators, simultaneous changes to other settings (e.g., random_state, regularization) can confound the signal, so avoid changing learning rate and regularization simultaneously.
- **Support:** kernels 27825577, 60759531; comps amex-default-prediction, learning-agency-lab-automate; tiers {'Expert': 2}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L2/learning_rate_and_optimizer
- **Examples:**
  - `27825577:e3#1` (amex-default-predict, Expert; steps 27825577:5->6, 27825577:6->7, 27825577:7->8, 27825577:8->9): Start from a moderate learning rate (e.g., 0.05). First probe lower values (halving: 0.025, 0.01). If validation degrades, probe higher values (0.1, 0.2). Use validation scores to bracket the optimum, then refine within the best bracket. When increasing learning rate substantially, also increase max_depth by 1 to give the model more capacity per round; when decreasing, reduce depth back. Increase early_stopping_rounds when using lower learning rates to allow enough rounds.
  - `60759531:e2#2` (learning-agency-lab-, Expert; steps 60759531:2->3, 60759531:5->6): When reducing learning rate, increase n_estimators by at least the inverse ratio (e.g., halving LR should at least double n_estimators) to allow early stopping to find the right iteration. Verify via validation curves that the model has converged before submitting. Do not change learning rate and regularization simultaneously.

## 58. revert_quickly_if_optimizer_or_head_change_regresses  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When switching to a new optimizer or re-tuning head hyperparameters (dropout, LR) after a significant architectural or loss-function change in a neural network, and the first probe submission shows regression.
- **Action:** Probe the change in a single submission. If it regresses, revert immediately and instead re-tune the original optimizer's or head's hyperparameters (learning rate, epochs, dropout) rather than spending time tuning the new configuration. Isolate each variable by reverting one at a time to determine which change actually helped.
- **Exceptions:** Attribution can be confounded when multiple changes are bundled (e.g., bug fixes, scheduler changes alongside optimizer swap), so ensure only one variable changes per probe.
- **Support:** kernels 7253130, 77129691; comps equity-post-hct-survival-pre, google-quest-challenge; tiers {'Contributor': 1, 'Master': 1}; episode reached new best: {'yes': 2}
- **Cells:** L2/learning_rate_and_optimizer
- **Examples:**
  - `7253130:e2#1` (google-quest-challen, Contributor; steps 7253130:3->4, 7253130:4->5): First move both dropout and learning rate together in the conservative direction (lower dropout, lower lr) to establish a working baseline. Then isolate each variable by reverting one at a time and submitting, to determine which change actually helped. Keep the configuration that scores best.
  - `77129691:e11#2` (equity-post-hct-surv, Master; steps 77129691:20->21, 77129691:21->22): Probe the alternative optimizer in a single submission. If it regresses, revert immediately and re-tune the original optimizer's hyperparameters (learning rate, epochs, batch size) rather than spending time tuning the new optimizer. Tabular models are often less sensitive to optimizer novelty than to hyperparameter tuning of a known optimizer.

## 59. pivot_architecture_when_incremental_tuning_plateaus  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** You have been iterating on a single model architecture (swapping checkpoints, tuning preprocessing, or hyperparameters) and scores have plateaued or local CV improvements no longer translate to leaderboard gains.
- **Action:** Stop incremental tuning of the current architecture. Instead, make a structural change: either port successful preprocessing/augmentation improvements to a different architecture variant, or redesign the model head (e.g., add attention mechanisms, multi-head outputs). Evaluate each architecture variant with the best-known preprocessing and select based on leaderboard feedback rather than local CV alone.
- **Exceptions:** Both items have limited causal evidence—one infers the benefit from a single checkpoint comparison, the other from a post-episode pivot. The rule is strongest when multiple architecture options are readily available.
- **Support:** kernels 15082684, 7018718; comps google-quest-challenge, ranzcr-clip-catheter-line-cl; tiers {'Master': 1, 'Expert': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L2/model_architecture_design
- **Examples:**
  - `15082684:e2#2` (ranzcr-clip-catheter, Master; steps 15082684:11->12, 15082684:12->13): If a checkpoint sweep across multiple training runs shows that higher local CV does not translate to higher LB scores, stop swapping checkpoints of the same architecture. Instead, change the model head design or add structural improvements (e.g., attention mechanisms, multi-head outputs) that may improve generalization in ways that single-fold CV cannot capture.
  - `7018718:e8#2` (google-quest-challen, Expert; steps 7018718:25->26, 7018718:26->27): When you develop a preprocessing improvement on one model architecture, port it to other architectures you have available. Combine the best preprocessing with each architecture variant and search over checkpoints for each combination.

## 60. revert_capacity_increase_on_regression  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When tuning model capacity parameters (tree depth/leaves, backbone size, channel width) by small increments and the first increase over a moderate baseline causes a score regression.
- **Action:** Revert to the original capacity setting rather than trying further increases. Try 2-3 configurations at most; if none improves over baseline, the capacity direction is wrong. For GBDT with ordinal objectives, prefer conservative tree capacity. For CNN attention blocks, a gap >0.5% AUC after 3 configs suggests the architecture variant itself is inferior.
- **Exceptions:** Only increasing capacity was tested in the GBDT case; decreasing below baseline was never tried. In the CNN case, backbone changes confounded the comparison.
- **Support:** kernels 13848868, 58527792; comps learning-agency-lab-automate, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 1, 'Contributor': 1}; episode reached new best: {'no': 2}
- **Cells:** L2/model_capacity_tuning
- **Examples:**
  - `13848868:e6#2` (ranzcr-clip-catheter, Grandmaster; steps 13848868:22->23, 13848868:24->25, 13848868:26->27): Try 2-3 channel width configurations (e.g., narrow → wider → revert). If the best variant still underperforms the original block type by a meaningful margin after the sweep, revert to the original block rather than continuing to tune. A gap of >0.5% AUC after 3 configurations suggests the block type itself is inferior for this task.
  - `58527792:e2#2` (learning-agency-lab-, Contributor; steps 58527792:2->3, 58527792:3->4): For GBDT models with custom ordinal objectives, prefer conservative tree capacity (fewer leaves relative to depth). If increasing max_depth and num_leaves by 1 worsens the score, revert immediately rather than trying larger increases—overfitting on the ordinal boundaries is likely the cause.

## 61. estimate_blend_impact_before_tuning  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When tuning hyperparameters of a model that contributes a small fraction (<5%) of an ensemble blend weight, and the ensemble is dominated by strong external or other submissions.
- **Action:** Before tuning, estimate the maximum possible score improvement given the blend weight. If the model's weight is too low for improvements to be visible on the leaderboard, either increase the model's blend weight first or redirect effort to the dominant ensemble components.
- **Exceptions:** In the EEG/spectrogram case the secondary branch was not blended by weight but architecturally integrated, so the principle applies loosely—the spectrogram preprocessing mattered more than EEG branch sizing.
- **Support:** kernels 29588171, 49576186; comps amex-default-prediction, hms-harmful-brain-activity-c; tiers {'Master': 1, 'Expert': 1}; episode reached new best: {'no': 2}
- **Cells:** L2/model_capacity_tuning
- **Examples:**
  - `29588171:e5#2` (amex-default-predict, Master; steps 29588171:35->36, 29588171:38->39): Before tuning hyperparameters of a low-weight ensemble member, estimate the maximum possible score improvement given the blend weight. If the model contributes <5% of the blend, even large model improvements will be invisible on the leaderboard. Either increase the model's blend weight first or focus effort on the dominant ensemble components.
  - `49576186:e6#2` (hms-harmful-brain-ac, Expert; steps 49576186:37->38, 49576186:38->39, 49576186:40->41): Keep the EEG branch backbone small (B0) and match the channel count exactly to the number of actual signal channels (here 4 bipolar pairs per region). Padding with zeros to 6 or 8 channels wastes capacity and can hurt. Verify input shape matches the data before scaling up the backbone.

## 62. explicit_deterministic_checkpoint_loading  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When loading model checkpoints for inference or ensembling, and the loading mechanism involves implicit discovery (e.g., glob) or silent fallback (e.g., pretrained=True with strict=False), producing unpredictable or mixed weight states.
- **Action:** Make checkpoint loading explicit and deterministic: use hard-coded file paths (annotated with fold/score metadata) instead of glob discovery, set pretrained=False when loading fine-tuned checkpoints, and use strict=True in load_state_dict. Fix model definition mismatches rather than silently skipping keys.
- **Exceptions:** none
- **Support:** kernels 15173072, 18426209; comps commonlitreadabilityprize, ranzcr-clip-catheter-line-cl; tiers {'Contributor': 1, 'Expert': 1}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L2/model_loading_infrastructure
- **Examples:**
  - `15173072:e2#2` (ranzcr-clip-catheter, Contributor; steps 15173072:10->11): When loading a fine-tuned checkpoint, set pretrained=False in the model constructor and use strict=True in load_state_dict (or at minimum inspect warnings from strict=False). If keys don't match, fix the model definition rather than silently skipping mismatched weights.
  - `18426209:e6#2` (commonlitreadability, Expert; steps 18426209:8->9): Replace glob-based checkpoint discovery with a hard-coded list of file paths. Annotate each path with its fold index and validation score so that future edits can reason about which to keep or drop.

## 63. linear_meta_learner_for_stacking  [L2]  —  2 kernels, 2 comps, 2 items

- **Context:** When stacking multiple base model predictions (OOF) as meta-features and the meta-feature space is low-dimensional (handful to ~20 base model predictions), especially with limited training data.
- **Action:** Start with a simple linear meta-learner (Ridge regression or LinearRegression) rather than nonlinear alternatives. Ridge is preferred over Lasso when you already perform explicit feature elimination. If a nonlinear meta-learner (e.g., RBF SVR) does not improve OOF score, revert to the linear model rather than tuning kernel hyperparameters.
- **Exceptions:** Ridge stacking alone may not beat well-tuned weighted averaging until combined with iterative feature elimination (73937748:e11#1). On very small datasets, even linear models may need regularization tuning.
- **Support:** kernels 18851026, 73937748; comps commonlitreadabilityprize, equity-post-hct-survival-pre; tiers {'Master': 2}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L2/stacking_meta_learner
- **Examples:**
  - `18851026:e1#1` (commonlitreadability, Master; steps 18851026:2->3, 18851026:3->4): Start with a simple linear model (LinearRegression or Ridge) as the stacking meta-learner before trying nonlinear alternatives like RBF SVR. With very few meta-features and small data, linear blending often outperforms nonlinear methods that can overfit. If a nonlinear kernel regresses, revert to the linear model rather than tuning kernel hyperparameters.
  - `73937748:e11#1` (equity-post-hct-surv, Master; steps 73937748:29->30, 73937748:30->31, 73937748:31->32, 73937748:32->33): Start with Ridge regression as the stacking meta-learner on rank-transformed OOF predictions. Add iterative feature elimination (drop each base model, keep removal if OOF score improves). Then tune Ridge hyperparameters (alpha, fit_intercept, positive constraint) with Optuna. Prefer Ridge over Lasso: L1 sparsity is less useful when you already do explicit feature elimination, and Lasso tends to underperform on small meta-feature sets.

## 64. isolate_regression_by_ablation  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** Combining components (models in ensemble, or multiple simultaneous changes) causes a significant score regression compared to individual components or the prior baseline.
- **Action:** Immediately isolate by running each component alone to confirm individual quality. Check merging/integration code for bugs (e.g., incorrect concatenation, misaligned predictions). Only after confirming components work individually and integration logic is correct, re-test the combination. For multi-component changes, remove the most aggressive/novel component first, test, then continue removing until regression source is identified.
- **Exceptions:** none
- **Support:** kernels 15372370, 52860091; comps hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Expert': 1, 'Grandmaster': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/explore/new_idea
- **Examples:**
  - `15372370:e5#1` (ranzcr-clip-catheter, Expert; steps 15372370:9->10, 15372370:10->11): Revert the changes incrementally rather than all at once: remove the most aggressive/novel component first, test, then remove remaining novel components. This isolates which change caused the regression. If the score still hasn't recovered after partial revert, continue removing until you return to baseline behavior.
  - `52860091:e5#2` (hms-harmful-brain-ac, Grandmaster; steps 52860091:16->17, 52860091:17->18, 52860091:18->19, 52860091:19->20): Immediately isolate by running each component alone to confirm individual quality. Check the merging code for bugs (e.g., predictions not being appended correctly). Only after confirming both components work individually and the merge logic is correct, re-test the combination. A regression from combining two working models usually indicates a code bug rather than model incompatibility.

## 65. batch_infrastructure_changes_before_submitting  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** A new approach requires coordinated changes across multiple pipeline components, and intermediate states are broken or not meaningful to evaluate.
- **Action:** Batch all prerequisite infrastructure changes without submitting. Use intermediate versions to inspect outputs (e.g., display dataframe heads, list directories, check shapes) to confirm correctness locally. Only submit once the complete pipeline is assembled and verified end-to-end. This avoids wasting submission quota on uninformative scores.
- **Exceptions:** none
- **Support:** kernels 27825577, 53747598; comps amex-default-prediction, hms-harmful-brain-activity-c; tiers {'Expert': 1, 'Master': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L3/explore/new_idea
- **Examples:**
  - `27825577:e5#2` (amex-default-predict, Expert; steps 27825577:14->15, 27825577:17->18, 27825577:19->20): After two submitted regressions from the same lever, limit further exploration to at most two more unsubmitted CV checks. If no CV improvement is found, abandon the lever and switch to a diagnostic or entirely different approach rather than continuing to permute the same options.
  - `53747598:e4#2` (hms-harmful-brain-ac, Master; steps 53747598:15->16, 53747598:16->17, 53747598:17->18, 53747598:18->19): Batch all prerequisite infrastructure changes without submitting. Only submit once the complete pipeline is assembled and locally verified. Use intermediate versions to inspect outputs (e.g., display dataframe heads, list directories) to confirm correctness without consuming leaderboard submissions.

## 66. test_candidate_model_solo_then_in_blend  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** You have a new candidate model and an existing ensemble of proven models, and want to evaluate whether the candidate adds value.
- **Action:** First test the candidate model solo (or with minimal blending) to gauge standalone quality. Then add it to the existing blend and compare. A weak solo model may still contribute diversity, so do not discard based on solo score alone—judge by the final blend score. If adding it worsens the blend despite decent solo quality, try weighted blending before discarding.
- **Exceptions:** 52860091: v0+v2 was worse than v2 alone despite v0 being decent solo, showing that diversity contribution is not guaranteed.
- **Support:** kernels 18423958, 52860091; comps commonlitreadabilityprize, hms-harmful-brain-activity-c; tiers {'Master': 1, 'Grandmaster': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/explore/new_idea
- **Examples:**
  - `18423958:e5#1` (commonlitreadability, Master; steps 18423958:10->11, 18423958:11->12, 18423958:12->13): First test the candidate model solo (or with minimal blending) to gauge its standalone quality. If it is weak alone, do not discard it—instead add back proven strong members one at a time and re-tune weights. A weak solo model may still contribute diversity to the final blend. Only judge the candidate's value by the final multi-model blend score, not its solo score.
  - `52860091:e5#1` (hms-harmful-brain-ac, Grandmaster; steps 52860091:17->18, 52860091:19->20, 52860091:20->21, 52860091:21->22): First evaluate each candidate model variant in isolation to establish its standalone quality. Then test pairwise and higher-order combinations. If adding a variant worsens the ensemble despite being decent alone, try weighted blending before discarding it. If a variant is much stronger solo than others, test it alone before averaging — uniform averaging can dilute a strong model. Stop uniform-weight search when adding members hurts, and switch to weighted blending.

## 67. stop_after_two_consecutive_null_or_regressing_probes  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** Two successive probes of the same lever (e.g., escalating a hyperparameter, ablating components, or tuning a preprocessing toggle) both show no improvement or increasing regression.
- **Action:** Revert to the best-known configuration and abandon that lever. Move on to an orthogonal lever rather than continuing to probe in the same direction. Do not spend more than two submissions confirming what two data points already show.
- **Exceptions:** none
- **Support:** kernels 18350823, 75145694; comps commonlitreadabilityprize, equity-post-hct-survival-pre; tiers {'Expert': 2}; episode reached new best: {'no': 2}
- **Cells:** L3/probe/new_idea/part1
- **Examples:**
  - `18350823:e9#2` (commonlitreadability, Expert; steps 18350823:20->21, 18350823:21->22): After two null results from increasing a parameter in the same direction, revert to the original value and move on to a different lever. Do not continue escalating; the signal indicates the lever has no effect or the effect is below measurement noise.
  - `75145694:e5#2` (equity-post-hct-surv, Expert; steps 75145694:14->15, 75145694:15->16): Stop ablating after at most two consecutive regressions. Revert to the best-known configuration and pivot to the opposite direction (adding components or complexity). Do not spend more submissions confirming what two data points already show.

## 68. bundle_high_confidence_fixes_to_save_submissions  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** Multiple fixes are identified where each has high confidence of being correct (e.g., matching known training settings like resolution and normalization), and submission budget is limited.
- **Action:** Bundle all high-confidence fixes into a single submission rather than testing each independently. Only isolate changes when the direction of effect is uncertain or when you need to attribute improvement to a specific change.
- **Exceptions:** Bundling makes attribution impossible; if one change could plausibly be harmful, test separately (15082684:e4#2 counter_evidence).
- **Support:** kernels 15082684, 55591012; comps learning-agency-lab-automate, ranzcr-clip-catheter-line-cl; tiers {'Master': 1, 'Grandmaster': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/probe/new_idea/part1
- **Examples:**
  - `15082684:e4#2` (ranzcr-clip-catheter, Master; steps 15082684:16->17, 15082684:17->18): Bundle multiple high-confidence fixes into a single submission rather than testing each independently. This conserves submission budget. Only isolate changes when the direction of effect is uncertain or when you need to attribute improvement to a specific change.
  - `55591012:e7#1` (learning-agency-lab-, Grandmaster; steps 55591012:23->24): After any change to ensemble composition (adding/removing models, retraining components), re-probe the blend weight by shifting it moderately from the previous best (e.g., ±0.10). If the first probe improves, accept it; if not, try the opposite direction. One or two probes usually suffice since the optimum rarely shifts dramatically.

## 69. checkpoint_and_move_on_after_clear_improvement  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** A single experiment yields a clear new best score, and there are other orthogonal levers (new features, new models) to explore.
- **Action:** Record the result with version logs documenting the baseline score, checkpoint the code, and move on to the next orthogonal lever rather than immediately grid-searching around the successful hyperparameters. Return to fine-tuning later if needed.
- **Exceptions:** none
- **Support:** kernels 15203842, 27836972; comps amex-default-prediction, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 1, 'Expert': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/probe/new_idea/part1
- **Examples:**
  - `15203842:e3#2` (ranzcr-clip-catheter, Grandmaster; steps 15203842:10->11, 15203842:11->12, 15203842:12->13, 15203842:13->14): Before changing code, checkpoint the current state with version logs documenting baseline scores. Then apply the suggested change as a single isolated edit and submit. If it improves, checkpoint again. This isolates the effect of the community suggestion from any other changes.
  - `27836972:e13#3` (amex-default-predict, Expert; steps 27836972:71->72, 27836972:72->73): After achieving a new best from a hyperparameter probe, record the result, checkpoint the code, and move on to the next orthogonal lever (e.g., new features) rather than immediately grid-searching around the new hyperparameters. Return to fine-tuning later if needed.

## 70. ablate_ensemble_member_before_tuning  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** An ensemble has multiple members and you suspect one is weaker or its contribution is uncertain.
- **Action:** Disable the suspected weaker member and submit the remaining prediction to measure marginal contribution. If the single/reduced model matches or beats the ensemble, drop the weaker member permanently. If it regresses, restore the ensemble and tune the weaker member or seek better diversity sources instead.
- **Exceptions:** 27502740:e4#2 notes that if blending same-framework models hurts, seek diversity from a genuinely different source rather than abandoning blending entirely.
- **Support:** kernels 27502740, 60197293; comps amex-default-prediction, learning-agency-lab-automate; tiers {'Grandmaster': 1, 'Expert': 1}; episode reached new best: {'no': 2}
- **Cells:** L3/probe/new_idea/part1
- **Examples:**
  - `27502740:e4#2` (amex-default-predict, Grandmaster; steps 27502740:7->8): If splitting an internal algorithm into a separate model and blending hurts the score, revert the split and instead seek diversity from a genuinely different source (different framework, different feature set, or external predictions). Keep the blending infrastructure but change what you blend.
  - `60197293:e5#1` (learning-agency-lab-, Expert; steps 60197293:28->29, 60197293:34->35): Disable the suspected weaker member, submit the single-model prediction, and compare to the ensemble score. If the single model matches or beats the ensemble, drop the weaker member permanently and invest effort elsewhere. If it regresses, restore the ensemble and tune the weaker member instead.

## 71. retune_blend_weights_after_ensemble_composition_change  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** The composition of an ensemble has changed (models added, removed, or retrained) and blend weights were tuned for the old composition.
- **Action:** Re-probe the blend weight by shifting it moderately from the previous best (e.g., ±0.10). If the first probe improves, accept it; if not, try the opposite direction. One or two probes usually suffice. Do not over-tune on a small public leaderboard—if redistribution causes regression, revert to previous weights and invest in improving base models instead.
- **Exceptions:** 18851026:e4#2 warns against over-tuning when the public test set is very small.
- **Support:** kernels 18851026, 55591012; comps commonlitreadabilityprize, learning-agency-lab-automate; tiers {'Master': 1, 'Grandmaster': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/probe/new_idea/part1
- **Examples:**
  - `18851026:e4#2` (commonlitreadability, Master; steps 18851026:10->11): After confirming a new component improves the score, resist over-tuning blend weights on a tiny public leaderboard. If redistributing weight away from the best-performing component causes regression, revert to the previous weights and instead invest effort in improving or adding base models. One round of weight adjustment is sufficient when the public test set is very small.
  - `55591012:e7#1` (learning-agency-lab-, Grandmaster; steps 55591012:23->24): After any change to ensemble composition (adding/removing models, retraining components), re-probe the blend weight by shifting it moderately from the previous best (e.g., ±0.10). If the first probe improves, accept it; if not, try the opposite direction. One or two probes usually suffice since the optimum rarely shifts dramatically.

## 72. verify_inference_changes_before_submitting  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** A change affects all predictions at inference time (e.g., TTA, dropout, scaling) and submission budget is limited.
- **Action:** Add per-sample debug prints or logging for the new inference path, run without submitting to inspect outputs for sanity (reasonable ranges, no degenerate values). Only submit after confirming outputs look reasonable. This avoids wasting submissions on broken inference.
- **Exceptions:** none
- **Support:** kernels 53424936, 75584724; comps equity-post-hct-survival-pre, hms-harmful-brain-activity-c; tiers {'Master': 2}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L3/probe/new_idea/part1
- **Examples:**
  - `53424936:e3#2` (hms-harmful-brain-ac, Master; steps 53424936:8->9, 53424936:9->10): Add per-sample debug prints for the new inference path, run without submitting to inspect outputs, then re-run (possibly unchanged) to submit only after confirming outputs look reasonable. This avoids wasting submissions on broken inference.
  - `75584724:e5#1` (equity-post-hct-surv, Master; steps 75584724:8->9, 75584724:9->10, 75584724:10->11): For a binary preprocessing toggle, first evaluate locally (OOF) without submitting. If local results are ambiguous, submit both variants to the leaderboard. If neither variant beats the prior best, abandon the idea and move on rather than iterating further on the same lever.

## 73. gate_risky_changes_on_local_cv  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When probing a fundamentally different model, architecture, or speculative preprocessing change whose impact is uncertain and leaderboard submissions are limited.
- **Action:** Do not submit until local CV confirms the change is at least competitive with the current best. Fix runtime issues first, then evaluate on validation. Only submit after CV scores match or exceed the current LB baseline. If CV is disappointing, abandon the probe without burning a submission.
- **Exceptions:** When local CV is unreliable (very small dataset, high CV-LB divergence), a direct LB probe may be necessary.
- **Support:** kernels 27502740, 55431616; comps amex-default-prediction, learning-agency-lab-automate; tiers {'Grandmaster': 2}; episode reached new best: {'no': 2}
- **Cells:** L3/probe/new_idea/part2
- **Examples:**
  - `27502740:e2#2` (amex-default-predict, Grandmaster; steps 27502740:2->3, 27502740:3->4, 27502740:4->5): After adding a speculative feature, run locally first without submitting. Fix any runtime errors (shape mismatches, type errors) in a separate micro-commit. Only submit once the pipeline runs cleanly. If the result is neutral or negative, revert the speculative part and submit the minimal surviving change to confirm the baseline is intact.
  - `55431616:e6#2` (learning-agency-lab-, Grandmaster; steps 55431616:20->21, 55431616:21->22, 55431616:22->23, 55431616:23->24): When probing a fundamentally different model, do not submit until local CV confirms the change is at least competitive with the current best. Reduce fold count to iterate faster, fix runtime issues first, then evaluate. Only submit after CV scores match or exceed the current LB baseline. If CV is disappointing, abandon the probe without burning a submission.

## 74. retest_cheap_toggles_after_model_change  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When you have a cheap binary post-processing toggle (e.g., rank conversion, normalization flag) or a blending weight whose optimal value was previously established, but you have since changed the underlying model or ensemble composition.
- **Action:** Re-test both states of the toggle (or previously discarded parameter values) after every model/ensemble change, as the optimal setting can shift. Submit both and keep whichever scores higher. Do not assume the previous winner carries over.
- **Exceptions:** none
- **Support:** kernels 13848868, 77347591; comps equity-post-hct-survival-pre, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 1, 'Expert': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/probe/new_idea/part2
- **Examples:**
  - `13848868:e5#3` (ranzcr-clip-catheter, Grandmaster; steps 13848868:17->18, 13848868:19->20): For any cheap binary post-processing toggle whose effect is model-dependent, always test both states after every model change. Submit both and keep whichever scores higher. Do not assume the previous winner carries over. Budget two submissions per model change for this.
  - `77347591:e3#1` (equity-post-hct-surv, Expert; steps 77347591:3->4): Re-test previously discarded blending weight values after changing other model hyperparameters, because the optimal blend point can shift. Submit each weight change in isolation to confirm its effect before moving on.

## 75. abandon_speculative_probe_on_first_regression  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When a speculative preprocessing or data augmentation change (e.g., text cleaning on pretrained encoders, SMOTE oversampling) is tested as a single probe and the leaderboard score regresses.
- **Action:** Revert immediately rather than tuning the parameters of the failed approach. If the direction is wrong on the first try, parameter tuning is unlikely to save it. Do not invest multiple iterations refining an approach that hurt initially.
- **Exceptions:** If the regression is very small and confounded by other simultaneous changes, a second isolated test may be warranted.
- **Support:** kernels 59253662, 7670859; comps google-quest-challenge, learning-agency-lab-automate; tiers {'Contributor': 2}; episode reached new best: {'no': 2}
- **Cells:** L3/probe/new_idea/part2
- **Examples:**
  - `59253662:e7#1` (learning-agency-lab-, Contributor; steps 59253662:29->30, 59253662:30->31): Treat it as a single probe: apply the change, submit once, and if the leaderboard score regresses, abandon the idea immediately and revert. Do not tune the resampling parameters—if the direction is wrong, parameter tuning won't save it. Bundle the change with minimal other modifications so the signal is attributable.
  - `7670859:e6#1` (google-quest-challen, Contributor; steps 7670859:31->32): Treat heavy text cleaning as a single probe experiment. If the leaderboard score regresses, revert immediately rather than tuning the cleaning further—pretrained encoders already handle noise, and aggressive normalization can destroy useful signal (casing, punctuation, numbers). Do not invest multiple iterations refining cleaning that hurt on the first try.

## 76. swap_backbone_diversity_over_weight_tuning  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When fine-tuning ensemble blend weights yields diminishing returns (negligible or negative improvement) and the ensemble contains multiple models from the same architecture family.
- **Action:** Stop tuning blend weights and instead swap the weakest-contributing member for a backbone from a different model family (e.g., replace a RoBERTa variant with DeBERTa). Architectural diversity typically yields larger gains than optimizing blend coefficients among similar models.
- **Exceptions:** If a non-linear blending formula (e.g., power-mean) hasn't been tried yet, it may yield a quick marginal gain before switching to backbone diversity.
- **Support:** kernels 15203842, 18523075; comps commonlitreadabilityprize, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 1, 'Expert': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/probe/new_idea/part2
- **Examples:**
  - `15203842:e3#1` (ranzcr-clip-catheter, Grandmaster; steps 15203842:12->13): Try replacing a simple linear average with a power-mean or RMS-style blend (e.g., averaging square roots of predictions). Make a single targeted change, submit, and keep it if it improves. Do not sweep exponents unless the first attempt fails—marginal gains here are small and the search space is narrow.
  - `18523075:e1#2` (commonlitreadability, Expert; steps 18523075:2->3): Stop tuning weights and instead swap the weakest-contributing member for a backbone from a different model family (e.g., replace a RoBERTa variant with DeBERTa or T5). Architectural diversity typically yields larger gains than optimizing blend coefficients among similar models.

## 77. ensemble_ablation_via_pruning  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When you have a complex ensemble with many weighted members and want to understand which components are actually contributing to performance.
- **Action:** Submit a drastically pruned version (1-2 members) to the leaderboard. If it regresses significantly, ensemble diversity is valuable—keep or expand members. If it matches or improves, many members are redundant and you should simplify. Limit to 1-2 ablation submissions.
- **Exceptions:** none
- **Support:** kernels 49524919, 75145694; comps equity-post-hct-survival-pre, hms-harmful-brain-activity-c; tiers {'Grandmaster': 1, 'Expert': 1}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L3/probe/new_idea/part2
- **Examples:**
  - `49524919:e34#1` (hms-harmful-brain-ac, Grandmaster; steps 49524919:158->159, 49524919:159->160, 49524919:160->161, 49524919:161->162): Submit each major model group in isolation (disabling all others) to measure its standalone score. If every component scores worse than the blend, the blend is validated. Then re-enable all components — the blend with any checkpoint updates discovered during probing often yields a further improvement. Limit probing to 2-4 submissions to conserve budget.
  - `75145694:e5#1` (equity-post-hct-surv, Expert; steps 75145694:14->15, 75145694:15->16): Submit a drastically pruned version (1-2 members) to the leaderboard. If it regresses significantly, the ensemble diversity is valuable and you should keep/expand members rather than simplify. If it matches or improves, many members are redundant. Limit to 1-2 ablation submissions before deciding direction.

## 78. stop_sweeping_after_structural_change_reprobe  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When you have already extensively swept a hyperparameter, then made a structural change to the pipeline, and a single re-probe near the old optimum confirms improvement.
- **Action:** Accept the re-probed value and move on to a different lever rather than re-sweeping the full range. Diminishing returns are likely since the prior sweep already mapped the landscape and the structural change is unlikely to have dramatically shifted the optimum.
- **Exceptions:** If the structural change fundamentally alters the prediction distribution (e.g., adding a new model family to the ensemble), a broader re-sweep may be warranted.
- **Support:** kernels 13848868, 55591012; comps learning-agency-lab-automate, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 2}; episode reached new best: {'yes': 2}
- **Cells:** L3/probe/new_idea/part2
- **Examples:**
  - `13848868:e5#3` (ranzcr-clip-catheter, Grandmaster; steps 13848868:17->18, 13848868:19->20): For any cheap binary post-processing toggle whose effect is model-dependent, always test both states after every model change. Submit both and keep whichever scores higher. Do not assume the previous winner carries over. Budget two submissions per model change for this.
  - `55591012:e7#2` (learning-agency-lab-, Grandmaster; steps 55591012:23->24, 55591012:24->25, 55591012:25->26): If you have already swept a parameter extensively in a prior episode and then make a structural change, a single re-probe near the old optimum is sufficient. If it improves, accept and move on to a different lever rather than re-sweeping the full range, since diminishing returns are likely.

## 79. revert_extreme_parameter_and_pivot  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When a parameter change is so extreme it causes runtime failure or nonsensical results (e.g., n_splits nearly equal to dataset size).
- **Action:** Do not try to fix incrementally. Reset the problematic parameter to a reasonable value and pivot to the next experiment. Bundle the fix with a new idea to save a version/submission.
- **Exceptions:** none
- **Support:** kernels 27502740, 7676170; comps amex-default-prediction, google-quest-challenge; tiers {'Grandmaster': 1, 'Contributor': 1}; episode reached new best: {'no': 2}
- **Cells:** L3/probe/new_idea/part2
- **Examples:**
  - `27502740:e2#2` (amex-default-predict, Grandmaster; steps 27502740:2->3, 27502740:3->4, 27502740:4->5): After adding a speculative feature, run locally first without submitting. Fix any runtime errors (shape mismatches, type errors) in a separate micro-commit. Only submit once the pipeline runs cleanly. If the result is neutral or negative, revert the speculative part and submit the minimal surviving change to confirm the baseline is intact.
  - `7676170:e4#2` (google-quest-challen, Contributor; steps 7676170:18->19, 7676170:19->20, 7676170:20->21): If a run fails or produces nonsensical output due to an extreme parameter, do not try to fix incrementally. Instead, reset the problematic parameter to a reasonable value and pivot to the next experiment you want to try. Bundling the fix with a new idea saves a version.

## 80. incremental_changes_avoid_consecutive_failures  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** Modifying an inference or training pipeline by adding multiple prediction calls, aggregation steps, or variable renames in a single edit.
- **Action:** Make changes incrementally: first add prediction calls and verify they run, then add aggregation, then wire to submission. Do a find-and-replace check on all variable references before submitting. This avoids consecutive failed runs that waste submission budget.
- **Exceptions:** none
- **Support:** kernels 17616127, 77450317; comps commonlitreadabilityprize, equity-post-hct-survival-pre; tiers {'Contributor': 1, 'Grandmaster': 1}; episode reached new best: {'no': 2}
- **Cells:** L3/probe/new_resource
- **Examples:**
  - `17616127:e12#2` (commonlitreadability, Contributor; steps 17616127:46->47, 17616127:47->48, 17616127:48->49): When adding multiple new model predictions and aggregation logic, make changes incrementally: first add the prediction calls and verify they run, then add the aggregation, then wire it to submission. Renaming variables across scattered cells is error-prone; do a find-and-replace check on all references before submitting. Two consecutive failed runs waste submission budget and time.
  - `77450317:e9#2` (equity-post-hct-surv, Grandmaster; steps 77450317:17->18, 77450317:18->19): Apply the change, run the notebook to get local CV metrics, and checkpoint the version without submitting. Only submit after confirming improvement locally or after combining the change with other pending improvements in a single submission.

## 81. pivot_lever_when_score_range_negligible  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When exhausting the natural variants of a lever (e.g., checkpoint subsets, small config changes) produces score differences smaller than leaderboard noise or the observed noise band from probe runs.
- **Action:** Stop iterating on the current lever. Pivot to a qualitatively different lever with higher potential variance in outcomes (e.g., different model family, different feature set, pipeline replacement). Reserve incremental tuning for when the baseline is already within a few points of the target.
- **Exceptions:** When the gap to competitive scores is small (<2–3 points), incremental tuning of the same lever may still be worthwhile (13577502:e1#2 implies this threshold).
- **Support:** kernels 13577502, 73671444; comps equity-post-hct-survival-pre, ranzcr-clip-catheter-line-cl; tiers {'Expert': 1, 'Grandmaster': 1}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L3/probe/none_visible
- **Examples:**
  - `13577502:e1#2` (ranzcr-clip-catheter, Expert; steps 13577502:3->4): After confirming a weak baseline with probe runs, skip incremental tuning and replace the core pipeline (model architecture, data loading, accelerator strategy) in one step. Reserve incremental tuning for when the baseline is already within a few points of the target.
  - `73671444:e1#2` (equity-post-hct-surv, Grandmaster; steps 73671444:2->3): Stop working the current lever after exhausting its natural variants if the score range is negligible. Pivot to a qualitatively different lever (different model family, different feature set) that has higher potential variance in outcomes.

## 82. stop_meta_learner_tuning_pivot_to_base_models  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When 2-3 iterations of meta-learner or stacking combiner hyperparameter tuning fail to exceed the best score achieved with default or simple settings.
- **Action:** Stop tuning the meta-learner and instead add new diverse base models to the ensemble. The marginal value of meta-learner hyperparameters is small compared to adding an uncorrelated base prediction.
- **Exceptions:** none
- **Support:** kernels 18851026, 73937748; comps commonlitreadabilityprize, equity-post-hct-survival-pre; tiers {'Master': 2}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L3/sweep/new_idea/part1
- **Examples:**
  - `18851026:e1#2` (commonlitreadability, Master; steps 18851026:2->3, 18851026:3->4): After testing a few discrete options on a secondary lever, if the best gain is small and a variant regresses substantially, stop the sweep and pivot to a higher-impact lever (e.g., richer features, additional base models, or a fundamentally different blending strategy) rather than continuing to tune the same lever.
  - `73937748:e11#3` (equity-post-hct-surv, Master; steps 73937748:34->35): Stop tuning the stacking meta-learner and instead add new diverse base models to the ensemble. The marginal value of meta-learner hyperparameters is small compared to adding an uncorrelated base prediction. Submit only after the new base models are integrated.

## 83. sweep_full_range_then_confirm_under_noise  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When leaderboard scores are noisy and you need to find the best value of a single scalar hyperparameter on a bounded interval.
- **Action:** Sweep the full plausible range at a fixed step size rather than greedily hill-climbing, because noisy feedback can mislead greedy search. After the sweep, return to the best-performing value and re-confirm it. Hold all other parameters fixed during the sweep to avoid confounding.
- **Exceptions:** 55987255 author confounded the signal by changing n_estimators simultaneously with blend weight.
- **Support:** kernels 55987255, 77129691; comps equity-post-hct-survival-pre, learning-agency-lab-automate; tiers {'Master': 2}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L3/sweep/new_idea/part1
- **Examples:**
  - `55987255:e29#2` (learning-agency-lab-, Master; steps 55987255:178->179, 55987255:182->183): Sweep the full plausible range at a fixed step size rather than greedily hill-climbing, because noisy feedback can mislead greedy search. After the sweep, return to the best-performing value and re-confirm it (possibly with a secondary change like more trees). If the confirmation score is close to the original best, accept it and move on to a different lever.
  - `77129691:e3#2` (equity-post-hct-surv, Master; steps 77129691:8->9): After bracketing an optimum on one hyperparameter, revert it to the best-known value and change only the second hyperparameter. Never change two hyperparameters simultaneously when the expected effect size is small, because a regression cannot be attributed. If you do change two and regress, revert both to the last-known-good state before continuing.

## 84. include_both_variants_when_swap_regresses  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When replacing component A with component B in an ensemble causes a regression, suggesting the removed component had unique predictive value.
- **Action:** Include both A and B in the ensemble instead of choosing one. A regression from swapping suggests the components are complementary. If the combined ensemble beats both individual variants, keep it; otherwise revert to the better single variant.
- **Exceptions:** none
- **Support:** kernels 49524919, 7573212; comps google-quest-challenge, hms-harmful-brain-activity-c; tiers {'Grandmaster': 1, 'Contributor': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/sweep/new_idea/part1
- **Examples:**
  - `49524919:e33#3` (hms-harmful-brain-ac, Grandmaster; steps 49524919:152->153, 49524919:157->158): After sweeping individual model groups and finding none matches the ensemble best, re-enable all groups and submit the full blend. Expect the blend to exceed the prior best if you improved individual components during the sweep (e.g., better checkpoints).
  - `7573212:e7#2` (google-quest-challen, Contributor; steps 7573212:11->12, 7573212:12->13): Include both A and B in the ensemble instead of choosing one. A regression from swapping suggests the removed component had unique value. Adding both increases diversity. If the combined ensemble beats both individual variants, keep it; otherwise revert to the better single variant.

## 85. sweep_individual_models_before_blending  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When you have multiple trained checkpoints or model variants with unknown relative LB performance and plan to build an ensemble.
- **Action:** Submit each variant individually to the leaderboard first to establish per-variant scores. Do not stop early based on a bad result—complete the full sweep when variant count is small (≤5-8). Then use the collected LB scores to guide ensemble composition and weights. Only after identifying the best single recipe, scale up by adding folds/seeds from that recipe.
- **Exceptions:** none
- **Support:** kernels 52200959, 55621328; comps hms-harmful-brain-activity-c, learning-agency-lab-automate; tiers {'Master': 2}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L3/sweep/new_idea/part1
- **Examples:**
  - `52200959:e4#1` (hms-harmful-brain-ac, Master; steps 52200959:20->21, 52200959:21->22, 52200959:22->23): Submit every variant individually to the leaderboard, recording each score. Do not stop early based on a bad result — complete the full sweep. Then use the collected LB scores to set ensemble weights. This is justified when CV-LB rank correlation is uncertain and the variant count is small enough to afford full enumeration.
  - `55621328:e16#1` (learning-agency-lab-, Master; steps 55621328:37->38, 55621328:39->40, 55621328:40->41, 55621328:41->42): First sweep single-checkpoint variants one at a time to identify the best training recipe on the leaderboard. Once the best recipe is found, scale up by adding all available folds from that recipe, then add multi-seed full-train checkpoints. Do not mix recipes until you know which single recipe is strongest. Adjust post-processing thresholds for each variant using local validation before submitting.

## 86. fix_infrastructure_before_judging_variable  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** When a run fails or produces suspicious/broken output after changing an experimental variable (e.g., checkpoint, config).
- **Action:** First check whether the failure is due to infrastructure issues (config paths, argument mismatches, data loading) rather than the variable itself. Fix the infrastructure, then re-submit. Do not count the failed run as evidence against the experimental variable.
- **Exceptions:** none
- **Support:** kernels 15082684, 52860091; comps hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Master': 1, 'Grandmaster': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L3/sweep/new_idea/part1
- **Examples:**
  - `15082684:e2#1` (ranzcr-clip-catheter, Master; steps 15082684:3->4, 15082684:4->5, 15082684:5->6, 15082684:6->7): Submit a handful of checkpoints spanning different training runs and epochs. If none beat the current best after ~5-6 tries and the CV-to-LB correlation appears weak (high CV doesn't yield high LB), stop the sweep and change approach rather than exhaustively testing all checkpoints. Track the best LB explicitly and revert to it before moving on.
  - `52860091:e2#2` (hms-harmful-brain-ac, Grandmaster; steps 52860091:5->6, 52860091:6->7): If a run fails or looks wrong after changing an experimental variable, first check whether the failure is due to infrastructure (config, paths, arguments) rather than the variable itself. Fix the infrastructure, then submit. Do not count the failed run as evidence against the variable.

## 87. enumerate_then_ensemble_small_option_sets  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** The option space is small enough to enumerate completely (e.g., <10 checkpoints or model variants) and individual options show small, noisy score differences on the leaderboard.
- **Action:** Submit each option once to get a rough ranking. If score differences between top options are small relative to noise, stop trying to pick a single winner and instead ensemble the top 2-3 candidates. Do not re-test the same option expecting different results unless another variable has changed.
- **Exceptions:** 7606235:e2#2 notes the author re-tested options and got different scores, suggesting uncontrolled variables in the pipeline.
- **Support:** kernels 52860091, 7606235; comps google-quest-challenge, hms-harmful-brain-activity-c; tiers {'Grandmaster': 1, 'Master': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/sweep/new_idea/part2
- **Examples:**
  - `52860091:e2#1` (hms-harmful-brain-ac, Grandmaster; steps 52860091:4->5, 52860091:5->6, 52860091:7->8): Swap checkpoints one at a time in the inference pipeline, submit each, and track LB scores. If a checkpoint scores worse, move on immediately. Keep the best-scoring checkpoint and, once you have scores for several, ensemble the top performers as the next step.
  - `7606235:e2#2` (google-quest-challen, Master; steps 7606235:10->11, 7606235:11->12, 7606235:12->13, 7606235:13->14): Enumerate all options once to get a rough ranking. If score differences between options are small relative to noise, stop trying to pick a single winner and instead ensemble the top candidates. Do not re-test options expecting different results unless you've changed something else.

## 88. revert_immediately_on_clear_single_variable_regression  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** A single-variable change (e.g., switching regularization type, applying a transformation universally) produces a score drop clearly larger than typical noise.
- **Action:** Immediately revert the change in the next iteration. Redirect effort to tuning the previously better variant's hyperparameters or to a different lever entirely. Do not spend multiple iterations trying to rescue the clearly inferior variant.
- **Exceptions:** none
- **Support:** kernels 73937748, 7548275; comps equity-post-hct-survival-pre, google-quest-challenge; tiers {'Master': 1, 'Expert': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L3/sweep/new_idea/part2
- **Examples:**
  - `73937748:e11#2` (equity-post-hct-surv, Master; steps 73937748:32->33, 73937748:33->34): Immediately revert the change in the next iteration rather than trying to tune the new variant. Redirect effort to tuning the previously better variant's hyperparameters or to a different lever entirely (e.g., adding base models). Do not spend multiple iterations trying to rescue a clearly inferior component.
  - `7548275:e6#2` (google-quest-challen, Expert; steps 7548275:23->24, 7548275:24->25, 7548275:25->26): When a transformation applied to all features/columns regresses versus a subset, revert to selective application. Use per-column validation metrics to identify which columns benefit. Then expand the selected set incrementally, submitting after each addition, and stop when gains plateau or turn negative.

## 89. never_bundle_cleanup_with_experimental_revert  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** You want to revert an unsuccessful experimental change and also clean up dead code or remove an inference block in the same submission.
- **Action:** Submit the experimental revert alone first to confirm the score impact. Only then clean up dead code in a separate submission. Bundling functional changes with refactoring makes regressions unattributable.
- **Exceptions:** none
- **Support:** kernels 13577502, 53424936; comps hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Expert': 1, 'Master': 1}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L3/sweep/new_idea/part2
- **Examples:**
  - `13577502:e3#2` (ranzcr-clip-catheter, Expert; steps 13577502:8->9): Revert to the configuration that produced the best score, then change only one variable at a time. Do not attempt to salvage the new combination—return to the known-good baseline first, then re-explore incrementally.
  - `53424936:e9#2` (hms-harmful-brain-ac, Master; steps 53424936:26->27): Never bundle code cleanup that removes functional inference blocks with a targeted experimental revert in the same submission. Submit the revert alone first to confirm the score, then clean up dead code in a separate submission. A regression after a combined change is unattributable.

## 90. add_resource_heavy_member_by_swap_then_restore  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** Adding a large new model to an already-large ensemble may exceed resource limits or dilute quality, and some existing members may be redundant.
- **Action:** First add the new member while disabling several existing members to create headroom. Submit to verify the new member works. Then re-enable disabled members one at a time, submitting after each, to find the best subset. Keep the configuration that achieved the best score.
- **Exceptions:** 18523075:e6#1 notes the author did not revert a regression, prioritizing exhaustive coverage over strict greedy improvement.
- **Support:** kernels 18523075, 49524919; comps commonlitreadabilityprize, hms-harmful-brain-activity-c; tiers {'Expert': 1, 'Grandmaster': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/sweep/new_idea/part2
- **Examples:**
  - `18523075:e6#1` (commonlitreadability, Expert; steps 18523075:11->12, 18523075:12->13, 18523075:13->14, 18523075:14->15): First add the new member while disabling several existing members to create headroom. Submit to verify the new member works. Then re-enable disabled members one at a time, submitting after each, to find the best subset. Stop when all candidates have been tried. Keep the configuration that achieved the best score.
  - `49524919:e33#1` (hms-harmful-brain-ac, Grandmaster; steps 49524919:148->149, 49524919:149->150, 49524919:150->151, 49524919:151->152): Disable all model groups except one (using skip/continue flags), submit each group's standalone predictions to the leaderboard, cycle through all groups to rank them, then re-enable all groups for the final blended submission. This reveals which groups are strong standalone and confirms the blend outperforms any individual member.

## 91. resubmit_identical_to_estimate_noise  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** Leaderboard score differences between configurations are small (comparable to or smaller than suspected evaluation noise), making single-submission comparisons unreliable.
- **Action:** Submit the same unchanged notebook multiple times to estimate the leaderboard noise floor. If noise is ~0.005-0.01, compare configurations using median or best-of-N scores across multiple runs rather than single submissions. Only declare a configuration better when the gap exceeds the observed noise range. For quick checks, one re-submission suffices; for close calls, use 5-8 runs.
- **Exceptions:** Consumes submission slots; may degenerate into cherry-picking the best random score rather than genuine noise estimation (50376011 counter_evidence).
- **Support:** kernels 13521245, 50376011; comps hms-harmful-brain-activity-c, ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 2}; episode reached new best: {'yes': 2}
- **Cells:** L3/sweep/new_resource
- **Examples:**
  - `13521245:e2#2` (ranzcr-clip-catheter, Grandmaster; steps 13521245:7->8, 13521245:9->10): After any significant score change, re-submit the identical code once to estimate leaderboard noise. If the re-run score is within ~0.005 of the original, treat the result as stable and proceed. If it diverges more, average mentally and be cautious about small subsequent changes.
  - `50376011:e10#1` (hms-harmful-brain-ac, Grandmaster; steps 50376011:41->42, 50376011:43->44, 50376011:44->45, 50376011:45->46): Submit the same unchanged notebook multiple times (5-8 runs) to estimate the noise floor of the leaderboard metric. Then compare the best or median score of each configuration across multiple runs rather than relying on single submissions. Only declare a winner when the gap exceeds the observed noise range.

## 92. toggle_transform_in_isolation_before_fixing  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** A prediction transform (e.g., sqrt, power transform) or calibration step gave mixed or confounded signals about whether it helps, because other changes were made simultaneously.
- **Action:** Test the transform in isolation by toggling it on/off with all other settings held constant. If removing it hurts, restore it immediately and treat it as a fixed component for subsequent tuning. Do not re-test unless the ensemble composition changes substantially. Note that rank-based averaging may implicitly replace calibration transforms.
- **Exceptions:** When switching to rank-based averaging, calibration transforms become redundant since ranks replace raw probabilities (15164527 counter_evidence).
- **Support:** kernels 15164527, 75584724; comps equity-post-hct-survival-pre, ranzcr-clip-catheter-line-cl; tiers {'Expert': 1, 'Master': 1}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L3/sweep/new_resource
- **Examples:**
  - `15164527:e4#3` (ranzcr-clip-catheter, Expert; steps 15164527:6->7, 15164527:7->8): Test the transform in isolation by toggling it on/off with all other settings held constant. If removing it hurts, restore it immediately and treat it as a fixed component for subsequent tuning. Do not re-test it unless the ensemble composition changes substantially.
  - `75584724:e6#2` (equity-post-hct-surv, Master; steps 75584724:11->12, 75584724:12->13, 75584724:13->14): After a regression from bundled changes, revert one variable at a time while keeping others fixed. Submit after each single change to isolate which factor caused the regression. Once the beneficial change is identified, re-apply the other change on top of it to check for interaction.

## 93. reverse_direction_on_regression_then_reduce_step  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** During a leaderboard hyperparameter or blend-weight sweep, a parameter change causes a clear score drop compared to the previous best.
- **Action:** Immediately reverse the direction of the parameter change, moving back toward the last best value with a smaller step size. Do not explore further in the regression direction unless there is a strong theoretical reason. If the reversal recovers or improves the score, bracket the optimum within a narrow range and stop.
- **Exceptions:** none
- **Support:** kernels 29588171, 7676170; comps amex-default-prediction, google-quest-challenge; tiers {'Master': 1, 'Contributor': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/sweep/none_visible
- **Examples:**
  - `29588171:e1#2` (amex-default-predict, Master; steps 29588171:6->7, 29588171:8->9): Immediately reverse the direction of the parameter change. Move back toward the last best value, possibly with a smaller step size. Do not explore further in the direction that caused the regression unless you have a strong theoretical reason.
  - `7676170:e1#2` (google-quest-challen, Contributor; steps 7676170:8->9, 7676170:9->10): After bracketing a hyperparameter optimum, test an extreme value far from the optimum (e.g., 5× larger) to confirm the direction of effect. If it confirms, return to the bracketed optimum but vary a co-parameter (e.g., regularization strength range) to check for interaction effects. If the combined change yields a new best, adopt both.

## 94. bisect_continuous_hyperparam_near_optimum  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** You are sweeping a continuous hyperparameter (e.g., blend weight, regularization), large steps cause regressions, and moderate steps yield small gains, suggesting the optimum is nearby.
- **Action:** Start with coarse steps to identify the improvement direction. When a step causes regression, reverse direction and halve the step size. When two consecutive submissions differ by less than noise, declare the optimum bracketed and stop sweeping that parameter. Move to a qualitatively different lever.
- **Exceptions:** 18426209:e7#1 shows the author did not strictly follow bisection—after regression at 0.65/0.35, they tried adding a third model rather than reversing direction on the same two-model weight.
- **Support:** kernels 18426209, 55591012; comps commonlitreadabilityprize, learning-agency-lab-automate; tiers {'Expert': 1, 'Grandmaster': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L3/sweep/plateau
- **Examples:**
  - `18426209:e7#1` (commonlitreadability, Expert; steps 18426209:9->10, 18426209:10->11): Try shifting weight toward the model you believe is strongest in small increments (e.g., 0.5→0.65). If the LB score worsens, do not continue in that direction; instead try adding a previously-dropped model at low weight. If neither improves over the baseline, stop weight tuning and accept the prior best.
  - `55591012:e12#1` (learning-agency-lab-, Grandmaster; steps 55591012:41->42, 55591012:45->46, 55591012:46->47, 55591012:47->48): Start with coarse steps to identify the direction of improvement. When a step causes regression, reverse direction and halve the step size. When two consecutive submissions differ by less than noise (e.g., 0.0000 delta), declare the optimum bracketed and stop sweeping that parameter. Move to a qualitatively different lever.

## 95. fix_pipeline_bugs_before_continuing_sweep  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** During an ensemble tuning sweep, a model that should be strong performs unexpectedly poorly, or you discover a data/model mismatch (e.g., shape mismatch, dead code, preprocessing inconsistency).
- **Action:** Stop the weight search. Fix the bug, then re-run the best-known ensemble configuration to get a clean baseline before further tuning. Do not continue optimizing weights on top of a buggy pipeline.
- **Exceptions:** none
- **Support:** kernels 50496431, 55591012; comps hms-harmful-brain-activity-c, learning-agency-lab-automate; tiers {'Grandmaster': 2}; episode reached new best: {'yes': 2}
- **Cells:** L3/sweep/plateau
- **Examples:**
  - `50496431:e56#3` (hms-harmful-brain-ac, Grandmaster; steps 50496431:227->228, 50496431:228->229): When a model that should be strong performs poorly in the ensemble, inspect its data pipeline for shape mismatches or preprocessing inconsistencies before continuing the weight search. Fix the bug, then re-run the best-known ensemble configuration to get a clean baseline before further tuning.
  - `55591012:e12#3` (learning-agency-lab-, Grandmaster; steps 55591012:39->40, 55591012:40->41): When integrating a new component, first run locally without submitting to verify it doesn't break the pipeline and check CV. Only submit after confirming CV is reasonable. If the new component doesn't help on CV, revert it before spending a submission.

## 96. confirm_multifactor_change_before_iterating  [L3]  —  2 kernels, 2 comps, 2 items

- **Context:** You have made multiple simultaneous modifications (e.g., new model versions + new blend weights, or several HPs at once) and the notebook has stochastic elements.
- **Action:** After a multi-factor change, re-run the notebook unchanged and submit to confirm the score before making further modifications. This separates the signal of the change from run-to-run variance. Only proceed to the next iteration after confirming improvement.
- **Exceptions:** none
- **Support:** kernels 60759531, 77450317; comps equity-post-hct-survival-pre, learning-agency-lab-automate; tiers {'Expert': 1, 'Grandmaster': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L3/sweep/regression
- **Examples:**
  - `60759531:e2#1` (learning-agency-lab-, Expert; steps 60759531:2->3, 60759531:3->4, 60759531:4->5, 60759531:5->6): Before tuning, snapshot the exact baseline configuration. If the first change regresses, fully revert to baseline before trying the next change. Never stack untested changes on top of a regression. Test one parameter at a time against the known-good baseline to isolate effects.
  - `77450317:e11#2` (equity-post-hct-surv, Grandmaster; steps 77450317:23->24, 77450317:24->25): After a multi-factor change, re-run the notebook unchanged and submit to confirm the score before making further modifications. This separates the signal of the change from run-to-run variance. Only proceed to the next iteration after confirming improvement.

## 97. match_inference_resolution_to_model  [L2]  —  2 kernels, 1 comps, 3 items

- **Context:** When running inference with a CNN (e.g., EfficientNet) and the test-time image resolution must be chosen, especially when switching between model checkpoints of different sizes.
- **Action:** Derive the test-time image resolution from the model's expected input shape (e.g., canonical resolution for the variant, or programmatically from model.input.shape) rather than hardcoding an arbitrary value. Mismatched resolution can cause significant score drops (e.g., 0.957 → 0.945). When the model checkpoint changes, always update the resolution accordingly.
- **Exceptions:** Auto-derived resolution may still produce poor scores if the model checkpoint itself failed to load correctly (13521245:e4#2).
- **Support:** kernels 13521245, 13702907; comps ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 2, 'Contributor': 1}; episode reached new best: {'yes': 2, 'no': 1}
- **Cells:** L2/input_resolution_selection
- **Examples:**
  - `13521245:e2#1` (ranzcr-clip-catheter, Grandmaster; steps 13521245:6->7, 13521245:8->9): Start with the canonical resolution for the model variant, then try one step above and one below. Pick the resolution that scores best. For EfficientNet B7, the canonical resolution is 600; try 528 and 600 and keep the winner. Two or three trials suffice to bracket the optimum.
  - `13521245:e4#2` (ranzcr-clip-catheter, Grandmaster; steps 13521245:12->13): Derive the test-time image resolution from the loaded model's input shape (e.g., model.input.shape) rather than hardcoding it. This eliminates resolution mismatch errors when switching between model checkpoints of different EfficientNet variants.
  - `13702907:e8#1` (ranzcr-clip-catheter, Contributor; steps 13702907:20->21, 13702907:21->22): Increase input resolution to the next available checkpoint size, update both the decoder target size and the model weights path simultaneously, then submit. If the score improves, re-run once to confirm it is not noise. If confirmed, lock in that resolution.

## 98. hierarchical_blending_for_correlated_models  [L2]  —  2 kernels, 1 comps, 2 items

- **Context:** When ensembling multiple model predictions where some sources are correlated (same architecture, similar training, or meta-learner trained on base model outputs) and others are more independent.
- **Action:** Group correlated predictors into sub-averages first, then combine sub-group means at a second level using a separate weighted average. This prevents correlated models from dominating. Give groups with more diverse/independent predictions slightly higher weight. Do not simply append meta-learner predictions into the same flat averaging pool as base models.
- **Exceptions:** When public LB feedback is very noisy (e.g., 7 rows), further refinement within the hierarchical scheme may regress (18837555:e5#1). Optimal structure may require more than two levels when additional diverse components are added (17616127:e10#2).
- **Support:** kernels 17616127, 18837555; comps commonlitreadabilityprize; tiers {'Contributor': 1, 'Expert': 1}; episode reached new best: {'yes': 2}
- **Cells:** L2/ensemble_blending_method
- **Examples:**
  - `17616127:e10#2` (commonlitreadability, Contributor; steps 17616127:37->38, 17616127:39->40, 17616127:40->41, 17616127:41->42): Do not simply append meta-learner predictions into the same averaging pool as base models. Instead, average base models within their group first, then combine the group mean with the meta-learner output using a separate weighted average. Give the base model group higher weight (e.g., 5/12 vs 4/12) since it aggregates more diverse predictions.
  - `18837555:e5#1` (commonlitreadability, Expert; steps 18837555:14->15, 18837555:15->16): Group correlated predictors into sub-averages first, then combine sub-group means with equal weight. This prevents correlated models from dominating. Try a balanced split (roughly equal-sized groups), submit, then refine by adjusting within-group weights. Stop when a refinement regresses.

## 99. expand_feature_set_before_engineering_interactions  [L2]  —  2 kernels, 1 comps, 2 items

- **Context:** When a GBDT model uses a small manually-selected subset of available features and scores poorly, before investing in crafting interaction or derived features.
- **Action:** Progressively expand the feature set by adding batches of unused features ordered by importance, validating each expansion. Simultaneously simplify unnecessary preprocessing (imputation, scaling, outlier removal) that GBDTs handle natively. Only after the feature set is comprehensive should you consider adding engineered interaction features.
- **Exceptions:** When all available features are already included (as in 27836972:e9#1), expansion is not possible and interaction engineering becomes the natural next step—though it may still not help.
- **Support:** kernels 27836972, 28093671; comps amex-default-prediction; tiers {'Expert': 1, 'Contributor': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L2/feature_engineering
- **Examples:**
  - `27836972:e9#1` (amex-default-predict, Expert; steps 27836972:44->45, 27836972:46->47, 27836972:48->49, 27836972:49->50): Start with a broad set of interaction pairs, submit or validate, then systematically narrow: remove columns that hurt CV one at a time, try both raw-level and aggregated-level (last, mean) variants separately, and compare CV. If the broad set doesn't beat baseline, try subsets before abandoning. Keep only the minimal set that improves CV.
  - `28093671:e8#1` (amex-default-predict, Contributor; steps 28093671:34->35, 28093671:35->36, 28093671:36->37): Progressively expand the feature set: first add the next batch of important features and submit to confirm improvement, then add more, and finally switch to automatic aggregation of all available features. Simultaneously simplify preprocessing (remove imputation, scaling, outlier removal) that the GBDT doesn't need, since these steps may discard signal or add noise.

## 100. avoid_broad_feature_removal_from_regularized_gbdt  [L2]  —  2 kernels, 1 comps, 2 items

- **Context:** When using a well-regularized GBDT (with feature subsampling, bagging, early stopping) and you suspect broad categories of engineered features (e.g., all max/min aggregations, or permutation-importance-flagged features) are adding noise.
- **Action:** Do not manually remove broad categories of engineered features by name pattern or a single importance run. If a targeted exclusion regresses the score, revert it. Instead, if importance-based removal hurts, regenerate importance with a different seed/method, compare lists, and only drop features consistently ranked unimportant across runs. The model's built-in regularization handles most irrelevant features.
- **Exceptions:** Feature-selection ratio tuning (e.g., keeping top 50%) can still help; the rule applies to categorical exclusion by feature-name pattern or a single noisy importance ranking.
- **Support:** kernels 27389424, 27799930; comps amex-default-prediction; tiers {'Grandmaster': 1, 'Contributor': 1}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L2/feature_selection
- **Examples:**
  - `27389424:e9#2` (amex-default-predict, Grandmaster; steps 27389424:67->68, 27389424:68->69, 27389424:69->70): Do not manually remove broad categories of engineered features (max, min, shift) from a regularized GBDT—the model's built-in feature subsampling and early stopping handle irrelevant features. If a targeted exclusion regresses the score, revert it and keep all features.
  - `27799930:e9#2` (amex-default-predict, Contributor; steps 27799930:64->65): Rather than simply dropping fewer features, regenerate the importance analysis (possibly with a different seed or method) and construct a new drop list. Compare the two lists to identify features that appear in one but not the other—these borderline features are likely the ones causing the regression. Keep those borderline features and only drop the consistently unimportant ones.

## 101. sweep_feature_count_threshold_bidirectionally  [L2]  —  2 kernels, 1 comps, 2 items

- **Context:** When using high-dimensional features (e.g., TF-IDF) with an importance-based feature count cutoff and the current cutoff already produces a competitive score.
- **Action:** Sweep the feature count in both directions from the current value using a fixed step (e.g., ±500–1000). If both directions degrade the score, the current value is near-optimal—stop sweeping and move to a different lever (e.g., adding new raw features or toggling feature selection on/off). When adding new feature sources, test with and without feature selection enabled to determine if the selection list is too restrictive for the new features.
- **Exceptions:** none
- **Support:** kernels 55431616, 60197293; comps learning-agency-lab-automate; tiers {'Grandmaster': 1, 'Expert': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L2/feature_selection
- **Examples:**
  - `55431616:e4#1` (learning-agency-lab-, Grandmaster; steps 55431616:13->14, 55431616:14->15, 55431616:15->16): Sweep the feature count in both directions from the current value using a fixed step (e.g., ±1000). If both directions degrade the leaderboard score, the current value is near-optimal—stop the sweep and move to a different lever such as adding new raw features.
  - `60197293:e18#1` (learning-agency-lab-, Expert; steps 60197293:124->125, 60197293:125->126, 60197293:128->129, 60197293:129->130): First test the new features with feature selection enabled (to filter noise). If that underperforms, try without feature selection (letting the model see all new features). Compare both against the baseline without the new features. If the new features help only without feature selection, the selection list may be too restrictive. Adjust the feature count cutoff by small increments (±500-1000) to find the sweet spot.

## 102. advanced_pooling_for_small_text_regression  [L2]  —  2 kernels, 1 comps, 2 items

- **Context:** When fine-tuning a pretrained transformer (e.g., RoBERTa) for regression on a small text dataset (~2800 samples) and the current model uses simple CLS or mean pooling.
- **Action:** Experiment with richer pooling strategies: attention-based pooling over last hidden states, or weighted hidden-layer pooling (initialize layer weights as zeros for uniform weighting after softmax, concatenate mean-pooled and max-pooled representations). Validate via CV before submitting. Note that these changes alone on a single model may not beat a diverse ensemble, and combining with layer reinitialization can regress if layers don't converge—revert reinitialization before discarding the pooling change.
- **Exceptions:** Combined pooling + layer reinitialization regressed on LB in one case (18757376:e5#2). A single improved-pooling model did not beat a multi-variant ensemble (17371717:e3#2), suggesting architectural improvements to one model may not substitute for model diversity.
- **Support:** kernels 17371717, 18757376; comps commonlitreadabilityprize; tiers {'Master': 1, 'Expert': 1}; episode reached new best: {'no': 2}
- **Cells:** L2/pooling_strategy
- **Examples:**
  - `17371717:e3#2` (commonlitreadability, Master; steps 17371717:5->6, 17371717:6->7): Initialize hidden-layer weights as zeros (uniform weighting after softmax), apply softmax in the forward pass to ensure proper normalization, and concatenate mean-pooled and max-pooled representations across the weighted layers. Avoid initializing layer weights with random values, as this creates unstable gradients early in training.
  - `18757376:e5#2` (commonlitreadability, Expert; steps 18757376:6->7): Try adding attention-based pooling over the last hidden states and reinitializing the last N (e.g., 4) transformer encoder layers to the model's initializer range. Validate via CV before submitting, as these changes can hurt if the reinitialized layers don't converge properly with limited data. If LB regresses, revert the reinitialization before discarding the pooling change.

## 103. curate_base_model_subset_for_meta_learner  [L2]  —  2 kernels, 1 comps, 2 items

- **Context:** When a stacking meta-learner has access to many base-model OOF predictions of varying quality, and some may be noisy or redundant.
- **Action:** Curate a subset of base-model predictions rather than passing all to the meta-learner. Use iterative feature elimination: drop each base model one at a time and keep the removal if OOF score improves. Validate by toggling the filter off; if LB drops, keep the filter. Weak or redundant members add noise the meta-learner may not fully ignore.
- **Exceptions:** Benefit may be marginal (~0.001 in 75924487:e4#2); the meta-learner switch alone was insufficient without elimination in 73937748:e11#1.
- **Support:** kernels 73937748, 75924487; comps equity-post-hct-survival-pre; tiers {'Master': 2}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L2/stacking_meta_learner
- **Examples:**
  - `73937748:e11#1` (equity-post-hct-surv, Master; steps 73937748:29->30, 73937748:30->31, 73937748:31->32, 73937748:32->33): Start with Ridge regression as the stacking meta-learner on rank-transformed OOF predictions. Add iterative feature elimination (drop each base model, keep removal if OOF score improves). Then tune Ridge hyperparameters (alpha, fit_intercept, positive constraint) with Optuna. Prefer Ridge over Lasso: L1 sparsity is less useful when you already do explicit feature elimination, and Lasso tends to underperform on small meta-feature sets.
  - `75924487:e4#2` (equity-post-hct-surv, Master; steps 75924487:6->7, 75924487:7->8): Curate a subset of base-model predictions to feed the meta-learner rather than passing all available columns. Validate by toggling the filter off; if LB drops, keep the filter. Weak or redundant members add noise that the meta-learner may not fully ignore.

## 104. match_pooling_to_checkpoint_at_inference  [L3]  —  2 kernels, 1 comps, 2 items

- **Context:** When you have multiple trained checkpoints that were trained with different architectural variants (e.g., mean+max pooling vs. mean-only pooling) and need to select the best inference configuration.
- **Action:** Ensure the pooling strategy at inference matches the one used during training for each checkpoint. Sweep all valid (pooling, checkpoint) combinations and compare LB scores. If neither variant consistently wins, pick the one with the best single result and refine checkpoint choice within that variant. Do not mix a checkpoint trained with one pooling type with a different pooling type at inference.
- **Exceptions:** Sweeping a small number of combinations may be incomplete; the best combination may require a checkpoint not yet available (17371717:e13#1).
- **Support:** kernels 17371717, 18757376; comps commonlitreadabilityprize; tiers {'Master': 1, 'Expert': 1}; episode reached new best: {'no': 2}
- **Cells:** L2/pooling_strategy
- **Examples:**
  - `17371717:e13#1` (commonlitreadability, Master; steps 17371717:30->31, 17371717:31->32, 17371717:32->33): Alternate between the architectural variants, each time loading the checkpoint that was trained with that variant. Compare LB scores across all combinations. If neither variant consistently wins, pick the one with the best single result and refine the checkpoint choice within that variant.
  - `18757376:e5#2` (commonlitreadability, Expert; steps 18757376:6->7): Try adding attention-based pooling over the last hidden states and reinitializing the last N (e.g., 4) transformer encoder layers to the model's initializer range. Validate via CV before submitting, as these changes can hurt if the reinitialized layers don't converge properly with limited data. If LB regresses, revert the reinitialization before discarding the pooling change.

## 105. revert_or_restore_after_catastrophic_infrastructure_regression  [L3]  —  2 kernels, 1 comps, 2 items

- **Context:** An infrastructure or dependency refactoring (not a modeling change) causes a catastrophic score drop (>10% or near-random), and a single corrective attempt does not fully restore performance.
- **Action:** Revert to the last known-good version immediately rather than continuing incremental patches. Diagnose the root cause offline before re-attempting the refactoring. If the drop was caused by intentional ablation for diagnostics, keep the pre-ablation code intact (commented out) so restoration is trivial, complete the diagnostic sweep, then restore in one step.
- **Exceptions:** If the drop is from an intentional diagnostic ablation (not a real regression), do not panic-revert — complete the investigation first, then restore.
- **Support:** kernels 13521245, 15164527; comps ranzcr-clip-catheter-line-cl; tiers {'Grandmaster': 1, 'Expert': 1}; episode reached new best: {'no': 2}
- **Cells:** L3/fix/bug_or_error
- **Examples:**
  - `13521245:e4#3` (ranzcr-clip-catheter, Grandmaster; steps 13521245:11->12, 13521245:12->13, 13521245:13->14): If a dependency or infrastructure refactoring causes a large regression and one corrective attempt does not fully restore performance, revert to the last working version immediately rather than continuing to patch. Diagnose the root cause offline before re-attempting.
  - `15164527:e7#2` (ranzcr-clip-catheter, Expert; steps 15164527:23->24, 15164527:25->26, 15164527:30->31): Do not panic-revert after a catastrophic drop caused by intentional ablation. Complete the diagnostic sweep, then restore the full pipeline in one step. Keep the pre-ablation code intact (commented out) so restoration is trivial.

## 106. revert_large_feature_batch_after_regression  [L3]  —  2 kernels, 1 comps, 2 items

- **Context:** A large batch of new features was added and the leaderboard score regressed, and one or two compensating tweaks (loss tuning, postprocessing) fail to recover the prior best.
- **Action:** Revert the feature addition entirely rather than continuing to tune around it. Do not spend more than two recovery attempts. If you believe some features are valuable, add them in smaller subsets in future experiments.
- **Exceptions:** 55987255:e24#1 suggests that if you can confirm value by ablation (removing only the new features causes regression), keep them—but if recovery attempts fail, revert.
- **Support:** kernels 55987255, 58130512; comps learning-agency-lab-automate; tiers {'Master': 2}; episode reached new best: {'no': 2}
- **Cells:** L3/probe/new_idea/part1
- **Examples:**
  - `55987255:e24#1` (learning-agency-lab-, Master; steps 55987255:148->149, 55987255:150->151, 55987255:151->152): Add the full feature pipeline in one commit, submit to get a leaderboard signal, then if the score improves, keep it; if you want to verify the contribution, remove only that feature block and re-submit. If removal causes regression, the feature is confirmed valuable—restore it rather than leaving it removed.
  - `58130512:e34#1` (learning-agency-lab-, Master; steps 58130512:105->106, 58130512:106->107, 58130512:107->108): After adding a large feature batch, submit immediately to measure impact. If the score regresses and one or two small compensating tweaks (loss tuning, postprocessing) fail to recover the prior best, revert the feature addition entirely rather than continuing to tune around it. Do not spend more than two recovery attempts.

## 107. quick_feasibility_probe_before_model_family_swap  [L3]  —  2 kernels, 1 comps, 2 items

- **Context:** The current model family has plateaued or regressed despite hyperparameter tuning, and you want to try a fundamentally different approach.
- **Action:** Run a quick probe with the alternative model on a small number of folds without submitting. Check that the model is compatible with the task (e.g., regression vs classification) and produces valid predictions. If the probe fails or produces clearly worse results, revert immediately. Keep the probe to one or two versions before deciding.
- **Exceptions:** 7676170:e4#1 warns that hasty probes can miss fundamental mismatches (e.g., using a classifier for regression); verify task compatibility before coding.
- **Support:** kernels 7018718, 7676170; comps google-quest-challenge; tiers {'Expert': 1, 'Contributor': 1}; episode reached new best: {'yes': 1, 'no': 1}
- **Cells:** L3/probe/new_idea/part1
- **Examples:**
  - `7018718:e8#1` (google-quest-challen, Expert; steps 7018718:25->26, 7018718:26->27): Before reverting an architectural change that regressed, try at least one alternative checkpoint with the same architecture. A regression may be due to the specific checkpoint rather than the architecture itself. Only revert the architecture if multiple checkpoints consistently underperform.
  - `7676170:e4#1` (google-quest-challen, Contributor; steps 7676170:20->21): Run a quick probe with the alternative model on a small number of folds without submitting. Check validation output for basic feasibility (does it even produce valid predictions for the task?). If the probe fails or produces clearly worse results, revert to the previous model family immediately rather than tuning the new one. Keep the probe to one or two versions before deciding.

## 108. estimate_noise_before_trusting_deltas  [L3]  —  2 kernels, 1 comps, 2 items

- **Context:** When the effect size of a change is similar to or smaller than suspected run-to-run variance (e.g., identical or near-identical re-runs show score fluctuations comparable to the delta from a change).
- **Action:** Re-run identical code at least once to estimate submission noise. Only accept a change as real if its improvement exceeds 2× the observed run-to-run variance. Do not chase small regressions from cosmetic or no-op changes.
- **Exceptions:** This consumes submission budget; the author in 13542132 never achieved actionable conclusions because the re-run strategy consumed budget without yielding clear signal.
- **Support:** kernels 13542132, 13702907; comps ranzcr-clip-catheter-line-cl; tiers {'Master': 1, 'Contributor': 1}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L3/sweep/new_idea/part1
- **Examples:**
  - `13542132:e2#1` (ranzcr-clip-catheter, Master; steps 13542132:4->5, 13542132:5->6, 13542132:7->8): Before concluding a change helped or hurt, re-run the identical notebook at least once to estimate submission noise. If the variance across identical runs exceeds the observed delta from the change, do not trust a single regression as evidence the change is harmful. Only accept a change if it consistently outperforms across multiple runs.
  - `13702907:e8#2` (ranzcr-clip-catheter, Contributor; steps 13702907:21->22, 13702907:22->23): When a new-best score is achieved, re-run at least twice with no code changes to estimate the noise floor. Only count an improvement as real if it exceeds 2× the observed run-to-run variance. Do not chase small regressions from cosmetic or no-op changes.

## 109. change_one_variable_at_a_time_when_effects_small  [L3]  —  2 kernels, 1 comps, 2 items

- **Context:** When the expected effect size of each change is small (differences ~0.001 or less) and you want to explore multiple hyperparameters.
- **Action:** After bracketing an optimum on one hyperparameter, revert it to the best-known value and change only the second hyperparameter. Never change two hyperparameters simultaneously when the expected effect size is small, because a regression cannot be attributed. If you do change two and regress, revert both to the last-known-good state before continuing.
- **Exceptions:** 73671444 used forward-exploration instead of bisecting, which is faster when many untested model variants are queued but risks missing a valuable removed component.
- **Support:** kernels 73671444, 77129691; comps equity-post-hct-survival-pre; tiers {'Grandmaster': 1, 'Master': 1}; episode reached new best: {'yes': 2}
- **Cells:** L3/sweep/new_idea/part1
- **Examples:**
  - `73671444:e5#2` (equity-post-hct-surv, Grandmaster; steps 73671444:11->12, 73671444:12->13): Rather than reverting, add the next planned component and test it in isolation (solo weight=1.0). If the new component partially recovers the score, continue building the blend. This forward-exploration approach is faster than bisecting the regression when you have many untested model variants queued, but risks missing that a removed component (like postprocessing) was valuable.
  - `77129691:e3#2` (equity-post-hct-surv, Master; steps 77129691:8->9): After bracketing an optimum on one hyperparameter, revert it to the best-known value and change only the second hyperparameter. Never change two hyperparameters simultaneously when the expected effect size is small, because a regression cannot be attributed. If you do change two and regress, revert both to the last-known-good state before continuing.

## 110. move_on_after_quick_win_from_weight_tuning  [L3]  —  2 kernels, 1 comps, 2 items

- **Context:** When a small adjustment to blend weights yields a new best score but the gain is modest and the weight space has limited remaining search space.
- **Action:** After a quick win from blend weight tuning, move on to exploring new model components, architectures, or features rather than exhaustively searching the weight space. The marginal gain from fine-tuning weights among a few models is small compared to adding a genuinely complementary model.
- **Exceptions:** 18423958 author's subsequent model explorations (DistilBERT) performed worse, suggesting sometimes sticking with weight tuning is safer.
- **Support:** kernels 17371717, 18423958; comps commonlitreadabilityprize; tiers {'Master': 2}; episode reached new best: {'no': 1, 'yes': 1}
- **Cells:** L3/sweep/new_idea/part1
- **Examples:**
  - `17371717:e13#2` (commonlitreadability, Master; steps 17371717:29->30, 17371717:30->31, 17371717:31->32, 17371717:32->33): After a short sweep (3-4 trials) that brackets but does not beat the baseline, stop the sweep and use the directional signal (which variant scored best most often) to guide the next training run rather than continuing to permute inference-only combinations. Resume with a fresh checkpoint trained under the best-identified variant.
  - `18423958:e4#2` (commonlitreadability, Master; steps 18423958:9->10): After a quick win from blend weight tuning, move on to exploring new model components or architectures rather than exhaustively searching the weight space. The marginal gain from fine-tuning weights among a few models is small compared to adding a genuinely complementary model to the ensemble.

## 111. prefer_fixed_weights_on_noisy_leaderboard  [L3]  —  2 kernels, 1 comps, 2 items

- **Context:** The public leaderboard is computed on very few samples (e.g., <10 rows), making single-submission score comparisons unreliable, and you are considering data-adaptive or conditional blending logic.
- **Action:** Prefer fixed blend weights over data-adaptive conditional logic. If a conditional strategy does not clearly beat the simple fixed-weight version, revert to fixed weights immediately. On noisy leaderboards, try one alternative configuration after a regression before concluding the direction is unproductive, but do not iterate extensively on conditional approaches.
- **Exceptions:** none
- **Support:** kernels 18350823, 18426209; comps commonlitreadabilityprize; tiers {'Expert': 2}; episode reached new best: {'no': 2}
- **Cells:** L3/sweep/plateau
- **Examples:**
  - `18350823:e4#2` (commonlitreadability, Expert; steps 18350823:9->10, 18350823:11->12): On small or noisy leaderboards, prefer fixed blend weights over data-adaptive conditional logic. If a conditional strategy does not clearly beat the simple version, revert to fixed weights immediately rather than iterating on the conditional approach.
  - `18426209:e7#2` (commonlitreadability, Expert; steps 18426209:9->10, 18426209:10->11): After a regression on a noisy leaderboard, try one alternative configuration before concluding the direction is unproductive. If the alternative also fails or looks unpromising locally, revert to the known best and move on to a different lever entirely. Do not submit configurations that look worse locally.

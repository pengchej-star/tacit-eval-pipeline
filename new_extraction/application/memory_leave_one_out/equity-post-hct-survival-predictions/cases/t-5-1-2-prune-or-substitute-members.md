# Prune or substitute members  `T.5.1.2`   50 edits, 0 experts
43 scored cases (improvement signed by each competition's direction), median +0.00111, 29 improved


- expert 17616127 · commonlitreadabilityprize · v13→v14   Remove the member whose individual score is worst (or was worst when tested alone) and replace it with one or more checkpoints known to score better individually. Re-submit after each swap to confirm improvement. Increasing ensemble size helps only when the added members are competitive on their own
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.51072 → 0.47623 (lower is better; improved by 0.03450)
- expert 17616127 · commonlitreadabilityprize · v120→v121   Hold all other blend components and weights constant, swap only the candidate array in one slot, and submit. If the same candidate wins across different pipeline states, treat it as a robust choice. Avoid changing multiple components simultaneously.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score n/a → 0.44803 (lower is better)
- expert 17616127 · commonlitreadabilityprize · v141→v145   Test each source alone in the blend, then test both together. If swapping one for the other yields similar scores and combining both does not clearly improve over either alone, the sources are likely redundant; keep whichever is simpler or more stable.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.44790 → n/a (lower is better)
- expert 18550705 · commonlitreadabilityprize · v2→v9   First grow the ensemble by adding candidate models one at a time, recording the metric after each addition. Then prune: remove each member individually and keep the removal if the metric improves or stays flat. This greedy add-then-prune search identifies which members actually contribute complement
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows.
    leaderboard score 0.45681 → 0.45411 (lower is better; improved by 0.00270)
- expert 18550705 · commonlitreadabilityprize · v9→v10   Select candidate backbones whose pretraining objective matches the downstream task type (encoder-only for classification/regression). After integrating each candidate, measure the ensemble's validation metric. If the metric worsens, remove the member immediately rather than hoping it will help throu
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.45411 → 0.45300 (lower is better; improved by 0.00111)
- expert 18550705 · commonlitreadabilityprize · v11→v12   Remove members one group at a time and simplify the combination mechanism (e.g., replace a neural stacking head with a learned weighted average). If the score degrades, the removed members carried complementary information and should be restored. Track each removal's effect individually rather than 
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.45284 → 0.45330 (lower is better; worse by 0.00046)
- expert 18523075 · commonlitreadabilityprize · v9→v10   Remove the offending member and substitute a different pretrained backbone from the same or a related model family that may provide more complementary representations. Evaluate immediately on the leaderboard to confirm the swap recovers or improves the score before further tuning.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.45613 → 0.45545 (lower is better; improved by 0.00068)
- expert 18523075 · commonlitreadabilityprize · v12→v15   Toggle candidate members on/off one at a time, submitting after each change to measure the marginal effect. Keep a member only if it improves the metric. When a member hurts, disable it before testing the next candidate. The best score observed during the sweep identifies the optimal subset.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.45581 → 0.45516 (lower is better; improved by 0.00065)
- expert 18426209 · commonlitreadabilityprize · v6→v7   Remove the suspected weak member and redistribute its weight equally among the remaining members. Compare the leaderboard or validation score before and after. If the score improves, keep the pruned ensemble; a member that degrades standalone performance often also degrades a blend even at low weigh
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.45828 → 0.45658 (lower is better; improved by 0.00171)
- expert 18851026 · commonlitreadabilityprize · v20→v24   Toggle individual ensemble members in and out, submitting each configuration. A smaller-capacity model may outperform or complement better than a larger one if the larger model overfits. Remove members that do not improve the blend rather than always including all available predictions.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.45875 → 0.45925 (lower is better; worse by 0.00050)
- expert 18851026 · commonlitreadabilityprize · v29→v30   Ablate by removing one original member at a time and submitting. If every subset that includes the new member scores worse than the original pair, revert to the original ensemble. Track all combinations' scores to avoid circular changes.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.45819 → 0.45835 (lower is better; worse by 0.00015)
- expert 18423958 · commonlitreadabilityprize · v25→v26   Drop the weakest model family entirely from the ensemble rather than down-weighting it. Redistribute its weight among the remaining, stronger members and verify on the leaderboard or validation that the simpler blend improves.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.46010 → 0.45875 (lower is better; improved by 0.00136)
- expert 18350823 · commonlitreadabilityprize · v23→v24   Replace the stagnant member with a structurally different inference pipeline (e.g., different pooling method, different framework) that loads separately trained checkpoints. Average predictions across folds and seeds to reduce variance, then rebalance ensemble weights.
    evidence: ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.46172 → 0.46072 (lower is better; improved by 0.00100)
- expert 18350823 · commonlitreadabilityprize · v22→v24   Incrementally reduce the weight of a suspected weak member while increasing the weight of stronger ones. If the leaderboard score improves, this confirms the weak member is hurting the blend and justifies investing effort to replace it with a better alternative.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.46191 → 0.46072 (lower is better; improved by 0.00119)
- expert 7548275 · google · v19→v20   Ablate ensemble members one at a time by removing each model's predictions from the blend and re-submitting. Drop any member whose removal improves the score. A single weak member can degrade a rank-based metric disproportionately because noisy predictions distort the rank ordering.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.30421 → 0.39772 (higher is better; improved by 0.09351)
- expert 6803050 · google · v39→v49   Sweep checkpoint variants one at a time across all folds, then vary ensemble size (full k-fold vs. subsets). Submit each configuration to measure its effect. Track that more folds do not always help—if some folds are weaker, including them dilutes the ensemble. Keep the configuration that scores bes
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows.
    leaderboard score 0.38287 → 0.36824 (higher is better; worse by 0.01463)
- expert 53747598 · hms · v12→v15   Before adding new diverse models, prune or disable ensemble members that are suspected to hurt or not help (e.g., models using only a subset of available inputs). This reduces noise in the blend baseline and makes it easier to attribute gains to the newly added components.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.23270 → 0.22838 (lower is better; improved by 0.00432)
- expert 53424936 · hms · v22→v23   Perform leave-one-out ablation: remove one ensemble member at a time, adjust the averaging denominator, and submit. If the score improves, permanently exclude that member. This identifies members that add noise or are miscalibrated relative to the rest of the blend.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.22735 → 0.22645 (lower is better; improved by 0.00090)
- expert 53424936 · hms · v32→v33   Remove the suspected weak or redundant member, adjust the denominator accordingly, and submit. If the score improves, keep it removed. Iterate by trying removal of each member one at a time to identify which ones hurt the blend.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.22615 → 0.22600 (lower is better; improved by 0.00015)
- expert 50376011 · hms · v11→v16   Evaluate individual members in isolation to gauge their standalone quality, then compare against the full ensemble. If the full ensemble beats every individual member, keep it. If adding a weak member hurts, remove it. Use the gap between single-member and ensemble scores to judge ensemble benefit a
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.40647 → 0.46668 (lower is better; worse by 0.06021)
- expert 50376011 · hms · v22→v26   Test subsets of available checkpoints separately before combining them. Start with the known-best subset, try adding new members, and compare. If the expanded ensemble scores worse, revert to the smaller set. Prefer a compact ensemble of consistently strong members over a larger one that includes we
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.39939 → 0.39657 (lower is better; improved by 0.00282)
- expert 50376011 · hms · v27→v31   Sweep one group at a time with uniform weights, submitting each to the leaderboard. Compare scores across groups to identify the best-performing subset before attempting to combine groups or tune weights.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score n/a → 0.39254 (lower is better)
- expert 50376011 · hms · v33→v35   Re-test each candidate model variant individually under the new aggregation scheme, compare scores, and select the best. Do not assume the ranking from the previous setup transfers; a single controlled swap per submission is sufficient to compare two candidates.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.39142 → 0.39434 (lower is better; worse by 0.00292)
- expert 50376011 · hms · v58→v59   Track each checkpoint's leaderboard score across submissions. Pick two or more checkpoints that each score well individually but were trained under different conditions (different fold splits, training runs, or hyperparameters) to maximize diversity. Start with equal-weight averaging and submit to c
    evidence: ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.36034 → 0.34053 (lower is better; improved by 0.01982)
- expert 50376011 · hms · v170→v174   Sweep ensemble composition by adding or removing one member at a time and submitting each variant. Start from the current best subset, try the full set, then systematically drop each member to identify which ones hurt. Keep the subset that scores best.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.24948 → 0.24842 (lower is better; improved by 0.00106)
- expert 50376011 · hms · v184→v188   Test each candidate checkpoint individually and in small combinations, submitting multiple times for the same config when feasible. Prefer combinations that consistently score well across runs over single-run winners. Start with the best individual members, then add members incrementally; if adding 
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.24841 → 0.24815 (lower is better; improved by 0.00026)
- expert 50376011 · hms · v192→v199   Run a systematic single-checkpoint sweep: submit each fold checkpoint alone, record its standalone score, then rank them. Use these rankings to select the top-performing members for the final ensemble and drop weak ones. Expect that no single checkpoint will beat a well-chosen ensemble, but the swee
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows.
    leaderboard score 0.23903 → 0.24449 (lower is better; worse by 0.00546)
- expert 49524919 · hms · v133→v134   Completely disable the suspect model family (remove its predictions from the blend) while ensuring all other intended models run correctly. Compare the resulting score to the best achieved with the family included. If the score improves, permanently remove that family and clean up its code.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.25459 → 0.24021 (lower is better; improved by 0.01438)
- expert 49524919 · hms · v128→v134   First, test each model group in isolation by skipping all others and submitting its solo predictions to establish per-group quality. Fix any column-reference or control-flow bugs before blending. Then enable all groups that individually score well, blend them, and submit. After each change, verify t
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score n/a → 0.24021 (lower is better)
- expert 49524919 · hms · v134→v135   Use a two-phase approach: first disable the component and submit to confirm the improvement on the leaderboard, then in a follow-up commit fully remove the dead code. This preserves the option to revert if the improvement was spurious, while eventually reducing complexity and runtime.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.24021 → n/a (lower is better)
- expert 49524919 · hms · v146→v148   Remove the weaker component entirely from the ensemble rather than trying to down-weight it. Even small blend weights on a substantially worse model can hurt, and removing dead code paths may also eliminate subtle side effects on shared data structures or preprocessing.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.27167 → 0.23482 (lower is better; improved by 0.03685)
- expert 49524919 · hms · v148→v158   Isolate each model group by disabling all others, submit to get its standalone score, and swap checkpoint files within each group to find the best variant. Once the best checkpoint per group is identified, re-enable all groups and submit the full blend. This confirms each component's contribution an
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.23482 → 0.23032 (lower is better; improved by 0.00450)
- expert 52551258 · hms · v3→v5   Try swapping checkpoint selection (last-epoch vs best-validation) and toggling individual ensemble members one at a time, submitting after each change. If switching to best-validation checkpoints does not help, the final-epoch checkpoints may have been better regularized or the validation metric may
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.37116 → 0.37494 (lower is better; worse by 0.00378)
- expert 52200959 · hms · v35→v38   Include the weaker model in the blend with a proportionally smaller weight (derived from its standalone score). Even a model that is significantly worse alone can improve the ensemble if it is architecturally diverse, because it contributes complementary error patterns. Verify by submitting and comp
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.41865 → 0.32209 (lower is better; improved by 0.09657)
- expert 60264017 · learning · v1→v2   Swap the original member's predictions with the clean-data variant's predictions in the blending pipeline, keeping all other members and weights unchanged, and evaluate on the leaderboard. If the score improves, keep the clean variant; otherwise revert. This isolates the effect of data cleaning on t
    evidence: ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.82788 → 0.82941 (higher is better; improved by 0.00153)
- expert 60264017 · learning · v2→v6   Change one ensemble member at a time (add, remove, or swap a variant), re-optimize blend weights, and submit. Compare each result to the current best. If the score drops, revert that member and try a different swap. This isolates each member's marginal contribution and avoids confounding multiple ch
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.82941 → 0.82875 (higher is better; worse by 0.00066)
- expert 60264017 · learning · v4→v5   Before searching over different architectures, try swapping training variants of the same architecture (e.g., different data subsets, cleaning strategies, or loss functions) into the ensemble. Measure each variant's marginal contribution; a variant that decorrelates errors with existing members can 
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.82940 → 0.83110 (higher is better; improved by 0.00170)
- expert 60264017 · learning · v8→v12   Use greedy forward/backward selection on the leaderboard or a reliable validation set: add or remove one member per iteration, re-optimize blend weights each time, and submit. Keep the change only if the metric improves. Prefer a smaller ensemble when a larger one shows no gain, as fewer members red
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score n/a → 0.82997 (higher is better)
- expert 60264017 · learning · v12→v13   Prune multiple members at once and submit to measure the impact. If the score drops, the removed members collectively contributed positively; restore them and instead try removing one at a time to isolate truly redundant members. Aggressive bulk pruning risks conflating individual member effects.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.82997 → 0.82848 (higher is better; worse by 0.00149)
- expert 13702907 · ranzcr · v3→v4   Before committing to an ensemble, test each constituent model individually on the leaderboard or validation set. If one model dominates, submit it alone. Only ensemble models whose individual scores are close to or above the current best; drop any that pull the average down.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.94606 → 0.94772 (higher is better; improved by 0.00167)
- expert 50496431 · hms · v22→v23   When ablating an ensemble member, treat it as a single-variable experiment: remove only that member, submit, and immediately compare. If the score worsens, restore the member before making any other changes. Never stack an ablation with other modifications (e.g., preprocessing tuning), because the d
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.33898 → 0.39115 (lower is better; worse by 0.05217)
- expert 50496431 · hms · v44→v45   Enable or disable one model branch at a time and submit to the leaderboard (or evaluate on validation) to isolate its marginal contribution. Keep the branch enabled only if the score improves.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.37087 → 0.35027 (lower is better; improved by 0.02061)
- expert 50496431 · hms · v72→v75   Ablate ensemble members one at a time by toggling each on/off and submitting. Compare scores to the full-ensemble baseline. Remove any member whose exclusion improves the score. Do this iteratively, re-checking after each removal, because interactions between members can shift.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score n/a → 0.27839 (lower is better)
- expert 50496431 · hms · v80→v81   After modifying any single ensemble member, re-test inclusion/exclusion of every other member one at a time. Do not assume a previously helpful member is now unnecessary just because another member was upgraded; architecturally diverse models (e.g., 2D vs 3D backbones) often remain complementary.
    evidence: ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.29794 → 0.27445 (lower is better; improved by 0.02349)
- expert 50496431 · hms · v104→v106   Remove the member in a controlled submission where no other change is made (or where other changes are subsequently reverted). If the score worsens, the member is contributing positively and should be kept. Avoid confounding the removal with other simultaneous changes.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.27115 → 0.28677 (lower is better; worse by 0.01561)
- expert 50496431 · hms · v137→v138   Toggle one member at a time (swap in the alternative, swap out the current best contributor) and submit. If the score degrades, keep the original member. Do not change multiple factors simultaneously when testing a single member's contribution, or the signal is confounded.
    evidence: ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.25172 → 0.25541 (lower is better; worse by 0.00370)
- expert 50496431 · hms · v148→v154   Change one or two factors per submission. When a change worsens the score, revert it before trying the next change. When a change improves or matches the score, keep it as the new baseline. Confirm the final configuration with a re-run to check for noise. This greedy coordinate-search with reversion
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.23064 → 0.23127 (lower is better; worse by 0.00063)
- expert 50496431 · hms · v156→v158   Swap one ensemble slot at a time, submitting each variant, and compare leaderboard scores. Keep the member that yields the best score. If a preprocessing change is made simultaneously, re-test the member choice because the best member can change with preprocessing.
    evidence: ✓ A plausible candidate has errors different from the current ensemble on the same validation rows. | ✓ A member or group has weak or redundant marginal contribution in earlier ablations.
    leaderboard score 0.26843 → 0.24233 (lower is better; improved by 0.02610)
- expert 50496431 · hms · v161→v163   Revert to the proven ensemble composition that excludes the new model. Keep the new model code available for future tuning but do not force it into the blend. Gains often come from re-tuning preprocessing or other parameters alongside the established members rather than from the new architecture its
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation.
    leaderboard score 0.26705 → 0.22940 (lower is better; improved by 0.03765)
- expert 50496431 · hms · v218→v230   Alternate between two axes: (1) toggle individual members in/out, and (2) switch between equal-weight averaging and a hand-tuned weighted blend. Submit each variant. When adding members with a weighted blend beats the simple mean, keep the larger set; when a member's inclusion consistently hurts, dr
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ A plausible candidate has errors different from the current ensemble on the same validation rows.
    leaderboard score 0.24602 → 0.22550 (lower is better; improved by 0.02052)
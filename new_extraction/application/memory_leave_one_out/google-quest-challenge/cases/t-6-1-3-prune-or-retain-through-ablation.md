# Prune or retain through ablation  `T.6.1.3`   105 edits, 0 experts
91 scored cases, median improvement -0.00020, 41 improved


- expert 17616127 (Contributor) · commonlitreadabilityprize · v8→v10   Stop searching for a single superior checkpoint after a few failed attempts. Instead, return to ensembling: add the best new checkpoints into a weighted blend, which is more likely to improve the score than any single-model swap.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ One member is consistently weak and a compatible replacement is available. | ✓ A candidate has nonredundant errors and plausible standalone quality.
    leaderboard score 0.50693 → 0.48130 (-0.02563)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v14→v18   Try averaging predictions from the homogeneous set, but compare against the existing diverse blend before committing. Diversity across architectures often matters more than quantity of same-architecture members; do not discard the heterogeneous blend unless the homogeneous one clearly wins on valida
    evidence: ✓ A previously better ensemble lost members during a recent change. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.47623 → 0.48999 (+0.01376)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v60→v65   Test the single-family subset alone to measure its standalone quality, then incrementally re-add the other components. If the simplified version scores worse, the diversity from multiple families is genuinely contributing. Restore the full blend and focus on weight tuning rather than removing member
    evidence: ✓ A previously better ensemble lost members during a recent change. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.45499 → 0.45576 (+0.00077)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v85→v86   Isolate the new backbone by submitting its fold-averaged predictions alone. If the score is worse than the ensemble, the backbone is valuable only as a diversity contributor, not a replacement. Re-incorporate it into the blend rather than using it solo.
    evidence: ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.45142 → 0.46303 (+0.01161)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v85→v86   Probe each backbone family in isolation by submitting its fold-averaged predictions. If every single-family probe underperforms the multi-family blend by a consistent margin, treat cross-family diversity as essential and keep all families in the final ensemble.
    evidence: ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.45142 → 0.46303 (+0.01161)
- expert 17616127 (Contributor) · commonlitreadabilityprize · v113→v114   Isolate the new model by disabling all other ensemble components and submit its raw predictions. Compare the standalone score to the ensemble baseline to gauge whether and how much weight it should receive in the blend.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score n/a → 0.46520
- expert 17616127 (Contributor) · commonlitreadabilityprize · v120→v121   Hold all other blend components and weights constant, swap only the candidate array in one slot, and submit. If the same candidate wins across different pipeline states, treat it as a robust choice. Avoid changing multiple components simultaneously.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score n/a → 0.44803
- expert 18550705 (Master) · commonlitreadabilityprize · v2→v9   First grow the ensemble by adding candidate models one at a time, recording the metric after each addition. Then prune: remove each member individually and keep the removal if the metric improves or stays flat. This greedy add-then-prune search identifies which members actually contribute complement
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ A candidate has nonredundant errors and plausible standalone quality.
    leaderboard score 0.45681 → 0.45411 (-0.00270)
- expert 18550705 (Master) · commonlitreadabilityprize · v5→v9   Evaluate each candidate's marginal contribution by adding it and checking the ensemble metric. If the metric worsens or stays flat, remove it: on small, noisy datasets a weaker member can degrade a stacking meta-learner even if it is architecturally diverse, because the meta-learner overfits to the 
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.45353 → 0.45411 (+0.00058)
- expert 18550705 (Master) · commonlitreadabilityprize · v9→v10   Select candidate backbones whose pretraining objective matches the downstream task type (encoder-only for classification/regression). After integrating each candidate, measure the ensemble's validation metric. If the metric worsens, remove the member immediately rather than hoping it will help throu
    evidence: ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.45411 → 0.45300 (-0.00111)
- expert 18550705 (Master) · commonlitreadabilityprize · v11→v12   Remove members one group at a time and simplify the combination mechanism (e.g., replace a neural stacking head with a learned weighted average). If the score degrades, the removed members carried complementary information and should be restored. Track each removal's effect individually rather than 
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.45284 → 0.45330 (+0.00046)
- expert 18523075 (Expert) · commonlitreadabilityprize · v8→v9   After each backbone addition, check whether the leaderboard score improves. When a new backbone fails to improve the score despite architectural diversity, suspect that either the new model's individual quality is too low or the ensemble is saturated. Revert or replace it with a stronger checkpoint 
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.45565 → 0.45613 (+0.00048)
- expert 18523075 (Expert) · commonlitreadabilityprize · v12→v15   Toggle candidate members on/off one at a time, submitting after each change to measure the marginal effect. Keep a member only if it improves the metric. When a member hurts, disable it before testing the next candidate. The best score observed during the sweep identifies the optimal subset.
    evidence: ✓ A previously better ensemble lost members during a recent change. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A candidate has nonredundant errors and plausible standalone quality.
    leaderboard score 0.45581 → 0.45516 (-0.00065)
- expert 18426209 (Expert) · commonlitreadabilityprize · v6→v7   Remove the suspected weak member and redistribute its weight equally among the remaining members. Compare the leaderboard or validation score before and after. If the score improves, keep the pruned ensemble; a member that degrades standalone performance often also degrades a blend even at low weigh
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.45828 → 0.45658 (-0.00171)
- expert 18851026 (Master) · commonlitreadabilityprize · v20→v24   Toggle individual ensemble members in and out, submitting each configuration. A smaller-capacity model may outperform or complement better than a larger one if the larger model overfits. Remove members that do not improve the blend rather than always including all available predictions.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.45875 → 0.45925 (+0.00050)
- expert 18851026 (Master) · commonlitreadabilityprize · v29→v30   Ablate by removing one original member at a time and submitting. If every subset that includes the new member scores worse than the original pair, revert to the original ensemble. Track all combinations' scores to avoid circular changes.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.45819 → 0.45835 (+0.00015)
- expert 18423958 (Master) · commonlitreadabilityprize · v10→v13   Include the weaker model in the blend with a small weight rather than discarding it. Verify on the leaderboard or validation that the expanded ensemble improves over the blend without it; if the gain is marginal or negative, remove it to reduce complexity.
    evidence: ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score 0.45979 → 0.45939 (-0.00040)
- expert 18423958 (Master) · commonlitreadabilityprize · v17→v21   Add the weaker model family with a small blend weight (e.g., 0.2) and verify the ensemble score. If it does not improve the score, remove it rather than keeping it. Always check that the blending arithmetic is correct before drawing conclusions about the model's contribution.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score 0.45975 → 0.46031 (+0.00056)
- expert 18423958 (Master) · commonlitreadabilityprize · v25→v26   Drop the weakest model family entirely from the ensemble rather than down-weighting it. Redistribute its weight among the remaining, stronger members and verify on the leaderboard or validation that the simpler blend improves.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.46010 → 0.45875 (-0.00136)
- expert 18350823 (Expert) · commonlitreadabilityprize · v14→v15   Save each component's standalone predictions as a separate submission file during inference. Submit both the ensemble and the single-component file to compare their scores, revealing whether the component is individually strong or only helpful through diversity in the blend.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.46250 → 0.46161 (-0.00088)
- expert 18350823 (Expert) · commonlitreadabilityprize · v15→v16   Submit the single strong component alone as a probe. If the score degrades (as is typical when the ensemble provides complementary error cancellation), revert to the ensemble and instead adjust blend weights to give the strong component more influence.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.46161 → 0.47653 (+0.01491)
- expert 18350823 (Expert) · commonlitreadabilityprize · v15→v16   Submit each component model individually to measure the gap between the best single model and the ensemble. If the gap is substantial (e.g., several percent of the metric), continue investing in blend-weight optimization rather than simplifying.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.46161 → 0.47653 (+0.01491)
- expert 18350823 (Expert) · commonlitreadabilityprize · v33→v38   Add one candidate model at a time and evaluate the new ensemble against the previous best. If the score worsens, remove that candidate before trying the next. A weaker individual model can drag down a simple average ensemble even if it adds diversity; only keep additions that demonstrably improve th
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score n/a → 0.46026
- expert 18757376 (Expert) · commonlitreadabilityprize · v4→v6   Selectively disable individual ensemble members one at a time and adjust the blend weights between the stacking meta-model output and direct base-model predictions. Evaluate each removal/reweighting on the leaderboard or CV. Removing a weak contributor and shifting weight toward stronger components 
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.46496 → 0.46094 (-0.00403)
- expert 17371717 (Master) · commonlitreadabilityprize · v5→v7   Probe by building the single improved model and comparing against the ensemble baseline. Expect that a single model, even with better pooling, is unlikely to match the diversity benefit of ensembling multiple variants. If the single model scores worse, revert to the ensemble approach or use the new 
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.47148 → 0.47432 (+0.00284)
- expert 73671444 (Grandmaster) · equity · v19→v21   Test a pure single-model submission and an equal-weight blend. If the difference is negligible, keep the equal blend for robustness but do not invest further in tuning weights between these two. Instead, seek diversity from a genuinely different model family or feature set. Adding more correlated mo
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A candidate has nonredundant errors and plausible standalone quality.
    leaderboard score 0.69416 → 0.69417 (+0.00000)
- expert 73671444 (Grandmaster) · equity · v21→v24   First blend the new model into the existing ensemble and submit. Then isolate the new model (weight = 1, others = 0) and submit. If both the blended and solo scores are worse than the prior best, discard the new model. This two-step probe (blend then isolate) distinguishes whether the model is weak 
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.69417 → 0.68425 (-0.00992)
- expert 77347591 (Expert) · equity · v20→v22   Apply the subset adjustment as a direct additive offset to the final blended prediction rather than manipulating individual model ranks before averaging. This preserves the ensemble's rank structure for unflagged samples while cleanly separating flagged ones. Tune the offset magnitude in small incre
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.69411 → 0.69416 (+0.00005)
- expert 75924487 (Master) · equity · v1→v2   Curate the set of base-model predictions fed to the meta-learner by explicitly listing which columns to keep. Remove models that are redundant or underperforming. Re-submit to verify the gain, since stochastic meta-learner training can cause score variance between identical runs.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.69156 → 0.69159 (+0.00003)
- expert 75924487 (Master) · equity · v6→v8   Run an A/B test: submit once with all base-model outputs and once with a hand-picked subset. Compare leaderboard or validation scores. If the curated subset wins, keep it; weak or redundant members add noise that the meta-learner cannot fully ignore.
    evidence: ✓ A previously better ensemble lost members during a recent change. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.69331 → 0.69347 (+0.00015)
- expert 75924487 (Master) · equity · v10→v12   Add new members incrementally rather than in a single large batch. After each addition, check the validation metric. A large simultaneous expansion of ensemble inputs can introduce correlated or noisy members that degrade the meta-learner, as evidenced by a score drop when many columns are added at 
    evidence: ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.69408 → 0.69305 (-0.00104)
- expert 75145694 (Expert) · equity · v3→v4   Create multiple regression targets from the same survival data using distinct statistical transforms of the censored outcome. Train separate base models on each target variant and blend their predictions. Even small per-model gains compound when the transforms are sufficiently decorrelated.
    evidence: ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.68865 → 0.68888 (+0.00022)
- expert 75145694 (Expert) · equity · v6→v11   Submit after each single, isolated change to the ensemble (one member added or removed, or one weight adjusted) so that the leaderboard delta can be attributed. Before sweeping composition, verify the end-to-end inference pipeline produces correct predictions (e.g., check shapes, fold alignment, and
    evidence: ✓ A previously better ensemble lost members during a recent change. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.69053 → 0.69043 (-0.00010)
- expert 75145694 (Expert) · equity · v14→v16   Ablate by disabling most ensemble members and submitting the reduced blend. If the score drops meaningfully, the removed members are contributing. Test progressively: first keep a small subset, then try a single base model alone. Use the magnitude of the drop to gauge each group's contribution. Rest
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.69067 → 0.68867 (-0.00200)
- expert 75145694 (Expert) · equity · v15→v16   Submit the raw base prediction (rank-transformed) without any blending and compare to the full pipeline score. The gap quantifies the ensemble's marginal value. If the gap is large relative to recent incremental gains, the blending infrastructure is essential and should be kept and expanded rather t
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.69041 → 0.68867 (-0.00174)
- expert 75145694 (Expert) · equity · v19→v22   Toggle the member on and off at least twice while keeping everything else fixed. If the score change is consistent in sign across toggles, the effect is likely real. If the magnitude is tiny and inconsistent, the member is near-neutral and can be dropped for simplicity. Avoid changing multiple membe
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.68978 → 0.68958 (-0.00020)
- expert 75145694 (Expert) · equity · v32→v33   Implement a pairwise ranking loss (optionally with focal weighting to emphasize hard pairs) for a tabular neural network with categorical embeddings. Add it as a new ensemble member. Expect a small but positive marginal gain from the loss-metric alignment, mainly through diversity in the blend.
    evidence: ✓ A candidate has nonredundant errors and plausible standalone quality.
    leaderboard score 0.69285 → 0.69296 (+0.00010)
- expert 75145694 (Expert) · equity · v56→v57   Include the new model's binary classification output in the aggregation that drives the discrete post-processing rule. This adds diversity to the binary vote without changing blend weights, and can recover small score losses from weight-only tuning.
    evidence: ✓ A candidate has nonredundant errors and plausible standalone quality.
    leaderboard score 0.69307 → 0.69317 (+0.00010)
- expert 75145694 (Expert) · equity · v60→v62   Separate the change into two commits: first rebalance existing weights to a clean baseline, then add the new member with a small initial weight. Submit only after the second step so the incremental effect of the new model is observable. This isolates the contribution and reduces risk of regression.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.69325 → 0.69354 (+0.00029)
- expert 77276039 (Expert) · equity · v13→v17   Toggle the candidate member in and out of the ensemble and submit both versions. Compare scores directly: if including the new member lowers the metric, drop it. This A/B probe requires only two submissions and gives a clear signal for inclusion decisions.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score n/a → 0.69244
- expert 77276039 (Expert) · equity · v22→v24   Add or remove one member at a time from the rank-average ensemble and evaluate after each change. Keep the member set that maximizes the target metric. When local validation is unavailable, use leaderboard feedback sparingly, changing only one member per submission.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.69028 → 0.69188 (+0.00159)
- expert 73937748 (Master) · equity · v12→v13   Try disabling standard scaling of numeric features when the pipeline uses only tree-based models. If the score stays the same or improves, remove scaling permanently to simplify the pipeline.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.68793 → 0.68805 (+0.00012)
- expert 73937748 (Master) · equity · v22→v25   Add candidate models one at a time and check the validation/leaderboard score after each addition. If the score drops despite weight re-optimization, the new member is likely redundant or noisy. Prefer a smaller, curated ensemble of individually strong and diverse models over a large pool of all ava
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ A candidate has nonredundant errors and plausible standalone quality.
    leaderboard score 0.69000 → 0.68721 (-0.00278)
- expert 73937748 (Master) · equity · v59→v60   Run the same model architecture on two or more distinct input representations (e.g., raw features vs. engineered features) and treat each run's out-of-fold predictions as a separate ensemble member. Feed all variants into the meta-learner so it can exploit the complementary information.
    evidence: ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score n/a → 0.69283
- expert 53747598 (Master) · hms · v12→v15   Before adding new diverse models, prune or disable ensemble members that are suspected to hurt or not help (e.g., models using only a subset of available inputs). This reduces noise in the blend baseline and makes it easier to attribute gains to the newly added components.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.23270 → 0.22838 (-0.00432)
- expert 53747598 (Master) · hms · v25→v30   Add the new checkpoints to the ensemble, then iteratively tune blend weights in small increments around the current best ratio. After each weight change, evaluate on the leaderboard or a reliable validation set. Prefer near-equal weighting as a starting point and shift weight toward the component th
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A candidate has nonredundant errors and plausible standalone quality.
    leaderboard score 0.22688 → 0.22587 (-0.00101)
- expert 53424936 (Master) · hms · v22→v23   Perform leave-one-out ablation: remove one ensemble member at a time, adjust the averaging denominator, and submit. If the score improves, permanently exclude that member. This identifies members that add noise or are miscalibrated relative to the rest of the blend.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.22735 → 0.22645 (-0.00090)
- expert 53424936 (Master) · hms · v23→v24   Evaluate the ensemble with and without the candidate on the leaderboard or a reliable validation set. If inclusion does not improve the metric, the candidate likely overlaps too much with existing members. Prioritize members that differ in training data views, architecture family, or loss function r
    evidence: ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.22645 → 0.22647 (+0.00002)
- expert 53424936 (Master) · hms · v32→v33   Remove the suspected weak or redundant member, adjust the denominator accordingly, and submit. If the score improves, keep it removed. Iterate by trying removal of each member one at a time to identify which ones hurt the blend.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.22615 → 0.22600 (-0.00015)
- expert 50376011 (Grandmaster) · hms · v8→v11   Try adding one candidate at a time to the existing ensemble and evaluate on the leaderboard or a held-out set. If every addition degrades the score, keep the original set. Adding weaker or redundant members to a simple average dilutes the ensemble and can hurt performance, so do not assume more memb
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.40047 → 0.40647 (+0.00600)
- expert 50376011 (Grandmaster) · hms · v8→v11   Test the candidate in at least two different ensemble compositions. If it consistently fails to improve (or worsens) the metric across compositions, discard it. A single negative result could be coincidence, but consistent degradation across contexts confirms the candidate is not complementary.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.40047 → 0.40647 (+0.00600)
- expert 50376011 (Grandmaster) · hms · v11→v16   Evaluate individual members in isolation to gauge their standalone quality, then compare against the full ensemble. If the full ensemble beats every individual member, keep it. If adding a weak member hurts, remove it. Use the gap between single-member and ensemble scores to judge ensemble benefit a
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score 0.40647 → 0.46668 (+0.06021)
- expert 50376011 (Grandmaster) · hms · v22→v26   Test subsets of available checkpoints separately before combining them. Start with the known-best subset, try adding new members, and compare. If the expanded ensemble scores worse, revert to the smaller set. Prefer a compact ensemble of consistently strong members over a larger one that includes we
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.39939 → 0.39657 (-0.00282)
- expert 50376011 (Grandmaster) · hms · v27→v31   Sweep one group at a time with uniform weights, submitting each to the leaderboard. Compare scores across groups to identify the best-performing subset before attempting to combine groups or tune weights.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score n/a → 0.39254
- expert 50376011 (Grandmaster) · hms · v58→v59   Track each checkpoint's leaderboard score across submissions. Pick two or more checkpoints that each score well individually but were trained under different conditions (different fold splits, training runs, or hyperparameters) to maximize diversity. Start with equal-weight averaging and submit to c
    evidence: ✓ A candidate has nonredundant errors and plausible standalone quality. | ✗ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.36034 → 0.34053 (-0.01982)
- expert 50376011 (Grandmaster) · hms · v68→v70   Systematically expand the ensemble by adding more diverse checkpoints. First verify the single-model baseline to confirm the ensemble is actually helping, then add members incrementally. Use equal weights unless there is evidence for differential quality. Reduce per-model batch size if memory is tig
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.32583 → 0.32116 (-0.00468)
- expert 50376011 (Grandmaster) · hms · v70→v74   Run each ensemble member individually and compare its score to the full ensemble. If every single member scores worse, the ensemble diversity is genuinely helping. If one member matches or beats the ensemble, simplify to that member and investigate why others hurt.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.32116 → 0.32513 (+0.00397)
- expert 50376011 (Grandmaster) · hms · v94→v97   Avoid spending many submissions testing individual ensemble members after the ensemble is already validated. Instead, use held-out validation to assess member quality offline. If leaderboard submissions are limited or noisy, keep the best ensemble as the baseline and only test modifications that add
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.31316 → 0.33459 (+0.02142)
- expert 50376011 (Grandmaster) · hms · v110→v121   Test single-model, two-model, and larger ensembles (e.g., 4–5 members) on the leaderboard or validation set. If two members show inconsistent improvement over one, scale up to more members before concluding that ensembling helps. Keep the multi-model configuration code ready so scaling up is a one-l
    evidence: ✓ A previously better ensemble lost members during a recent change. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score 0.29444 → 0.28921 (-0.00524)
- expert 50376011 (Grandmaster) · hms · v122→v123   Progressively increase the number of ensemble members with equal blending weights. When prior experiments show monotonic improvement from 1→2→4 members, try the full set of available checkpoints. Use uniform weights as a strong default unless there is evidence that some members are weaker.
    evidence: ✓ A candidate has nonredundant errors and plausible standalone quality. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.28870 → 0.27696 (-0.01174)
- expert 50376011 (Grandmaster) · hms · v169→v170   Search incrementally: start from the best small ensemble, add one member at a time, and submit. Also try removing each existing member. Keep the configuration that yields the best test metric. Stop expanding when adding any available new member no longer improves the score.
    evidence: ✓ A candidate has nonredundant errors and plausible standalone quality. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.25069 → 0.24948 (-0.00121)
- expert 50376011 (Grandmaster) · hms · v170→v174   Sweep ensemble composition by adding or removing one member at a time and submitting each variant. Start from the current best subset, try the full set, then systematically drop each member to identify which ones hurt. Keep the subset that scores best.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score 0.24948 → 0.24842 (-0.00106)
- expert 50376011 (Grandmaster) · hms · v171→v174   After trying the full set of checkpoints, remove each member one at a time and compare scores. If dropping a member improves the ensemble, leave it out. Prefer a smaller, higher-quality subset over the full set.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score 0.25445 → 0.24842 (-0.00603)
- expert 50376011 (Grandmaster) · hms · v228→v229   Temporarily replace the ensemble with a single member and submit. Compare the single-member score to the ensemble score. If the gap is large (here ~0.08 on a 0.23 baseline), the ensemble is clearly beneficial and should be kept or expanded.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.23565 → 0.31671 (+0.08106)
- expert 49524919 (Grandmaster) · hms · v76→v84   First evaluate each candidate backbone individually to confirm it produces reasonable predictions. Then include all viable backbones simultaneously with equal blend weights. Adding more diverse architectures tends to reduce variance and improve the ensemble even when no single new backbone beats the
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score 0.27414 → 0.26879 (-0.00535)
- expert 49524919 (Grandmaster) · hms · v85→v88   Submit each model's predictions individually to the leaderboard to rank their standalone quality. Use these rankings to decide inclusion and to set blend weights proportional to individual performance, then verify the full blend still beats the best single model before finalizing.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score 0.27935 → 0.26916 (-0.01019)
- expert 49524919 (Grandmaster) · hms · v113→v120   Use conditional skip flags to first evaluate each new model in isolation on the leaderboard, then enable all models together and submit the blend. Compare standalone scores against the blended score to confirm diversity benefit before permanently including them. Remove models whose standalone perfor
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.27048 → 0.24466 (-0.02581)
- expert 49524919 (Grandmaster) · hms · v133→v134   Completely disable the suspect model family (remove its predictions from the blend) while ensuring all other intended models run correctly. Compare the resulting score to the best achieved with the family included. If the score improves, permanently remove that family and clean up its code.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.25459 → 0.24021 (-0.01438)
- expert 49524919 (Grandmaster) · hms · v128→v134   First, test each model group in isolation by skipping all others and submitting its solo predictions to establish per-group quality. Fix any column-reference or control-flow bugs before blending. Then enable all groups that individually score well, blend them, and submit. After each change, verify t
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score n/a → 0.24021
- expert 49524919 (Grandmaster) · hms · v134→v136   First, delete all dead code for the removed model family to reduce complexity and runtime. Then systematically try different epoch checkpoints for each fold of the remaining models, submitting to see if a different combination yields a small score improvement. Expect only marginal gains (on the orde
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.24021 → 0.24011 (-0.00010)
- expert 49524919 (Grandmaster) · hms · v134→v135   Use a two-phase approach: first disable the component and submit to confirm the improvement on the leaderboard, then in a follow-up commit fully remove the dead code. This preserves the option to revert if the improvement was spurious, while eventually reducing complexity and runtime.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.24021 → n/a
- expert 49524919 (Grandmaster) · hms · v146→v148   Remove the weaker component entirely from the ensemble rather than trying to down-weight it. Even small blend weights on a substantially worse model can hurt, and removing dead code paths may also eliminate subtle side effects on shared data structures or preprocessing.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.27167 → 0.23482 (-0.03685)
- expert 49524919 (Grandmaster) · hms · v148→v158   Isolate each model group by disabling all others, submit to get its standalone score, and swap checkpoint files within each group to find the best variant. Once the best checkpoint per group is identified, re-enable all groups and submit the full blend. This confirms each component's contribution an
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score 0.23482 → 0.23032 (-0.00450)
- expert 49524919 (Grandmaster) · hms · v158→v162   Systematically submit each model group in isolation, record its standalone score, then submit the full blend. If the blend beats every individual member, keep it; if a member scores worse than the blend margin, consider dropping it. This ablation should be repeated whenever checkpoints or members ch
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score 0.23032 → 0.22875 (-0.00157)
- expert 52860091 (Grandmaster) · hms · v22→v23   If down-weighting the weaker model still cannot match the single-model baseline, remove it entirely. To regain ensemble diversity, introduce a model from a different architecture family rather than another checkpoint or variant of the same family, because uncorrelated errors are what make ensembles 
    evidence: ✓ One member is consistently weak and a compatible replacement is available. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.27950 → 0.27421 (-0.00530)
- expert 52860091 (Grandmaster) · hms · v40→v43   Submit the new model's predictions alone (weight 1.0) to establish its standalone leaderboard score. Compare this to the existing blend's score. If the standalone score is within a reasonable margin, the model likely adds diversity and should be blended at a low weight. If it is much worse, consider
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ One member is consistently weak and a compatible replacement is available. | ✓ A candidate has nonredundant errors and plausible standalone quality.
    leaderboard score 0.25799 → 0.25606 (-0.00193)
- expert 52551258 (Expert) · hms · v7→v9   Test the complex variant on the leaderboard. If it scores worse, revert promptly. Do not assume added complexity helps; treat it as a probe and keep the simpler model as the default unless the complex one clearly wins.
    evidence: ✓ A previously better ensemble lost members during a recent change. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.32513 → 0.36957 (+0.04445)
- expert 52551258 (Expert) · hms · v11→v13   Evaluate the new checkpoint both in isolation and within the full ensemble. If the isolated score is worse than the ensemble, the diversity contribution of the other family is confirmed. Always restore the full ensemble after testing a component swap, and only drop a family if the ensemble without i
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.30250 → 0.30219 (-0.00031)
- expert 52551258 (Expert) · hms · v16→v17   Test the new model in isolation first, disabling all other ensemble members. If it already beats the full ensemble, use it as the new baseline and build future ensembles around it. A stronger single model often outperforms an ensemble of weaker ones.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.31128 → 0.28185 (-0.02943)
- expert 53762022 (Contributor) · hms · v1→v4   Add the candidate member, submit or validate, and compare the metric to the baseline ensemble. If the score worsens, remove the member rather than trying to down-weight it; a weak or redundant member can hurt even at low weight, and removing it is the cleanest fix.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.29936 → 0.30010 (+0.00074)
- expert 53762022 (Contributor) · hms · v7→v8   Submit each component model's predictions individually to measure its standalone quality. If a single component scores much worse than the blend, the ensemble is providing significant value and the regression likely comes from the modified component. Use this diagnostic to decide which component to 
    evidence: ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.40866 → 0.68408 (+0.27542)
- expert 53762022 (Contributor) · hms · v7→v8   Submit the single best component's raw predictions as an ablation. Compare the gap to the blended score. If the gap is large (e.g., error more than doubles), the ensemble synergy is critical and effort should go into maintaining or improving the blend rather than relying on any single model.
    evidence: ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.40866 → 0.68408 (+0.27542)
- expert 53762022 (Contributor) · hms · v8→v9   Submit each ensemble member's predictions individually to the leaderboard (or evaluate on a held-out fold). If a component scores far below the ensemble, prioritize improving that component's pipeline (features, preprocessing, validation) rather than continuing to tune blend coefficients.
    evidence: ✓ One member is consistently weak and a compatible replacement is available. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.68408 → 0.36230 (-0.32178)
- expert 52200959 (Master) · hms · v8→v11   Submit each component model individually to the leaderboard (or evaluate on a held-out fold) to rank them by standalone performance. Use this ranking to inform ensemble weighting or pruning: the weakest standalone models may still help via diversity, but knowing the ranking guides which combinations
    evidence: ✓ A previously better ensemble lost members during a recent change. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.34134 → 0.41926 (+0.07792)
- expert 52200959 (Master) · hms · v8→v11   Evaluate each component in isolation and compare against the ensemble score. If the ensemble substantially outperforms even the best single component, all members likely contribute through diversity. If the gap is small, consider simplifying to fewer components and reallocating effort to improving t
    evidence: ✓ A previously better ensemble lost members during a recent change. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.34134 → 0.41926 (+0.07792)
- expert 60264017 (Master) · learning · v8→v12   Use greedy forward/backward selection on the leaderboard or a reliable validation set: add or remove one member per iteration, re-optimize blend weights each time, and submit. Keep the change only if the metric improves. Prefer a smaller ensemble when a larger one shows no gain, as fewer members red
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ A candidate has nonredundant errors and plausible standalone quality. | ✓ One member is consistently weak and a compatible replacement is available.
    leaderboard score n/a → 0.82997
- expert 60264017 (Master) · learning · v12→v13   Prune multiple members at once and submit to measure the impact. If the score drops, the removed members collectively contributed positively; restore them and instead try removing one at a time to isolate truly redundant members. Aggressive bulk pruning risks conflating individual member effects.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.82997 → 0.82848 (-0.00149)
- expert 55621328 (Master) · learning · v48→v49   Add extra checkpoints incrementally and check the metric. If the base model is already overfitting (evidenced by underperforming a smaller model), adding more checkpoints from the same training regime is unlikely to help and may dilute signal. Focus instead on improving the individual model quality 
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.80865 → 0.80701 (-0.00164)
- expert 55621328 (Master) · learning · v80→v81   Test a single-checkpoint variant against the full ensemble. If the score drops, keep the multi-checkpoint ensemble; the diversity from multiple folds or seeds is contributing meaningfully to prediction quality.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.82504 → 0.82051 (-0.00453)
- expert 55431616 (Grandmaster) · learning · v11→v13   Strip the ensemble back to the single stronger model, simplify infrastructure, and simultaneously improve the cross-validation scheme (use stratified folds for imbalanced/ordinal targets) and align the training objective with the evaluation metric. Evaluate the cleaner pipeline before re-adding comp
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.81502 → 0.81762 (+0.00261)
- expert 58130512 (Master) · learning · v42→v43   Remove one backbone at a time and re-evaluate on the leaderboard or a reliable validation set. If the score drops, restore that backbone. Ensure the feature-selection step and embedding dimensionality are updated consistently when a backbone is removed. A score drop confirms the removed model was co
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.82268 → 0.81956 (-0.00313)
- expert 60197293 (Expert) · learning · v28→v35   Ablate the ensemble by disabling one member entirely and submitting the single-model pipeline. If the score barely changes, drop the weaker member to reduce complexity and free capacity for other improvements. A difference smaller than typical leaderboard noise (a few ten-thousandths) means the remo
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.81799 → 0.81788 (-0.00011)
- expert 55987255 (Master) · learning · v50→v56   Progressively reduce the weaker model's blend weight toward zero across several runs while monitoring the validation metric. If performance improves or stays flat as the weight decreases, the secondary model is adding noise rather than diversity; remove it entirely to simplify the pipeline and reduc
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score n/a → n/a
- expert 55987255 (Master) · learning · v56→v57   Before tuning an ensemble further, verify that each component's predictions are actually being used correctly. Simplify the pipeline to the minimal working version (single model, no wrapper) and confirm the score. Only re-add complexity once the baseline is verified bug-free.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score n/a → 0.82112
- expert 55987255 (Master) · learning · v56→v57   Test the single best model alone as a baseline before blending. If the single model scores higher than the ensemble, inspect the ensemble code and weaker members for bugs or detrimental contributions before re-introducing them.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score n/a → 0.82112
- expert 55987255 (Master) · learning · v89→v92   After observing that expanding the model list hurts, prune back to fewer, higher-quality backbones and replace expensive extracted features with lightweight dimensionality-reduced representations (e.g., latent factors from matrix decomposition). Verify the recovery on the leaderboard before adding c
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score n/a → 0.81822
- expert 13702907 (Contributor) · ranzcr · v3→v4   Before committing to an ensemble, test each constituent model individually on the leaderboard or validation set. If one model dominates, submit it alone. Only ensemble models whose individual scores are close to or above the current best; drop any that pull the average down.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✗ A previously better ensemble lost members during a recent change.
    leaderboard score 0.94606 → 0.94772 (+0.00167)
- expert 50496431 (Grandmaster) · hms · v22→v23   When ablating an ensemble member, treat it as a single-variable experiment: remove only that member, submit, and immediately compare. If the score worsens, restore the member before making any other changes. Never stack an ablation with other modifications (e.g., preprocessing tuning), because the d
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.33898 → 0.39115 (+0.05217)
- expert 50496431 (Grandmaster) · hms · v44→v45   Enable or disable one model branch at a time and submit to the leaderboard (or evaluate on validation) to isolate its marginal contribution. Keep the branch enabled only if the score improves.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost.
    leaderboard score 0.37087 → 0.35027 (-0.02061)
- expert 50496431 (Grandmaster) · hms · v72→v75   Ablate ensemble members one at a time by toggling each on/off and submitting. Compare scores to the full-ensemble baseline. Remove any member whose exclusion improves the score. Do this iteratively, re-checking after each removal, because interactions between members can shift.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score n/a → 0.27839
- expert 50496431 (Grandmaster) · hms · v80→v81   After modifying any single ensemble member, re-test inclusion/exclusion of every other member one at a time. Do not assume a previously helpful member is now unnecessary just because another member was upgraded; architecturally diverse models (e.g., 2D vs 3D backbones) often remain complementary.
    evidence: ✗ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.29794 → 0.27445 (-0.02349)
- expert 50496431 (Grandmaster) · hms · v88→v92   First disable the new model and restore the previous best ensemble to confirm the baseline. Then test the new model alongside other members using weighted blending rather than uniform averaging, giving it lower weight initially. If the ensemble still degrades, exclude it. If it helps with reduced we
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change. | ✓ A candidate has nonredundant errors and plausible standalone quality.
    leaderboard score 0.28657 → 0.27226 (-0.01432)
- expert 50496431 (Grandmaster) · hms · v104→v106   Remove the member in a controlled submission where no other change is made (or where other changes are subsequently reverted). If the score worsens, the member is contributing positively and should be kept. Avoid confounding the removal with other simultaneous changes.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.27115 → 0.28677 (+0.01561)
- expert 50496431 (Grandmaster) · hms · v137→v138   Toggle one member at a time (swap in the alternative, swap out the current best contributor) and submit. If the score degrades, keep the original member. Do not change multiple factors simultaneously when testing a single member's contribution, or the signal is confounded.
    evidence: ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.25172 → 0.25541 (+0.00370)
- expert 50496431 (Grandmaster) · hms · v161→v163   Revert to the proven ensemble composition that excludes the new model. Keep the new model code available for future tuning but do not force it into the blend. Gains often come from re-tuning preprocessing or other parameters alongside the established members rather than from the new architecture its
    evidence: ✓ One member is consistently weak and a compatible replacement is available. | ✓ A member is redundant, harmful in prior blends, or contributes little relative to its inference cost. | ✓ A previously better ensemble lost members during a recent change.
    leaderboard score 0.26705 → 0.22940 (-0.03765)
# Reweight observed examples  `T.3.1.2`   7 edits, 0 experts
6 scored cases, median improvement -0.00003, 2 improved


- expert 27389424 (Grandmaster) · amex · v10→v25   First sweep the minority-class weight exponentially upward (e.g., 1, 2, 5, 10, 25, 50, 100) to find where performance peaks and degrades. Then reverse direction and sweep below 1.0 (e.g., 0.8, 0.5, 0.25, 0.1, 0.04, 0.01) to check whether down-weighting the minority class helps. Use a fast local vali
    evidence: ✓ Rare classes or relevant subgroups contribute too little to the current objective.
    leaderboard score n/a → n/a
- expert 27502740 (Grandmaster) · amex · v2→v5   Try adding sample weights that inflate the majority class relative to the minority class. Compare the leaderboard score to the unweighted baseline. If the score does not improve (or slightly degrades), revert the weights—ranking-based metrics are often invariant to or harmed by class reweighting bec
    evidence: ✓ Rare classes or relevant subgroups contribute too little to the current objective. | ✓ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.79421 → 0.79418 (-0.00003)
- expert 27656049 (Expert) · amex · v23→v26   Sweep the exponent applied to the negative-to-positive ratio (e.g., 1/4, 1/3, 1/2, 1) to set the class weight. Submit or validate each, and pick the exponent that maximizes the target metric. Moderate exponents (e.g., cube root) often outperform both the raw ratio and near-unity weights.
    evidence: ✓ Rare classes or relevant subgroups contribute too little to the current objective.
    leaderboard score 0.79224 → 0.79258 (+0.00034)
- expert 58130512 (Master) · learning · v29→v32   Oversample (duplicate) the subpopulation that matches the test distribution before fitting the unsupervised feature extractor, so its vocabulary and term weights better reflect test-time text. Keep the supervised labels and folds unchanged; only the representation-fitting corpus is rebalanced.
    evidence: ✓ A minority subgroup matches the expected test population and is currently underrepresented. | ✗ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.82105 → 0.82190 (+0.00085)
- expert 58130512 (Master) · learning · v32→v34   Submit variants that oversample each candidate subgroup separately and compare leaderboard scores. If one selection degrades performance, revert to the other. A single-variable change per submission isolates the effect of the subgroup choice.
    evidence: ✓ A minority subgroup matches the expected test population and is currently underrepresented. | ✓ Low-confidence labels, duplicates, or a mismatched source subset can be identified. | ✓ A prior augmentation trial degraded validation without improving minority-group errors.
    leaderboard score 0.82190 → 0.82015 (-0.00175)
- expert 60197293 (Expert) · learning · v93→v94   Test contraction expansion and a large class-weight parameter together. If the score drops, revert: rank-correlation metrics like quadratic weighted kappa are not directly improved by class rebalancing, and aggressive positive-class weighting can distort predicted values in a regression setup. Probe
    evidence: ✓ Rare classes or relevant subgroups contribute too little to the current objective.
    leaderboard score 0.81872 → 0.81836 (-0.00035)
- expert 60197293 (Expert) · learning · v93→v94   Avoid using binary-classification class-weighting parameters (e.g., positive-class weight) in a regression setup; they are ignored or misapplied and can degrade predictions. Instead, address ordinal imbalance through sample weights proportional to inverse class frequency, stratified cross-validation
    evidence: ✓ Rare classes or relevant subgroups contribute too little to the current objective.
    leaderboard score 0.81872 → 0.81836 (-0.00035)
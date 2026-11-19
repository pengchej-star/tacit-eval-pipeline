# Average independent training seeds  `T.5.1.5`   11 edits, 0 experts
8 scored cases, median improvement +0.00027, 4 improved


- expert 27799930 (Contributor) · amex · v55→v63   Train the full CV loop multiple times with different random seeds and average all resulting predictions. Start with 2–3 seeds; compare leaderboard scores. If a smaller number of seeds scores as well or better (due to less overfitting to noise or compute constraints), prefer fewer seeds.
    evidence: ✓ Independent training seeds produce materially different errors on the same examples. | ✗ Compatible unused fold checkpoints exist or fold quality varies substantially.
    leaderboard score 0.79342 → 0.79472 (+0.00130)
- expert 27799930 (Contributor) · amex · v69→v71   Probe by toggling between fewer and more seeds (e.g., 1 vs 2 vs 3) and comparing validation scores. If removing a seed hurts validation, keep it; if adding one doesn't help or hurts (due to a weaker seed), remove it. Two to three seeds is often a practical sweet spot for tree-based models.
    evidence: ✓ A member or group has weak or redundant marginal contribution in earlier ablations. | ✗ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.79475 → n/a
- expert 27799930 (Contributor) · amex · v73→v74   Treat the number of folds and seeds as low-cost hyperparameters to search over. Increase one at a time, verify on the leaderboard or a stable local metric, and keep the configuration that improves the score. If adding a seed or fold does not help, revert. Avoid assuming more is always better.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score n/a → n/a
- expert 18350823 (Expert) · commonlitreadabilityprize · v5→v8   Test by doubling the number of averaged inference runs with varied seeds. If the score does not change after one doubling, further increases are unlikely to help because the model's forward pass is effectively deterministic. Move on to other levers such as changing blend weights, adding distinct mod
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.46275 → 0.46275 (+0.00000)
- expert 18350823 (Expert) · commonlitreadabilityprize · v26→v27   Disable all stochastic layers (dropout, droppath) during inference so each forward pass is deterministic, and increase the number of random-seed replicates being averaged. These changes reduce prediction variance and can yield a larger improvement than weight tuning alone.
    evidence: ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.46069 → 0.45945 (-0.00124)
- expert 18350823 (Expert) · commonlitreadabilityprize · v28→v29   Add the new seed checkpoints to the averaging pool and evaluate. If the score does not improve, the new checkpoints may be weaker or trained under different conditions; in that case, either remove them or down-weight them rather than giving equal weight to all seeds.
    evidence: ✗ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.45904 → 0.45931 (+0.00027)
- expert 18757376 (Expert) · commonlitreadabilityprize · v7→v8   Gradually increase the number of seeds averaged (e.g., from 3 to 7) and monitor local CV. Stop increasing when the CV improvement plateaus or when diminishing returns are visible. Ensure the aggregation code is correct before drawing conclusions about the effect of more seeds.
    evidence: ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score n/a → n/a
- expert 17371717 (Master) · commonlitreadabilityprize · v7→v8   Train the same model multiple times with different random seeds, save all checkpoints, and average predictions across seeds within each fold at inference time. This multi-seed ensemble smooths out seed-dependent noise without requiring different architectures.
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.47432 → 0.47270 (-0.00162)
- expert 17371717 (Master) · commonlitreadabilityprize · v14→v16   Ablate by submitting individual seed checkpoints one at a time and comparing each to the ensemble score. If every single seed scores worse than the ensemble, keep the ensemble. If one seed consistently matches or beats it, the ensemble may be adding noise from weaker seeds. On a tiny leaderboard, pr
    evidence: ✓ The full blend has never been compared with its strongest member under the same evaluation. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.46639 → 0.46838 (+0.00199)
- expert 17371717 (Master) · commonlitreadabilityprize · v20→v21   For each fold, load checkpoints from several training runs that differ only in random seed. Run inference with each, average their predictions per fold, then average across folds. Expect diminishing but consistent gains (often a few hundredths of RMSE on small test sets). Increase batch size to offs
    evidence: ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.46543 → 0.46533 (-0.00010)
- expert 55621328 (Master) · learning · v45→v46   Append the different-seed checkpoints to the prediction-averaging ensemble. Because seed variation is partially orthogonal to fold variation, the averaged predictions are more stable and the metric typically improves modestly.
    evidence: ✓ Compatible unused fold checkpoints exist or fold quality varies substantially. | ✓ Independent training seeds produce materially different errors on the same examples.
    leaderboard score 0.81599 → 0.81880 (+0.00281)
# Average independent training runs  `T.7.3.3`   17 edits, 0 experts
10 scored cases, median improvement +0.00027, 5 improved


- expert 27799930 (Contributor) · amex · v55→v63   Train the full CV loop multiple times with different random seeds and average all resulting predictions. Start with 2–3 seeds; compare leaderboard scores. If a smaller number of seeds scores as well or better (due to less overfitting to noise or compute constraints), prefer fewer seeds.
    evidence: ✗ The model has usable stochastic layers and repeated inference is intended to sample them. | ✗ Stochastic layers are active at inference without a validated repeated-pass strategy.
    leaderboard score 0.79342 → 0.79472 (+0.00130)
- expert 27799930 (Contributor) · amex · v69→v71   Probe by toggling between fewer and more seeds (e.g., 1 vs 2 vs 3) and comparing validation scores. If removing a seed hurts validation, keep it; if adding one doesn't help or hurts (due to a weaker seed), remove it. Two to three seeds is often a practical sweet spot for tree-based models.
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ The model has usable stochastic layers and repeated inference is intended to sample them. | ✗ Stochastic layers are active at inference without a validated repeated-pass strategy.
    leaderboard score 0.79475 → n/a
- expert 18350823 (Expert) · commonlitreadabilityprize · v28→v29   Add the new seed checkpoints to the averaging pool and evaluate. If the score does not improve, the new checkpoints may be weaker or trained under different conditions; in that case, either remove them or down-weight them rather than giving equal weight to all seeds.
    evidence: ✓ Independent training seeds produce materially different errors. | ✓ Several compatible training snapshots of one model are available for weight averaging.
    leaderboard score 0.45904 → 0.45931 (+0.00027)
- expert 18757376 (Expert) · commonlitreadabilityprize · v7→v8   Gradually increase the number of seeds averaged (e.g., from 3 to 7) and monitor local CV. Stop increasing when the CV improvement plateaus or when diminishing returns are visible. Ensure the aggregation code is correct before drawing conclusions about the effect of more seeds.
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score n/a → n/a
- expert 17371717 (Master) · commonlitreadabilityprize · v7→v8   Train the same model multiple times with different random seeds, save all checkpoints, and average predictions across seeds within each fold at inference time. This multi-seed ensemble smooths out seed-dependent noise without requiring different architectures.
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score 0.47432 → 0.47270 (-0.00162)
- expert 17371717 (Master) · commonlitreadabilityprize · v12→v14   Test single-checkpoint-per-fold first as a baseline, then add per-seed averaging (load all seed-specific checkpoints for each fold, average their predictions, then average across folds). Compare leaderboard scores to confirm that multi-seed averaging helps. Pair with newer/better-trained checkpoints
    evidence: ✓ Independent training seeds produce materially different errors. | ✓ Several compatible training snapshots of one model are available for weight averaging.
    leaderboard score 0.47587 → 0.46639 (-0.00948)
- expert 17371717 (Master) · commonlitreadabilityprize · v14→v16   Ablate by submitting individual seed checkpoints one at a time and comparing each to the ensemble score. If every single seed scores worse than the ensemble, keep the ensemble. If one seed consistently matches or beats it, the ensemble may be adding noise from weaker seeds. On a tiny leaderboard, pr
    evidence: ✓ Independent training seeds produce materially different errors. | ✓ Several compatible training snapshots of one model are available for weight averaging.
    leaderboard score 0.46639 → 0.46838 (+0.00199)
- expert 17371717 (Master) · commonlitreadabilityprize · v20→v21   For each fold, load checkpoints from several training runs that differ only in random seed. Run inference with each, average their predictions per fold, then average across folds. Expect diminishing but consistent gains (often a few hundredths of RMSE on small test sets). Increase batch size to offs
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score 0.46543 → 0.46533 (-0.00010)
- expert 17371717 (Master) · commonlitreadabilityprize · v10→v12   Do not assume ensembling gains transfer across model configurations. When a fundamental change (architecture, head design) is made, first evaluate the single-model baseline, then add ensembling. If the single-model score is already worse than the prior best, ensembling on top is unlikely to close th
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score 0.47528 → 0.47587 (+0.00059)
- expert 77129691 (Master) · equity · v2→v3   Increase the number of ensemble members or repeated runs. Deterministic seeds make each member reproducible, and adding more distinct-seed members restores the variance-reduction benefit that was partially lost by fixing randomness within each run.
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score 0.69005 → 0.68967 (-0.00038)
- expert 77129691 (Master) · equity · v4→v8   Incrementally increase the number of seeded reruns, submitting after each increase. Track the metric at each step. Stop and revert to the previous count when the score drops for the first time, as the variance-reduction benefit has been exhausted.
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score n/a → 0.69063
- expert 77129691 (Master) · equity · v13→v14   Re-probe the ensemble repeat count after major model changes, but expect that the optimal count may differ. If increasing repeats hurts on the leaderboard (as it did before at high counts), revert promptly rather than continuing to increase. The sweet spot depends on the model mix and may need to be
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score n/a → 0.69390
- expert 77129691 (Master) · equity · v13→v14   Increase repeat count incrementally and monitor the leaderboard. Stop and revert as soon as the score drops. After adding a new diverse model to the ensemble, reset the repeat count to a lower baseline because the cross-model diversity already reduces variance, making additional same-model repeats l
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score n/a → 0.69390
- expert 77129691 (Master) · equity · v19→v20   Try a small increment in the repeat count. If the score does not improve (or slightly regresses), revert and invest effort in other levers such as architecture, optimizer, or loss changes instead of further repeat increases. Treat repeat-count tuning as a quick probe, not a reliable source of contin
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score 0.69540 → 0.69534 (-0.00006)
- expert 77129691 (Master) · equity · v23→v25   Re-sweep the repeat count in both directions around the previous best (one step up, one step down). If neither direction improves the score, keep the previous value and move on to other levers rather than continuing to sweep further.
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score 0.69602 → n/a
- expert 60264017 (Master) · learning · v13→v14   Build an inference routine that loads every available checkpoint, runs each on the test data, and averages their outputs. Optionally fit a scaler (e.g., min-max) on out-of-fold predictions to align the averaged output's range with the target distribution before feeding it into the downstream ensembl
    evidence: ✓ Independent training seeds produce materially different errors. | ✓ Several compatible training snapshots of one model are available for weight averaging.
    leaderboard score 0.82848 → n/a
- expert 55621328 (Master) · learning · v45→v46   Append the different-seed checkpoints to the prediction-averaging ensemble. Because seed variation is partially orthogonal to fold variation, the averaged predictions are more stable and the metric typically improves modestly.
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score 0.81599 → 0.81880 (+0.00281)
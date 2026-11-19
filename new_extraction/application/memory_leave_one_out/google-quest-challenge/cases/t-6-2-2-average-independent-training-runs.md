# Average independent training runs  `T.6.2.2`   22 edits, 0 experts
12 scored cases, median improvement -0.00010, 4 improved


- expert 27799930 (Contributor) · amex · v55→v63   Train the full CV loop multiple times with different random seeds and average all resulting predictions. Start with 2–3 seeds; compare leaderboard scores. If a smaller number of seeds scores as well or better (due to less overfitting to noise or compute constraints), prefer fewer seeds.
    evidence: ✗ Available fold checkpoints were trained with incompatible feature layouts. | ✓ Independent training seeds produce materially different errors. | ✗ Dropout or other random inference operations are active or being proposed. | ✓ Repeated forward passes with the same weights and inputs are numerically identical. | ✗ The task has valid input symmetries or multiple aligned views of the same target.
    leaderboard score 0.79342 → 0.79472 (+0.00130)
- expert 27799930 (Contributor) · amex · v69→v71   Probe by toggling between fewer and more seeds (e.g., 1 vs 2 vs 3) and comparing validation scores. If removing a seed hurts validation, keep it; if adding one doesn't help or hurts (due to a weaker seed), remove it. Two to three seeds is often a practical sweet spot for tree-based models.
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.79475 → n/a
- expert 27799930 (Contributor) · amex · v73→v74   Treat the number of folds and seeds as low-cost hyperparameters to search over. Increase one at a time, verify on the leaderboard or a stable local metric, and keep the configuration that improves the score. If adding a seed or fold does not help, revert. Avoid assuming more is always better.
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score n/a → n/a
- expert 17616127 (Contributor) · commonlitreadabilityprize · v9→v10   Test changing the random seed and increasing the maximum token length at inference. Expect minimal impact: seed affects only stochastic elements (e.g., dropout if left on), and longer tokens help only if inputs were being truncated. If the gap to the ensemble persists, return to ensembling rather th
    evidence: ✓ Independent training seeds produce materially different errors. | ✓ Dropout or other random inference operations are active or being proposed. | ✗ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score n/a → 0.48130
- expert 18550705 (Master) · commonlitreadabilityprize · v10→v11   Apply stochastic weight averaging to each constituent model's checkpoints before inference. This smooths the loss landscape and reduces variance of individual model predictions, which can translate to a small ensemble-level improvement.
    evidence: ✓ Independent training seeds produce materially different errors.
    leaderboard score 0.45300 → 0.45284 (-0.00016)
- expert 18350823 (Expert) · commonlitreadabilityprize · v28→v29   Add the new seed checkpoints to the averaging pool and evaluate. If the score does not improve, the new checkpoints may be weaker or trained under different conditions; in that case, either remove them or down-weight them rather than giving equal weight to all seeds.
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Dropout or other random inference operations are active or being proposed. | ✓ Repeated forward passes with the same weights and inputs are numerically identical. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.45904 → 0.45931 (+0.00027)
- expert 18757376 (Expert) · commonlitreadabilityprize · v7→v8   Gradually increase the number of seeds averaged (e.g., from 3 to 7) and monitor local CV. Stop increasing when the CV improvement plateaus or when diminishing returns are visible. Ensure the aggregation code is correct before drawing conclusions about the effect of more seeds.
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score n/a → n/a
- expert 17371717 (Master) · commonlitreadabilityprize · v7→v8   Train the same model multiple times with different random seeds, save all checkpoints, and average predictions across seeds within each fold at inference time. This multi-seed ensemble smooths out seed-dependent noise without requiring different architectures.
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.47432 → 0.47270 (-0.00162)
- expert 17371717 (Master) · commonlitreadabilityprize · v12→v14   Test single-checkpoint-per-fold first as a baseline, then add per-seed averaging (load all seed-specific checkpoints for each fold, average their predictions, then average across folds). Compare leaderboard scores to confirm that multi-seed averaging helps. Pair with newer/better-trained checkpoints
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.47587 → 0.46639 (-0.00948)
- expert 17371717 (Master) · commonlitreadabilityprize · v14→v16   Ablate by submitting individual seed checkpoints one at a time and comparing each to the ensemble score. If every single seed scores worse than the ensemble, keep the ensemble. If one seed consistently matches or beats it, the ensemble may be adding noise from weaker seeds. On a tiny leaderboard, pr
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.46639 → 0.46838 (+0.00199)
- expert 17371717 (Master) · commonlitreadabilityprize · v20→v21   For each fold, load checkpoints from several training runs that differ only in random seed. Run inference with each, average their predictions per fold, then average across folds. Expect diminishing but consistent gains (often a few hundredths of RMSE on small test sets). Increase batch size to offs
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.46543 → 0.46533 (-0.00010)
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
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.69602 → n/a
- expert 50376011 (Grandmaster) · hms · v222→v228   Add checkpoints to the ensemble incrementally, submitting after each addition. Keep adding as long as the metric improves. Verify with single-model ablations that the ensemble is indeed better than any individual member. Continue until all available checkpoints are included or gains plateau.
    evidence: ✓ Independent training seeds produce materially different errors. | ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Available fold checkpoints were trained with incompatible feature layouts. | ✗ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.23868 → 0.23565 (-0.00303)
- expert 50376011 (Grandmaster) · hms · v237→v251   Incrementally add checkpoints to the ensemble, submitting after each addition. When the improvement from adding one more member falls within the noise floor, stop. If runtime is the binding constraint, reduce per-sample processing cost (e.g., smaller batch counts or fewer augmentation passes) to fit
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts. | ✓ Available fold checkpoints differ in quality or some are currently unused. | ✗ Repeated forward passes with the same weights and inputs are numerically identical.
    leaderboard score 0.23496 → n/a
- expert 50376011 (Grandmaster) · hms · v252→v254   Add checkpoints incrementally, submitting after each addition. Track the marginal improvement per added member. Continue adding until the marginal gain becomes negligible or turns negative, then stop at the best count.
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Repeated forward passes with the same weights and inputs are numerically identical. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.22970 → 0.22640 (-0.00331)
- expert 60264017 (Master) · learning · v13→v14   Build an inference routine that loads every available checkpoint, runs each on the test data, and averages their outputs. Optionally fit a scaler (e.g., min-max) on out-of-fold predictions to align the averaged output's range with the target distribution before feeding it into the downstream ensembl
    evidence: ✓ Available fold checkpoints differ in quality or some are currently unused. | ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.82848 → n/a
- expert 55621328 (Master) · learning · v45→v46   Append the different-seed checkpoints to the prediction-averaging ensemble. Because seed variation is partially orthogonal to fold variation, the averaged predictions are more stable and the metric typically improves modestly.
    evidence: ✓ Independent training seeds produce materially different errors. | ✗ Available fold checkpoints were trained with incompatible feature layouts.
    leaderboard score 0.81599 → 0.81880 (+0.00281)
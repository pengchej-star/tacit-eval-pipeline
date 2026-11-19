# Retain raw continuous predictions  `T.6.1.1`   5 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median -0.00742, 0 improved


- expert 6803050 · google · v2→v9   For a purely rank-based metric, submit the raw (unclipped, unscaled) predictions first as a baseline, since monotonic transforms cannot change ranks. Only add clipping or rescaling if the submission format requires bounded values or if post-processing (e.g., rounding to discrete levels) is applied a
    evidence: ✓ The metric depends on order and proposed transformations only erase or perturb useful ordering.
    leaderboard score n/a → n/a (higher is better)
- expert 6803050 · google · v24→v26   Avoid inserting additional normalization between the raw predictions and a quantile/rank-based calibration step, because altering the relative scale can shift values across quantile boundaries and destroy rank order. If tried, verify immediately and revert if the score drops.
    evidence: ✓ The metric depends on order and proposed transformations only erase or perturb useful ordering. | ✓ Target-level frequencies are stable enough that a reference distribution may improve mapping.
    leaderboard score 0.37058 → 0.25892 (higher is better; worse by 0.11166)
- expert 6803050 · google · v26→v27   Remove the unnecessary normalization. Rank-based post-processing (quantile mapping) depends on the ordering of predictions, not their scale, so any rescaling that distorts relative ordering (e.g., adding constants, dividing by a per-fold max) can only hurt. Feed raw averaged outputs directly into th
    evidence: ✓ The metric depends on order and proposed transformations only erase or perturb useful ordering.
    leaderboard score 0.25892 → n/a (higher is better)
- expert 6803050 · google · v35→v39   Avoid adding random noise to predictions when the evaluation metric is rank-based, as it can only degrade signal. Clipping to avoid exact 0/1 is also unnecessary for rank metrics. Use raw model outputs or deterministic post-processing (e.g., quantile mapping) instead.
    evidence: ✓ The metric depends on order and proposed transformations only erase or perturb useful ordering. | ✓ Labels occupy known ordered levels and learned thresholds are not reliably better.
    leaderboard score n/a → 0.38287 (higher is better)
- expert 15173072 · ranzcr · v14→v20   Once the correct order of magnitude for prediction scaling is found (evidenced by a large score jump), further fine-tuning the multiplier yields diminishing or negative returns for a rank-based metric like AUC, because AUC depends on ranking, not absolute values. Lock in the working scale factor and
    evidence: ✓ The metric depends on order and proposed transformations only erase or perturb useful ordering.
    leaderboard score 0.96062 → 0.95319 (higher is better; worse by 0.00742)
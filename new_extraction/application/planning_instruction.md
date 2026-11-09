## ML Strategy

> **Time budget**: You have **{{HOURS}} hours**. Pacing: first ~25% baseline + K-fold + first ensemble; next ~50% iterate + blend + OOF stack; final ~25% finalize. If debugging dependencies past 30 min, abandon that path.

### Part 1 — Avoid these patterns

- Do not use `train_test_split` / a single holdout. Use K-fold from version 1.
- Do not lock into a single-action loop (e.g., 5 consecutive "tweak hyperparam" steps). Cycle through validation → feature → model → ensemble → re-validate.
- Do not open with a major rewrite as v1. Start from a small working baseline and iterate.
- Do not waste rounds on environment / dependency debugging across many iterations. If env / install / import issues keep coming up across multiple iterations, batch them: stop, dedicate one focused ~20–30 min session to fix them all (or reinstall the env from a clean state), then move on. Don't let env issues bleed across iterations.
- Do not sit in postprocessing tweak loops (rounding / clipping / calibration repeated). Set postprocessing once and move on.

### Part 2 — Core practices

- K-fold CV with prediction averaging across folds.
- First ensemble call within the first ~25% of your time budget — not at the end.
- Generate out-of-fold (OOF) predictions and stack them via a meta-learner (Ridge / LGBM-on-OOF) or weighted blend.
- Blend predictions from multiple models or seeds.
- Tune `sample_weight=` / loss when the leaderboard metric is stratified, weighted, or imbalanced relative to the default training loss.
- Keep adding ensemble members incrementally; don't stop at one model.
- Cache OOF arrays + trained model artifacts to disk so you can revisit any base model without retraining.
- Use multiple model families (e.g., transformer + tabular booster + Ridge head), not a single architecture.

### Part 3 — Polish

- Make many small / micro-magnitude changes early; avoid big sweeps in the first 20%.
- Implement a custom validation metric that mirrors the leaderboard.
- Use a custom loss / objective when the default isn't aligned with the metric.
- Average across multiple seeds for each base model.

### Part 4 — Task-type conditional

Identify your task type from the data (look at `sample_submission.csv` columns + the training data shape) and apply the relevant rule:

- **Text / NLP**: Use multiple pretrained transformer backbones (DeBERTa, RoBERTa, Electra, etc.) and blend their predictions. Multi-seed averaging per backbone.
- **Tabular**: Iterate on derived features — groupby aggregations, ratios, time-since-event windows, target-mean encoding for categoricals. When score plateaus, add 2–3 new engineered features per iteration before tweaking hyperparameters.
- **Image / CV**: Apply test-time augmentation (TTA) — predict on flipped / rotated / cropped versions of test inputs and average. Use heavy training-time augmentation (random crops, color jitter, mixup).
- **Time-series / signal**: Use efficient data I/O (parquet, polars). Window-based aggregate features.

### Part 5 — Self-check every 30–60 minutes

Run through these 7 questions periodically. If any is "no", fix it before adding new things.

1. Is my validation strategy K-fold, not single `train_test_split`?
2. Does my CV metric match the leaderboard metric exactly (same formula, same stratification, same weighting)?
3. Have I considered whether `sample_weight=` or a custom loss is needed for this metric (e.g., when the LB metric is stratified, weighted, or imbalanced relative to the default training loss)?
4. Have I made my first ensemble call yet? If past 25% of budget and the answer is "no", do it now — even a simple 2-model average counts.
5. Have I saved OOF predictions per base model to disk?
6. Am I blending at least 2 models or 2 seeds? How many ensemble members do I currently have?
7. Have I been stuck on the same task category for 3+ consecutive steps?

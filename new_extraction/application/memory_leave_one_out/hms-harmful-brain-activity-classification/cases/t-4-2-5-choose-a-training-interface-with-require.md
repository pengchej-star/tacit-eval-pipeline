# Choose a training interface with required controls  `T.4.2.5`   4 edits, 0 experts
2 scored cases, median improvement +0.00047, 1 improved


- expert 29588171 (Master) · amex · v9→v10   Switch to the native training API with a held-out validation set and early stopping. Compare the leaderboard score at the same blend weight. If the score does not improve, the gain from API-level control is negligible and effort is better spent elsewhere (e.g., features or hyperparameters).
    evidence: ✓ The current API obscures required probability output or evaluation controls.
    leaderboard score 0.79988 → 0.79973 (-0.00014)
- expert 28984551 (Contributor) · amex · v12→v13   Use the classifier variant of the model and extract class probabilities (not raw predictions) as stacking features. This keeps all base-learner outputs on the same [0,1] probability scale, improving ensemble coherence and typically the final metric.
    evidence: ✗ Outcomes contain censoring or the metric evaluates risk ranking within known subgroups. | ✓ The current API obscures required probability output or evaluation controls. | ✓ The existing ensemble already includes a model using the proposed target transform, so adding another would be redundant rather than diversifying.
    leaderboard score 0.79232 → 0.79279 (+0.00047)
- expert 28093671 (Contributor) · amex · v12→v15   Check which API was used to train the model. The low-level API's model object typically has only a generic `.predict()` method that returns probabilities when the objective is a classification loss. The scikit-learn wrapper adds `.predict_proba()`. Mixing them causes attribute errors. Match the pred
    evidence: ✓ The current API obscures required probability output or evaluation controls.
    leaderboard score n/a → n/a
- expert 27656049 (Expert) · amex · v6→v7   Use the scikit-learn-compatible estimator class. It handles dataset wrapping internally, provides a predict_proba method for direct probability output, and accepts early-stopping callbacks in the fit call, reducing boilerplate and integration friction.
    evidence: ✓ The current API obscures required probability output or evaluation controls.
    leaderboard score n/a → n/a
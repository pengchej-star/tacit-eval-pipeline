# Append structured text metadata  `T.4.4.4`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00571, 2 improved


- expert 7573212 · google · v4→v5   Compute surface-level text features (word counts, sentence counts, categorical indicators), standardize them, and concatenate them with the language model's pooled output before the prediction head. Retrain with these additional inputs and verify improvement on the leaderboard or validation metric.
    evidence: ✓ Structured metadata or surface statistics vary with targets but are absent from the model.
    leaderboard score 0.38324 → 0.38598 (higher is better; improved by 0.00273)
- expert 7240226 · google · v6→v7   One-hot encode the categorical metadata, concatenate it with the text encoder's pooled output, and feed the combined vector into the prediction head. Evaluate on the leaderboard or validation to confirm the gain.
    evidence: ✓ Structured metadata or surface statistics vary with targets but are absent from the model.
    leaderboard score 0.38126 → 0.38697 (higher is better; improved by 0.00571)
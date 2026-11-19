# Compare reduced and full precision  `T.3.1.4`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.00001, 1 improved


- expert 17371717 · commonlitreadabilityprize · v8→v9   Cast the model to half precision before running inference and compare the metric against full precision. For typical transformer regression tasks the score change is negligible, so half precision can be safely adopted to save memory and time.
    evidence: ✗ The raw table or engineered feature table exceeds memory before model inference starts. | ✓ Model tensors dominate memory and the current pipeline uses full precision. | ✗ Duplicate DataFrame copies (e.g., X_train/X_test/y_train/y_test) are created in a loop instead of using index-based slicing into a single master DataFrame, roughly doubling memory usage.
    leaderboard score 0.47270 → 0.47268 (lower is better; improved by 0.00001)
- expert 50376011 · hms · v210→v211   Test inference with mixed precision disabled (full FP32). If the score worsens or stays the same, keep mixed precision for its speed benefit. In this case the score got worse, indicating that the precision difference was not the bottleneck and the run-to-run variance or other factors dominated.
    evidence: ✓ Model tensors dominate memory and the current pipeline uses full precision.
    leaderboard score 0.25194 → 0.25970 (lower is better; worse by 0.00776)
# Reduce inference batch size  `T.3.1.3`   6 edits, 0 experts
4 scored cases, median improvement -0.00001, 0 improved


- expert 7670859 (Contributor) · google · v16→v17   Halve the inference batch size from the previous setting and re-run. If it still fails, halve again. Choose the largest power-of-two batch size that completes without memory errors to balance throughput and stability.
    evidence: ✗ The raw table or engineered feature table exceeds memory before model inference starts. | ✓ Memory failure occurs in a single forward pass and grows with batch size.
    leaderboard score n/a → n/a
- expert 50376011 (Grandmaster) · hms · v77→v79   Change only one variable at a time when possible. If a large batch size degrades the score, revert to the smaller default; large batches can cause silent OOM issues or numerical differences that hurt predictions, especially on limited GPU memory.
    evidence: ✓ Memory failure occurs in a single forward pass and grows with batch size.
    leaderboard score 0.36160 → 0.33044 (-0.03116)
- expert 50376011 (Grandmaster) · hms · v221→v222   When expanding the number of ensemble members, proportionally reduce the inference batch size to keep peak memory within budget. Process one model at a time, accumulate predictions, and average at the end.
    evidence: ✓ Memory failure occurs in a single forward pass and grows with batch size. | ✗ Model tensors dominate memory and the current pipeline uses full precision.
    leaderboard score 0.24562 → 0.23868 (-0.00694)
- expert 15372370 (Expert) · ranzcr · v3→v4   Reduce the batch size to fit within memory constraints and verify that the metric is unchanged. This is safe whenever the model's forward pass does not depend on batch statistics at inference time.
    evidence: ✓ Memory failure occurs in a single forward pass and grows with batch size.
    leaderboard score 0.96342 → 0.96341 (-0.00001)
- expert 15173072 (Contributor) · ranzcr · v13→v14   Increase the inference batch size as much as GPU memory allows for speed. Expect identical predictions and scores, since eval-mode batch norm and deterministic forward passes are independent of batch size.
    evidence: ✗ Memory failure occurs in a single forward pass and grows with batch size.
    leaderboard score 0.96062 → 0.96062 (+0.00000)
- expert 50496431 (Grandmaster) · hms · v62→v68   Start with a conservatively small batch size (e.g., one-eighth of the default) for the new model. Only increase after verifying that checkpoint loading is strict (no missing/unexpected keys) and that model configuration parameters exactly match the trained checkpoint. A sudden catastrophic score is 
    evidence: ✓ Memory failure occurs in a single forward pass and grows with batch size. | ✗ The raw table or engineered feature table exceeds memory before model inference starts. | ✗ Peak memory is driven by the number of sequential inference passes (e.g., seed replicas) kept simultaneously in memory.
    leaderboard score n/a → 0.30784
# Change text-stream structure  `T.4.4.3`   2 edits, 0 experts
2 scored cases (improvement signed by each competition's direction), median +0.01260, 1 improved


- expert 17371717 · commonlitreadabilityprize · v21→v23   Try the paired-input approach and measure validation or leaderboard impact. If it hurts performance, revert the pairing but keep any simpler architectural improvements (e.g., a cleaner attention pooling) that emerged during the experiment. Paired encoding adds sequence length and may confuse a model
    evidence: ✓ The pretrained checkpoint was trained on single-sequence input, so switching to paired encoding at inference creates a train/inference mismatch. | ✓ Distinct text fields are flattened together despite different roles in the target.
    leaderboard score 0.46533 → 0.46690 (lower is better; worse by 0.00157)
- expert 7613444 · google · v2→v5   Separate the two semantically distinct text segments into dedicated input streams through the pretrained encoder, each with its own tokenization and segment handling, rather than concatenating everything into one sequence. Use a loss function (e.g., binary cross-entropy for bounded targets) that mat
    evidence: ✓ Custom normalization changes text beyond the tokenizer’s training assumptions. | ✓ Distinct text fields are flattened together despite different roles in the target. | ✗ The pretrained checkpoint was trained on single-sequence input, so switching to paired encoding at inference creates a train/inference mismatch.
    leaderboard score 0.38542 → 0.39802 (higher is better; improved by 0.01260)
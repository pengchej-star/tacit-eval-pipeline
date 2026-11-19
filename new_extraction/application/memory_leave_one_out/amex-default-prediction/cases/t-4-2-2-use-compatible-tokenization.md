# Use compatible tokenization  `T.4.2.2`   2 edits, 0 experts
1 scored cases, median improvement +0.00000, 0 improved


- expert 17371717 (Master) · commonlitreadabilityprize · v1→v2   Replace manual preprocessing with the library's native parameter. Submit or validate to confirm the output is equivalent or better, establishing a clean baseline before making architectural changes.
    evidence: ✓ Manual padding, special tokens, or masks differ from the training tokenizer. | ✗ A previous version without this text cleaning scored higher than the version with it, suggesting the preprocessing hurts performance.
    leaderboard score 0.47570 → 0.47570 (+0.00000)
- expert 55621328 (Master) · learning · v8→v9   Add special whitespace tokens (e.g., newline characters) to the tokenizer as added tokens, ensuring the inference tokenizer matches the one used during fine-tuning. Verify the tokenizer vocabulary size matches the model's embedding layer.
    evidence: ✓ Manual padding, special tokens, or masks differ from the training tokenizer. | ✗ The model is fixed and no checkpoint was trained for the proposed new prompt or vocabulary. | ✓ The text preprocessing applied at inference differs from what was used during training of the loaded checkpoint, creating a train/inference mismatch. | ✗ The pretrained encoder's subword tokenization already handles misspellings and special characters, making explicit text cleaning redundant.
    leaderboard score 0.78266 → n/a
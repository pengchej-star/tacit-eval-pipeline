# Restore the training tokenizer  `T.1.1.2`   7 edits, 0 experts
2 scored cases, median improvement +0.07047, 1 improved


- expert 18837555 (Expert) · commonlitreadabilityprize · v2→v5   Before debugging model logic, verify that (1) the tokenizer is explicitly instantiated from the correct path, (2) all checkpoint file paths resolve to existing files, and (3) the tokenizer path matches the vocabulary the model was fine-tuned with. Fix one path variable at a time and re-run to isolat
    evidence: ✓ Tokenizer vocabulary or special-token handling differs from the fine-tuning artifact. | ✓ Checkpoint or model artifact file paths do not resolve to existing files in the current environment.
    leaderboard score 0.46181 → 0.46041 (-0.00141)
- expert 7240226 (Contributor) · google · v1→v3   Verify that the model weights path and the tokenizer/vocabulary path point to artifacts from the same release. Confirm the casing flag (lower-case vs. cased) matches the checkpoint variant. Run a quick sanity check (e.g., encode one example and inspect token ids) before launching full training.
    evidence: ✓ Tokenizer vocabulary or special-token handling differs from the fine-tuning artifact. | ✓ Configuration or logging references point to the wrong model name or architecture, indicating a copy-paste error that may affect runtime settings. | ✓ Checkpoint or model artifact file paths do not resolve to existing files in the current environment.
    leaderboard score n/a → n/a
- expert 55621328 (Master) · learning · v34→v36   Ensure the model's vocab_size config parameter matches the tokenizer length, and call the embedding-resize method after model instantiation but before loading the checkpoint weights. If unsure whether resizing is needed, temporarily disable it to check for errors, then re-enable with the correct voc
    evidence: ✓ Checkpoint keys or tensor dimensions do not match the instantiated model. | ✓ Tokenizer vocabulary or special-token handling differs from the fine-tuning artifact. | ✓ A config file default value differs from the setting used when the checkpoint was trained.
    leaderboard score n/a → 0.81031
- expert 55621328 (Master) · learning · v107→v108   Do not override vocabulary size unless there is clear evidence of a mismatch (e.g., a runtime error). If you override it and the score drops substantially, revert immediately — the checkpoint's saved config almost certainly already encodes the correct vocabulary size.
    evidence: ✓ Checkpoint keys or tensor dimensions do not match the instantiated model. | ✓ Tokenizer vocabulary or special-token handling differs from the fine-tuning artifact. | ✗ Checkpoint or model artifact file paths do not resolve to existing files in the current environment. | ✓ A config file default value differs from the setting used when the checkpoint was trained.
    leaderboard score n/a → 0.81837
- expert 55621328 (Master) · learning · v8→v9   Add special whitespace tokens (e.g., newline characters) to the tokenizer as added tokens, ensuring the inference tokenizer matches the one used during fine-tuning. Verify the tokenizer vocabulary size matches the model's embedding layer.
    evidence: ✓ Tokenizer vocabulary or special-token handling differs from the fine-tuning artifact.
    leaderboard score 0.78266 → n/a
- expert 55621328 (Master) · learning · v19→v22   Ensure the tokenizer configuration at inference exactly matches training. Never add special tokens to the tokenizer at inference unless the checkpoint was trained with those tokens. If uncertain whether a checkpoint included extra tokens, run inference both ways and compare scores to confirm.
    evidence: ✓ Tokenizer vocabulary or special-token handling differs from the fine-tuning artifact.
    leaderboard score n/a → 0.73480
- expert 55621328 (Master) · learning · v22→v27   When adding special tokens to a tokenizer at inference, also update the code that locates special token positions (e.g., mask token index) in the encoded output. Extract and pass the correct position index to the model. Verify the returned index is the expected type (scalar vs. list) to avoid shape 
    evidence: ✓ Tokenizer vocabulary or special-token handling differs from the fine-tuning artifact. | ✓ The mask token position index is not correctly computed, typed, or propagated from tokenization through the dataset to the model forward pass. | ✓ Checkpoint or model artifact file paths do not resolve to existing files in the current environment.
    leaderboard score 0.73480 → 0.80527 (+0.07047)
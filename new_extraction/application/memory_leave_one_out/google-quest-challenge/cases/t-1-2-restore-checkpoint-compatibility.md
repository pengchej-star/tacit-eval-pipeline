# Restore checkpoint compatibility  `T.1.2`   26 edits, 0 experts
14 scored cases, median improvement +0.00024, 7 improved


- expert 18426209 (Expert) · commonlitreadabilityprize · v2→v3   When upgrading a backbone size, verify that (1) every layer referencing the hidden dimension is updated, (2) the loaded checkpoint was fine-tuned with the exact same architecture definition, and (3) run a quick sanity check on a few predictions before submitting. A large score regression signals a w
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences.
    leaderboard score 0.46287 → 0.74137 (+0.27850)
- expert 18837555 (Expert) · commonlitreadabilityprize · v2→v5   Before debugging model logic, verify that (1) the tokenizer is explicitly instantiated from the correct path, (2) all checkpoint file paths resolve to existing files, and (3) the tokenizer path matches the vocabulary the model was fine-tuned with. Fix one path variable at a time and re-run to isolat
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Execution stops at an import, file access, device operation, or library call.
    leaderboard score 0.46181 → 0.46041 (-0.00141)
- expert 18423958 (Master) · commonlitreadabilityprize · v1→v3   When changing backbone size, update every hidden-size-dependent layer dimension in the custom head (attention layers, linear regressors) to match the new backbone's hidden size. If pretrained checkpoints for the larger variant are unavailable or cause errors, revert to the smaller variant with its m
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Execution stops at an import, file access, device operation, or library call.
    leaderboard score 0.46275 → 0.46226 (-0.00049)
- expert 17371717 (Master) · commonlitreadabilityprize · v6→v7   Before discarding the approach, audit the implementation details: verify that learnable weight parameters are properly normalized (e.g., softmax), that aggregation operations match the intended math (sum vs. mean), that output dimensions match the loss function, and that inference loads the correct 
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Written predictions have the wrong direction, range, normalization, or source variable.
    leaderboard score 0.48546 → 0.47432 (-0.01114)
- expert 75145694 (Expert) · equity · v16→v17   Replicate the exact preprocessing pipeline (imputer, scaler) used during training, create a dedicated inference branch for the new model, and add verbose logging that prints input shapes, loaded model details, and output statistics. Verify these logs before trusting the blended result. This catches 
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ The executed ensemble does not match its configured members or weights. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score 0.68867 → 0.69070 (+0.00203)
- expert 49524919 (Grandmaster) · hms · v46→v47   Update every architecture hyperparameter in the inference code (width, depth, head dimensions, activation type) to exactly match the training configuration of the new checkpoints. Change them all in one coordinated edit together with the checkpoint path swap, and also revisit any test-time augmentat
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences.
    leaderboard score 0.46059 → 0.41674 (-0.04385)
- expert 53762022 (Contributor) · hms · v5→v7   Always verify that every architecture hyperparameter in the inference code exactly matches the configuration used during training of the checkpoint. Change the architecture definition and the checkpoint together, not separately. After swapping, compare a few sample outputs against the old model befo
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences.
    leaderboard score n/a → 0.40866
- expert 55621328 (Master) · learning · v3→v5   After changing the checkpoint and config paths, audit every conditional branch that dispatches on the experiment name (or config key) and add the new identifier to the appropriate branch so the correct model class, tokenizer, and preprocessing are used. Test that the pipeline loads and runs before s
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Execution stops at an import, file access, device operation, or library call.
    leaderboard score 0.78177 → n/a
- expert 55621328 (Master) · learning · v19→v22   Ensure the tokenizer configuration at inference exactly matches training. Never add special tokens to the tokenizer at inference unless the checkpoint was trained with those tokens. If uncertain whether a checkpoint included extra tokens, run inference both ways and compare scores to confirm.
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences.
    leaderboard score n/a → 0.73480
- expert 55621328 (Master) · learning · v22→v27   When adding special tokens to a tokenizer at inference, also update the code that locates special token positions (e.g., mask token index) in the encoded output. Extract and pass the correct position index to the model. Verify the returned index is the expected type (scalar vs. list) to avoid shape 
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Execution stops at an import, file access, device operation, or library call. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation. | ✓ Sample identifiers or feature columns differ between prediction sources or stages.
    leaderboard score 0.73480 → 0.80527 (+0.07047)
- expert 55621328 (Master) · learning · v34→v36   Ensure the model's vocab_size config parameter matches the tokenizer length, and call the embedding-resize method after model instantiation but before loading the checkpoint weights. If unsure whether resizing is needed, temporarily disable it to check for errors, then re-enable with the correct voc
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.81031
- expert 55621328 (Master) · learning · v69→v71   Always update the pretrained model path to match the architecture size of the fine-tuned checkpoint. Treat the checkpoint file and the pretrained backbone path as a coupled pair that must be changed together.
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences.
    leaderboard score 0.81872 → 0.82319 (+0.00447)
- expert 55621328 (Master) · learning · v107→v108   Do not override vocabulary size unless there is clear evidence of a mismatch (e.g., a runtime error). If you override it and the score drops substantially, revert immediately — the checkpoint's saved config almost certainly already encodes the correct vocabulary size.
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences.
    leaderboard score n/a → 0.81837
- expert 55621328 (Master) · learning · v111→v113   Explicitly override architecture-critical parameters at inference time to match the settings used during training. Check output dimensionality, optional module flags, and any parameter that changes the model graph. Verify by confirming the run completes and produces plausible outputs before submitti
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ The executed ensemble does not match its configured members or weights.
    leaderboard score 0.80843 → 0.82329 (+0.01487)
- expert 55621328 (Master) · learning · v117→v119   First load with strict mode enabled to identify exactly which keys are missing or unexpected. If the mismatched keys are auxiliary (e.g., an extra loss head not needed at inference), switch to non-strict loading so the matched weights are used and unmatched ones are ignored. Verify that the resultin
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.82840
- expert 55621328 (Master) · learning · v115→v117   When swapping in a checkpoint from a different training run, also update the import path or installed package version to match the code that produced that checkpoint. Verify that config files, tokenizer vocabulary, and model class definitions are all consistent before running inference.
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ The executed ensemble does not match its configured members or weights. | ✓ Execution stops at an import, file access, device operation, or library call.
    leaderboard score 0.80119 → n/a
- expert 15082684 (Master) · ranzcr · v19→v22   Add debug prints to inspect the loaded state dict (keys, shapes, count) immediately after loading. Compare against the model's expected parameters. Check that every configuration flag (architecture variant, head type, number of outputs) matches the training configuration of those specific checkpoint
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✗ Execution stops at an import, file access, device operation, or library call. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score 0.96183 → 0.96591 (+0.00408)
- expert 15082684 (Master) · ranzcr · v22→v23   Before loading, iterate over the state_dict and strip the wrapper prefix from each key using string manipulation, then load the cleaned dict. Also set the map_location to the target device to avoid device-mismatch errors.
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Execution stops at an import, file access, device operation, or library call.
    leaderboard score 0.96591 → n/a
- expert 15164527 (Expert) · ranzcr · v1→v2   Verify that every submodule's attribute name in the class definition exactly matches the name used in forward(), in checkpoint state-dict keys, and in any layer-replacement code. Print or diff the model's state_dict keys against the checkpoint keys to catch mismatches.
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences.
    leaderboard score n/a → n/a
- expert 13521245 (Grandmaster) · ranzcr · v11→v14   Before removing a custom model package, verify that the replacement loader reconstructs an identical architecture and that all saved weights are restored (check for warnings or layer-count mismatches). If weights don't transfer, retrain or keep the original package rather than expecting a pure infra
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Execution stops at an import, file access, device operation, or library call. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation.
    leaderboard score 0.94487 → 0.77458 (-0.17029)
- expert 13702907 (Contributor) · ranzcr · v10→v12   When modifying the classification head for inference, ensure the new architecture exactly matches the checkpoint's layer names and shapes. Test changes incrementally: first verify the model loads and runs, then check that predictions are sensible, before submitting. If a head change degrades score s
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.94757
- expert 13702907 (Contributor) · ranzcr · v17→v19   When inference must run under a specific device strategy, prefer recreating the model architecture inside that strategy's scope and loading only the weights, rather than deserializing the full model from a saved file. Test both paths and verify outputs before submitting.
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation. | ✓ Execution stops at an import, file access, device operation, or library call.
    leaderboard score 0.95232 → 0.95256 (+0.00024)
- expert 13702907 (Contributor) · ranzcr · v23→v25   Test both approaches and compare outputs. If scores differ, suspect an architecture mismatch (e.g., different dropout mode, layer configuration) rather than a fundamental difference in the loading method. Prefer the approach where the architecture definition is explicitly controlled in code, as it i
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation. | ✓ Execution stops at an import, file access, device operation, or library call.
    leaderboard score 0.95237 → 0.95228 (-0.00009)
- expert 50496431 (Grandmaster) · hms · v11→v12   Store checkpoints in per-model directories and discover them programmatically (e.g., list all files matching a pattern in the directory). This ensures all trained folds are included automatically and reduces copy-paste errors when updating the ensemble.
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ The executed ensemble does not match its configured members or weights.
    leaderboard score 0.37435 → 0.36527 (-0.00907)
- expert 50496431 (Grandmaster) · hms · v65→v68   Enable strict checkpoint loading to catch architecture-checkpoint mismatches immediately. Verify that all model constructor parameters (input dimensions, depth, temporal length) match the training configuration exactly. Fix these before adjusting batch size or other inference settings. A catastrophi
    evidence: ✓ Substantive changes leave predictions unchanged or a silent fallback bypasses the intended computation. | ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✗ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.30784
- expert 50496431 (Grandmaster) · hms · v79→v80   Always use strict weight loading (exact key matching) after any architecture change. If it raises an error, the checkpoint is incompatible and must be retrained or the architecture reverted. This prevents silent degradation from partially loaded weights.
    evidence: ✓ A checkpoint swap introduced missing keys, incompatible dimensions, or tokenizer differences. | ✓ Execution stops at an import, file access, device operation, or library call.
    leaderboard score n/a → 0.29794
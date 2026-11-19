# Match architecture and weights  `T.1.1.1`   34 edits, 0 experts
18 scored cases, median improvement +0.00338, 10 improved


- expert 18426209 (Expert) · commonlitreadabilityprize · v2→v3   When upgrading a backbone size, verify that (1) every layer referencing the hidden dimension is updated, (2) the loaded checkpoint was fine-tuned with the exact same architecture definition, and (3) run a quick sanity check on a few predictions before submitting. A large score regression signals a w
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score 0.46287 → 0.74137 (+0.27850)
- expert 18423958 (Master) · commonlitreadabilityprize · v1→v3   When changing backbone size, update every hidden-size-dependent layer dimension in the custom head (attention layers, linear regressors) to match the new backbone's hidden size. If pretrained checkpoints for the larger variant are unavailable or cause errors, revert to the smaller variant with its m
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✗ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.46275 → 0.46226 (-0.00049)
- expert 18423958 (Master) · commonlitreadabilityprize · v3→v4   When swapping a backbone, verify that the hidden dimension, tokenizer, and checkpoint weights are all mutually consistent before trusting the leaderboard result. If the score degrades dramatically (e.g., more than doubles), suspect a configuration mismatch rather than concluding the backbone is infe
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ The same raw example produces different training and inference features.
    leaderboard score 0.46226 → 1.04188 (+0.57961)
- expert 17371717 (Master) · commonlitreadabilityprize · v9→v11   Be cautious about changing the model head architecture at inference time without retraining checkpoints to match. If checkpoints were trained with a simpler head, loading them into a more complex head will likely degrade performance. Verify architecture-checkpoint compatibility before submitting, an
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.47268 → 0.47606 (+0.00338)
- expert 17371717 (Master) · commonlitreadabilityprize · v30→v33   Sweep pooling variants (e.g., mean-only vs. concatenated mean+max over hidden layers) jointly with checkpoint versions, changing one factor at a time. Compare leaderboard or validation scores for each combination to identify the correct pairing, since using the wrong pooling for a given checkpoint w
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.47074 → 0.46357 (-0.00717)
- expert 6803050 (Master) · google · v37→v39   When a score drops unexpectedly after changing checkpoint paths, verify every path string character-by-character. Load one fold at a time and check that the model produces non-trivial outputs before running the full ensemble. Treat any sudden regression after a path change as a path bug until proven
    evidence: ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.29940 → 0.38287 (+0.08347)
- expert 7606235 (Master) · google · v18→v23   Before submitting, verify that all checkpoint paths resolve correctly and that the ensemble code actually loads and averages the intended models (e.g., print model count and a sample prediction). Use a local validation split to pre-screen checkpoint combinations and only submit the most promising on
    evidence: ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.38871 → 0.38785 (-0.00086)
- expert 7240226 (Contributor) · google · v1→v3   Verify that the model weights path and the tokenizer/vocabulary path point to artifacts from the same release. Confirm the casing flag (lower-case vs. cased) matches the checkpoint variant. Run a quick sanity check (e.g., encode one example and inspect token ids) before launching full training.
    evidence: ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ The same raw example produces different training and inference features.
    leaderboard score n/a → n/a
- expert 49524919 (Grandmaster) · hms · v36→v46   Check and fix these in order: (1) ensure the model architecture (layer sizes, branches present/absent, activation functions) exactly matches what was used during training; (2) verify that preprocessing and augmentation flags reference the correct variables; (3) confirm that the post-processing step 
    evidence: ✗ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✓ The same raw example produces different training and inference features.
    leaderboard score n/a → 0.46059
- expert 49524919 (Grandmaster) · hms · v46→v47   Update every architecture hyperparameter in the inference code (width, depth, head dimensions, activation type) to exactly match the training configuration of the new checkpoints. Change them all in one coordinated edit together with the checkpoint path swap, and also revisit any test-time augmentat
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score 0.46059 → 0.41674 (-0.04385)
- expert 49524919 (Grandmaster) · hms · v47→v49   After a regression from a combined architecture+checkpoint change, inspect the forward pass carefully for correctness bugs before concluding the architecture or checkpoints are worse. Fix any bugs first, then re-evaluate. Only after confirming correctness should you continue sweeping checkpoints or 
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.41674 → 0.41042 (-0.00633)
- expert 53762022 (Contributor) · hms · v5→v7   Always verify that every architecture hyperparameter in the inference code exactly matches the configuration used during training of the checkpoint. Change the architecture definition and the checkpoint together, not separately. After swapping, compare a few sample outputs against the old model befo
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score n/a → 0.40866
- expert 55621328 (Master) · learning · v19→v22   Ensure the tokenizer configuration at inference exactly matches training. Never add special tokens to the tokenizer at inference unless the checkpoint was trained with those tokens. If uncertain whether a checkpoint included extra tokens, run inference both ways and compare scores to confirm.
    evidence: ✓ The same raw example produces different training and inference features. | ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score n/a → 0.73480
- expert 55621328 (Master) · learning · v22→v27   When adding special tokens to a tokenizer at inference, also update the code that locates special token positions (e.g., mask token index) in the encoded output. Extract and pass the correct position index to the model. Verify the returned index is the expected type (scalar vs. list) to avoid shape 
    evidence: ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ The same raw example produces different training and inference features.
    leaderboard score 0.73480 → 0.80527 (+0.07047)
- expert 55621328 (Master) · learning · v34→v36   Ensure the model's vocab_size config parameter matches the tokenizer length, and call the embedding-resize method after model instantiation but before loading the checkpoint weights. If unsure whether resizing is needed, temporarily disable it to check for errors, then re-enable with the correct voc
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ The same raw example produces different training and inference features.
    leaderboard score n/a → 0.81031
- expert 55621328 (Master) · learning · v69→v71   Always update the pretrained model path to match the architecture size of the fine-tuned checkpoint. Treat the checkpoint file and the pretrained backbone path as a coupled pair that must be changed together.
    evidence: ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score 0.81872 → 0.82319 (+0.00447)
- expert 55621328 (Master) · learning · v107→v108   Do not override vocabulary size unless there is clear evidence of a mismatch (e.g., a runtime error). If you override it and the score drops substantially, revert immediately — the checkpoint's saved config almost certainly already encodes the correct vocabulary size.
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score n/a → 0.81837
- expert 55621328 (Master) · learning · v109→v111   Treat major inference pipeline changes (new tokenizer vocabulary, new special tokens, new model wrapper) as high-risk. Submit them only after verifying on a local validation set that predictions are reasonable. If the score drops sharply, revert to the known-good pipeline before trying incremental f
    evidence: ✓ The same raw example produces different training and inference features. | ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score 0.82798 → 0.80843 (-0.01955)
- expert 55621328 (Master) · learning · v111→v113   Explicitly override architecture-critical parameters at inference time to match the settings used during training. Check output dimensionality, optional module flags, and any parameter that changes the model graph. Verify by confirming the run completes and produces plausible outputs before submitti
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.80843 → 0.82329 (+0.01487)
- expert 55621328 (Master) · learning · v117→v119   First load with strict mode enabled to identify exactly which keys are missing or unexpected. If the mismatched keys are auxiliary (e.g., an extra loss head not needed at inference), switch to non-strict loading so the matched weights are used and unmatched ones are ignored. Verify that the resultin
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.82840
- expert 55621328 (Master) · learning · v115→v117   When swapping in a checkpoint from a different training run, also update the import path or installed package version to match the code that produced that checkpoint. Verify that config files, tokenizer vocabulary, and model class definitions are all consistent before running inference.
    evidence: ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score 0.80119 → n/a
- expert 55621328 (Master) · learning · v141→v142   When swapping backbone sizes, ensure the checkpoints were actually trained with that backbone. Simply changing the pretrained path to a smaller variant while loading checkpoints trained on a larger variant will degrade performance or fail silently due to weight mismatches. Always verify checkpoint-b
    evidence: none recorded
    leaderboard score n/a → 0.82067
- expert 55431616 (Grandmaster) · learning · v27→v28   Enumerate checkpoints explicitly rather than using file-system glob patterns. Initialize the tokenizer and preprocess data inside each checkpoint's inference loop to guarantee compatibility. Free model memory (garbage collection, cache clearing) between checkpoints. Average the per-checkpoint output
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → n/a
- expert 15082684 (Master) · ranzcr · v19→v22   Add debug prints to inspect the loaded state dict (keys, shapes, count) immediately after loading. Compare against the model's expected parameters. Check that every configuration flag (architecture variant, head type, number of outputs) matches the training configuration of those specific checkpoint
    evidence: ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score 0.96183 → 0.96591 (+0.00408)
- expert 15082684 (Master) · ranzcr · v22→v23   Before loading, iterate over the state_dict and strip the wrapper prefix from each key using string manipulation, then load the cleaned dict. Also set the map_location to the target device to avoid device-mismatch errors.
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score 0.96591 → n/a
- expert 15164527 (Expert) · ranzcr · v1→v2   Verify that every submodule's attribute name in the class definition exactly matches the name used in forward(), in checkpoint state-dict keys, and in any layer-replacement code. Print or diff the model's state_dict keys against the checkpoint keys to catch mismatches.
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score n/a → n/a
- expert 15173072 (Contributor) · ranzcr · v6→v7   Treat a score near random chance as evidence that model weights are not effectively loaded or applied. Check: (1) the model is set to evaluation mode, (2) the architecture definition matches the checkpoint's layer names, (3) input preprocessing (normalization mean/std, resolution) matches what was u
    evidence: none recorded
    leaderboard score n/a → 0.50990
- expert 15173072 (Contributor) · ranzcr · v7→v8   Check that (1) the model is set to evaluation mode so dropout and batch-norm behave correctly, and (2) the checkpoint file actually matches the model architecture being constructed. Fix both before investigating other issues.
    evidence: ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.50990 → 0.55637 (+0.04647)
- expert 13521245 (Grandmaster) · ranzcr · v11→v14   Before removing a custom model package, verify that the replacement loader reconstructs an identical architecture and that all saved weights are restored (check for warnings or layer-count mismatches). If weights don't transfer, retrain or keep the original package rather than expecting a pure infra
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✓ The same raw example produces different training and inference features.
    leaderboard score 0.94487 → 0.77458 (-0.17029)
- expert 13702907 (Contributor) · ranzcr · v10→v12   When modifying the classification head for inference, ensure the new architecture exactly matches the checkpoint's layer names and shapes. Test changes incrementally: first verify the model loads and runs, then check that predictions are sensible, before submitting. If a head change degrades score s
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions. | ✗ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.94757
- expert 13702907 (Contributor) · ranzcr · v17→v19   When inference must run under a specific device strategy, prefer recreating the model architecture inside that strategy's scope and loading only the weights, rather than deserializing the full model from a saved file. Test both paths and verify outputs before submitting.
    evidence: ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score 0.95232 → 0.95256 (+0.00024)
- expert 13702907 (Contributor) · ranzcr · v23→v25   Test both approaches and compare outputs. If scores differ, suspect an architecture mismatch (e.g., different dropout mode, layer configuration) rather than a fundamental difference in the loading method. Prefer the approach where the architecture definition is explicitly controlled in code, as it i
    evidence: ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score 0.95237 → 0.95228 (-0.00009)
- expert 50496431 (Grandmaster) · hms · v65→v68   Enable strict checkpoint loading to catch architecture-checkpoint mismatches immediately. Verify that all model constructor parameters (input dimensions, depth, temporal length) match the training configuration exactly. Fix these before adjusting batch size or other inference settings. A catastrophi
    evidence: ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score n/a → 0.30784
- expert 50496431 (Grandmaster) · hms · v79→v80   Always use strict weight loading (exact key matching) after any architecture change. If it raises an error, the checkpoint is incompatible and must be retrained or the architecture reverted. This prevents silent degradation from partially loaded weights.
    evidence: ✓ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score n/a → 0.29794
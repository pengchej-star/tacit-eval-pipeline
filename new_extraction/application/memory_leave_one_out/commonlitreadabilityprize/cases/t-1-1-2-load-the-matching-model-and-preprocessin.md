# Load the matching model and preprocessing artifacts  `T.1.1.2`   45 edits, 0 experts
26 scored cases (improvement signed by each competition's direction), median +0.00447, 20 improved


- expert 13848868 · ranzcr · v36→v37   Set the inference input resolution to match the resolution the checkpoint was trained at. Start with raw score averaging (no rank transform) as the baseline, then toggle the rank transform to see which post-processing is better for this particular checkpoint.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration.
    leaderboard score 0.95509 → 0.95762 (higher is better; improved by 0.00253)
- expert 75924487 · equity · v11→v13   When updating artifact paths, verify that column names, fold indices, and row counts of the new OOF files match what the ensembler expects. Remove or rename stale path variables immediately. Submit only after a local validation check confirms the new artifacts reproduce or improve the previous CV sc
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a (higher is better)
- expert 75145694 · equity · v16→v17   Replicate the exact preprocessing pipeline (imputer, scaler) used during training, create a dedicated inference branch for the new model, and add verbose logging that prints input shapes, loaded model details, and output statistics. Verify these logs before trusting the blended result. This catches 
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.68867 → 0.69070 (higher is better; improved by 0.00203)
- expert 75145694 · equity · v59→v60   Create a dedicated feature-preparation function for each model that replicates the exact preprocessing used during that model's training (specific imputation, encoding, derived features). Route inference through the correct function based on model identity. This avoids cross-contamination of preproc
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration.
    leaderboard score 0.69324 → 0.69325 (higher is better; improved by 0.00001)
- expert 7613444 · google · v11→v12   Log or print the full resolved file path before loading each checkpoint, and add an explicit existence check or assertion. This catches naming mismatches early and prevents silent omission of fold models from the ensemble.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.39956 → 0.40047 (higher is better; improved by 0.00091)
- expert 7606235 · google · v1→v6   Before referencing a checkpoint path in code, list the actual files in the input directory (e.g., with a shell command or directory listing) to confirm the exact slug, subdirectory, and file extension. Fix all mismatches in one edit rather than iterating blindly.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score n/a → n/a (higher is better)
- expert 7606235 · google · v9→v15   Isolate the variable being tested: either load only the single checkpoint under evaluation, or freeze all other ensemble members and vary only one slot. Without this control, score differences are confounded and the sweep results are unreliable.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.38394 → 0.38524 (higher is better; improved by 0.00130)
- expert 7240226 · google · v1→v3   Verify that the model weights path and the tokenizer/vocabulary path point to artifacts from the same release. Confirm the casing flag (lower-case vs. cased) matches the checkpoint variant. Run a quick sanity check (e.g., encode one example and inspect token ids) before launching full training.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → n/a (higher is better)
- expert 53424936 · hms · v19→v20   Audit every preprocessing function for dependencies on label-derived quantities. Replace any such dependency with a test-compatible default (e.g., a fixed canonical offset). After fixing, verify the score recovers or improves beyond the simpler baseline.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.22756 (lower is better)
- expert 50376011 · hms · v20→v21   Write a dedicated inference script that exactly mirrors training: reconstruct the model architecture, restore the full config, load weights with the same utility used during training, run predictions with the same batching and data pipeline, and serialize per-model outputs for downstream ensembling.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration.
    leaderboard score 0.41352 → 0.39943 (lower is better; improved by 0.01409)
- expert 49524919 · hms · v29→v34   When introducing a new preprocessing branch, audit every function call and variable reference in the inference loop to ensure it uses the new branch's transforms, normalization, and imputation—not the old ones. Specifically check: (1) the correct transform/augmentation object is called, (2) missing-
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.55426 (lower is better)
- expert 49524919 · hms · v36→v46   Check and fix these in order: (1) ensure the model architecture (layer sizes, branches present/absent, activation functions) exactly matches what was used during training; (2) verify that preprocessing and augmentation flags reference the correct variables; (3) confirm that the post-processing step 
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file. | ✗ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ Individual models produce varying outputs but the saved submission is constant, partial or duplicates a member. | ✓ Predictions or new features no longer match the original sample identifiers or column order.
    leaderboard score n/a → 0.46059 (lower is better)
- expert 49524919 · hms · v46→v47   Update every architecture hyperparameter in the inference code (width, depth, head dimensions, activation type) to exactly match the training configuration of the new checkpoints. Change them all in one coordinated edit together with the checkpoint path swap, and also revisit any test-time augmentat
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.46059 → 0.41674 (lower is better; improved by 0.04385)
- expert 49576186 · hms · v24→v26   Apply the exact per-channel mean and standard deviation normalization that the pretrained backbone was trained with. This typically recovers a significant portion of the performance gap, but may not fully close it if the underlying representation change (e.g., colormap vs. original channels) is subo
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.37436 → 0.36532 (lower is better; improved by 0.00904)
- expert 52860091 · hms · v5→v7   When swapping model artifacts in a config-driven pipeline, verify that all required configuration overrides (e.g., environment mode, paths, runtime flags) are set correctly for the target execution context. If a run produces no submission, check the configuration layer before suspecting the model fi
    evidence: ✓ No end-to-end run has yet produced a verified prediction file. | ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration.
    leaderboard score 0.36479 → 0.34843 (lower is better; improved by 0.01636)
- expert 52860091 · hms · v43→v48   Set up a separate output directory and import path for the new codebase. Run data conversion and inference independently, saving outputs with distinct version-tagged filenames. Verify the new predictions in isolation (submit or validate alone) before blending, so any integration bugs are caught befo
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.25606 → 0.27952 (lower is better; worse by 0.02346)
- expert 52551258 · hms · v5→v7   When a model swap degrades performance, check that the inference-time preprocessing (filtering, normalization, downsampling) exactly matches what the checkpoint was trained with, and that the output transformation (e.g., softmax vs. log-softmax) is correct. Fix preprocessing alignment before conclud
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.37494 → 0.32513 (lower is better; improved by 0.04982)
- expert 52551258 · hms · v20→v21   Ensure the inference-time feature extraction (spectral transform parameters, normalization, cropping/resizing) exactly matches what was used during training. When the training pipeline is uncertain, try the most likely transform library and parameters, and measure the score change. A large improveme
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.51146 → 0.33979 (lower is better; improved by 0.17167)
- expert 53762022 · hms · v5→v7   Always verify that every architecture hyperparameter in the inference code exactly matches the configuration used during training of the checkpoint. Change the architecture definition and the checkpoint together, not separately. After swapping, compare a few sample outputs against the old model befo
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration.
    leaderboard score n/a → 0.40866 (lower is better)
- expert 55621328 · learning · v3→v5   After changing the checkpoint and config paths, audit every conditional branch that dispatches on the experiment name (or config key) and add the new identifier to the appropriate branch so the correct model class, tokenizer, and preprocessing are used. Test that the pipeline loads and runs before s
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.78177 → n/a (higher is better)
- expert 55621328 · learning · v19→v22   Ensure the tokenizer configuration at inference exactly matches training. Never add special tokens to the tokenizer at inference unless the checkpoint was trained with those tokens. If uncertain whether a checkpoint included extra tokens, run inference both ways and compare scores to confirm.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.73480 (higher is better)
- expert 55621328 · learning · v22→v27   When adding special tokens to a tokenizer at inference, also update the code that locates special token positions (e.g., mask token index) in the encoded output. Extract and pass the correct position index to the model. Verify the returned index is the expected type (scalar vs. list) to avoid shape 
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.73480 → 0.80527 (higher is better; improved by 0.07047)
- expert 55621328 · learning · v34→v36   Ensure the model's vocab_size config parameter matches the tokenizer length, and call the embedding-resize method after model instantiation but before loading the checkpoint weights. If unsure whether resizing is needed, temporarily disable it to check for errors, then re-enable with the correct voc
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.81031 (higher is better)
- expert 55621328 · learning · v69→v71   Always update the pretrained model path to match the architecture size of the fine-tuned checkpoint. Treat the checkpoint file and the pretrained backbone path as a coupled pair that must be changed together.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ Predictions or new features no longer match the original sample identifiers or column order.
    leaderboard score 0.81872 → 0.82319 (higher is better; improved by 0.00447)
- expert 55621328 · learning · v98→v102   First do a quick sanity check by running the new checkpoints through an existing script with minimal path changes. If results are poor or the run fails, write a dedicated inference script that handles the new variant's specific preprocessing (tokenization, padding/bucketing, embedding resizing). The
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.82066 → 0.82366 (higher is better; improved by 0.00300)
- expert 55621328 · learning · v107→v108   Do not override vocabulary size unless there is clear evidence of a mismatch (e.g., a runtime error). If you override it and the score drops substantially, revert immediately — the checkpoint's saved config almost certainly already encodes the correct vocabulary size.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score n/a → 0.81837 (higher is better)
- expert 55621328 · learning · v109→v111   Treat major inference pipeline changes (new tokenizer vocabulary, new special tokens, new model wrapper) as high-risk. Submit them only after verifying on a local validation set that predictions are reasonable. If the score drops sharply, revert to the known-good pipeline before trying incremental f
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.82798 → 0.80843 (higher is better; worse by 0.01955)
- expert 55621328 · learning · v111→v113   Explicitly override architecture-critical parameters at inference time to match the settings used during training. Check output dimensionality, optional module flags, and any parameter that changes the model graph. Verify by confirming the run completes and produces plausible outputs before submitti
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.80843 → 0.82329 (higher is better; improved by 0.01487)
- expert 55621328 · learning · v117→v119   First load with strict mode enabled to identify exactly which keys are missing or unexpected. If the mismatched keys are auxiliary (e.g., an extra loss head not needed at inference), switch to non-strict loading so the matched weights are used and unmatched ones are ignored. Verify that the resultin
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score n/a → 0.82840 (higher is better)
- expert 55621328 · learning · v115→v117   When swapping in a checkpoint from a different training run, also update the import path or installed package version to match the code that produced that checkpoint. Verify that config files, tokenizer vocabulary, and model class definitions are all consistent before running inference.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.80119 → n/a (higher is better)
- expert 15082684 · ranzcr · v16→v18   Audit every preprocessing step—resolution, cropping, normalization mean/std, interpolation mode—and ensure inference exactly mirrors training. Prioritize resolution and normalization statistics, as these are the most common sources of silent mismatch.
    evidence: ✗ Predictions or new features no longer match the original sample identifiers or column order. | ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.95870 → 0.96509 (higher is better; improved by 0.00639)
- expert 15082684 · ranzcr · v22→v23   Before loading, iterate over the state_dict and strip the wrapper prefix from each key using string manipulation, then load the cleaned dict. Also set the map_location to the target device to avoid device-mismatch errors.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.96591 → n/a (higher is better)
- expert 15164527 · ranzcr · v1→v2   Verify that every submodule's attribute name in the class definition exactly matches the name used in forward(), in checkpoint state-dict keys, and in any layer-replacement code. Print or diff the model's state_dict keys against the checkpoint keys to catch mismatches.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score n/a → n/a (higher is better)
- expert 15173072 · ranzcr · v7→v8   Check that (1) the model is set to evaluation mode so dropout and batch-norm behave correctly, and (2) the checkpoint file actually matches the model architecture being constructed. Fix both before investigating other issues.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.50990 → 0.55637 (higher is better; improved by 0.04647)
- expert 13521245 · ranzcr · v1→v2   Ensure the input preprocessing (especially image resolution and normalization) exactly matches what the checkpoint was trained with. A mismatch between the model's expected input size and the actual test-image size can depress the score far more than the choice of augmentation or caching strategy. V
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.80492 (higher is better)
- expert 13521245 · ranzcr · v12→v13   Read the expected spatial dimensions directly from the model's input tensor shape and use that to set the image decoding/resizing target, rather than maintaining a separate hardcoded resolution variable.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.81275 → 0.83623 (higher is better; improved by 0.02348)
- expert 13521245 · ranzcr · v11→v14   Before removing a custom model package, verify that the replacement loader reconstructs an identical architecture and that all saved weights are restored (check for warnings or layer-count mismatches). If weights don't transfer, retrain or keep the original package rather than expecting a pure infra
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.94487 → 0.77458 (higher is better; worse by 0.17029)
- expert 13702907 · ranzcr · v5→v6   Audit the full pipeline to ensure the image dimensions in the data-loading/decoding step and the model input-shape specification both match the resolution used during training. A single index or variable mismatch can cause a significant score drop without raising any runtime error.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration.
    leaderboard score n/a → 0.95131 (higher is better)
- expert 13702907 · ranzcr · v17→v19   When inference must run under a specific device strategy, prefer recreating the model architecture inside that strategy's scope and loading only the weights, rather than deserializing the full model from a saved file. Test both paths and verify outputs before submitting.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.95232 → 0.95256 (higher is better; improved by 0.00024)
- expert 13702907 · ranzcr · v23→v25   Test both approaches and compare outputs. If scores differ, suspect an architecture mismatch (e.g., different dropout mode, layer configuration) rather than a fundamental difference in the loading method. Prefer the approach where the architecture definition is explicitly controlled in code, as it i
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.95237 → 0.95228 (higher is better; worse by 0.00009)
- expert 50496431 · hms · v11→v12   Store checkpoints in per-model directories and discover them programmatically (e.g., list all files matching a pattern in the directory). This ensures all trained folds are included automatically and reduces copy-paste errors when updating the ensemble.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.37435 → 0.36527 (lower is better; improved by 0.00907)
- expert 50496431 · hms · v65→v68   Enable strict checkpoint loading to catch architecture-checkpoint mismatches immediately. Verify that all model constructor parameters (input dimensions, depth, temporal length) match the training configuration exactly. Fix these before adjusting batch size or other inference settings. A catastrophi
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✓ A traceback identifies an import, callback signature, dataframe operation or device mismatch. | ✓ No end-to-end run has yet produced a verified prediction file.
    leaderboard score n/a → 0.30784 (lower is better)
- expert 50496431 · hms · v79→v80   Always use strict weight loading (exact key matching) after any architecture change. If it raises an error, the checkpoint is incompatible and must be retrained or the architecture reverted. This prevents silent degradation from partially loaded weights.
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration.
    leaderboard score n/a → 0.29794 (lower is better)
- expert 50496431 · hms · v82→v84   Keep inference-time preprocessing identical to training-time preprocessing. When refactoring (removing duplicates, reordering, parameterizing), verify that the actual numerical output of the pipeline remains unchanged before submitting. Any mismatch between training and inference preprocessing will 
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file.
    leaderboard score 0.27938 → 0.30215 (lower is better; worse by 0.02277)
- expert 50496431 · hms · v195→v199   Avoid modifying feature-extraction or normalization parameters at inference time without retraining the model on identically processed data. Even seemingly reasonable adjustments (resolution, scaling) cause large score regressions due to distribution mismatch. If exploration is needed, treat each ch
    evidence: ✓ The checkpoint, tokenizer or preprocessing metadata differs from the instantiated inference configuration. | ✗ No end-to-end run has yet produced a verified prediction file. | ✗ A traceback identifies an import, callback signature, dataframe operation or device mismatch.
    leaderboard score 0.22795 → 0.25381 (lower is better; worse by 0.02586)
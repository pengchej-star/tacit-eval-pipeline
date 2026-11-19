# Restore training-time preprocessing  `T.2.2.3`   21 edits, 0 experts
15 scored cases, median improvement +0.00001, 8 improved


- expert 18851026 (Master) · commonlitreadabilityprize · v7→v8   Extract test embeddings from the same fine-tuned checkpoints used to produce training fold embeddings, ensuring the feature distributions seen by the meta-learner are consistent between train and test. Verify on the leaderboard that the change does not regress, since subtle differences in extraction
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✓ The variable feeding a downstream stage references the wrong version of the data (e.g., raw vs. preprocessed, or vice versa).
    leaderboard score n/a → 0.45924
- expert 75145694 (Expert) · equity · v16→v17   Replicate the exact preprocessing pipeline (imputer, scaler) used during training, create a dedicated inference branch for the new model, and add verbose logging that prints input shapes, loaded model details, and output statistics. Verify these logs before trusting the blended result. This catches 
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✓ An indentation or scoping bug causes a critical statement (e.g., predict call) to execute outside its intended conditional or loop block.
    leaderboard score 0.68867 → 0.69070 (+0.00203)
- expert 75145694 (Expert) · equity · v59→v60   Create a dedicated feature-preparation function for each model that replicates the exact preprocessing used during that model's training (specific imputation, encoding, derived features). Route inference through the correct function based on model identity. This avoids cross-contamination of preproc
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score 0.69324 → 0.69325 (+0.00001)
- expert 53424936 (Master) · hms · v17→v20   When a complex model underperforms expectations at inference, systematically check for data-processing bugs (e.g., features computed using training-only metadata like label offsets that are unavailable at test time). Fix such leaks by using test-compatible defaults, then scale up the fold ensemble a
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✓ A preprocessing or target-building step consumes identifiers or labels unavailable at prediction time. | ✓ Outputs are constant across substantial edits or some configured members never produce predictions. | ✓ Function default arguments or internal references use variable names that were renamed in a prior refactor, causing NameError or silent misuse.
    leaderboard score n/a → 0.22756
- expert 50376011 (Grandmaster) · hms · v20→v21   Write a dedicated inference script that exactly mirrors training: reconstruct the model architecture, restore the full config, load weights with the same utility used during training, run predictions with the same batching and data pipeline, and serialize per-model outputs for downstream ensembling.
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score 0.41352 → 0.39943 (-0.01409)
- expert 50376011 (Grandmaster) · hms · v57→v58   Keep feature extraction parameters (e.g., spectral transform window size, normalization constants) identical between training and inference. If you want to explore a different parameter, retrain the model with that setting. A quick submission test can confirm whether a mismatch exists: if the score 
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score 0.34376 → 0.36034 (+0.01659)
- expert 49524919 (Grandmaster) · hms · v36→v46   Check and fix these in order: (1) ensure the model architecture (layer sizes, branches present/absent, activation functions) exactly matches what was used during training; (2) verify that preprocessing and augmentation flags reference the correct variables; (3) confirm that the post-processing step 
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✓ The variable feeding a downstream stage references the wrong version of the data (e.g., raw vs. preprocessed, or vice versa). | ✓ Function default arguments or internal references use variable names that were renamed in a prior refactor, causing NameError or silent misuse. | ✓ The forward-pass wiring applies an operation (activation, residual, etc.) to the wrong intermediate variable. | ✓ A supposedly behavior-preserving refactor has changed predictions or has not been checked for equivalence. | ✓ A new feature branch receives implausible shapes or values.
    leaderboard score n/a → 0.46059
- expert 49524919 (Grandmaster) · hms · v66→v67   When swapping to a new checkpoint, also update the inference-time transforms (dropout, normalization order, additional augmentations) to match or complement the training regime of that checkpoint. Test the combined change as a single submission; if it beats both the old checkpoint and the new checkp
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score 0.29086 → 0.29040 (-0.00045)
- expert 52551258 (Expert) · hms · v1→v2   Ensure the image resize, normalization, and channel formatting in the inference pipeline exactly match what was used during training. When loading a fine-tuned checkpoint, instantiate the backbone with pretrained=False so the architecture matches the saved weights and no pretrained weights are loade
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✓ The variable feeding a downstream stage references the wrong version of the data (e.g., raw vs. preprocessed, or vice versa).
    leaderboard score n/a → 0.65796
- expert 52551258 (Expert) · hms · v5→v7   When a model swap degrades performance, check that the inference-time preprocessing (filtering, normalization, downsampling) exactly matches what the checkpoint was trained with, and that the output transformation (e.g., softmax vs. log-softmax) is correct. Fix preprocessing alignment before conclud
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score 0.37494 → 0.32513 (-0.04982)
- expert 52551258 (Expert) · hms · v20→v21   Ensure the inference-time feature extraction (spectral transform parameters, normalization, cropping/resizing) exactly matches what was used during training. When the training pipeline is uncertain, try the most likely transform library and parameters, and measure the score change. A large improveme
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score 0.51146 → 0.33979 (-0.17167)
- expert 15082684 (Master) · ranzcr · v16→v18   Audit every preprocessing step—resolution, cropping, normalization mean/std, interpolation mode—and ensure inference exactly mirrors training. Prioritize resolution and normalization statistics, as these are the most common sources of silent mismatch.
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score 0.95870 → 0.96509 (+0.00639)
- expert 13521245 (Grandmaster) · ranzcr · v1→v2   Ensure the input preprocessing (especially image resolution and normalization) exactly matches what the checkpoint was trained with. A mismatch between the model's expected input size and the actual test-image size can depress the score far more than the choice of augmentation or caching strategy. V
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✓ Model or artifact file paths reference an outdated directory that no longer matches the current environment's pretrained-model location.
    leaderboard score n/a → 0.80492
- expert 13521245 (Grandmaster) · ranzcr · v12→v13   Read the expected spatial dimensions directly from the model's input tensor shape and use that to set the image decoding/resizing target, rather than maintaining a separate hardcoded resolution variable.
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score 0.81275 → 0.83623 (+0.02348)
- expert 13702907 (Contributor) · ranzcr · v5→v6   Audit the full pipeline to ensure the image dimensions in the data-loading/decoding step and the model input-shape specification both match the resolution used during training. A single index or variable mismatch can cause a significant score drop without raising any runtime error.
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score n/a → 0.95131
- expert 50496431 (Grandmaster) · hms · v46→v47   Revert the feature addition so the inference input matches the training input exactly. Treat any input-shape or channel change as requiring retrained weights before it can help at inference.
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✓ The inference code contains a duplicated or residual preprocessing/transform step that was not present during training.
    leaderboard score 0.38888 → 0.36464 (-0.02424)
- expert 50496431 (Grandmaster) · hms · v82→v84   Keep inference-time preprocessing identical to training-time preprocessing. When refactoring (removing duplicates, reordering, parameterizing), verify that the actual numerical output of the pipeline remains unchanged before submitting. Any mismatch between training and inference preprocessing will 
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✓ The inference code contains a duplicated or residual preprocessing/transform step that was not present during training.
    leaderboard score 0.27938 → 0.30215 (+0.02277)
- expert 50496431 (Grandmaster) · hms · v93→v95   Keep inference-time preprocessing (filter bands, normalization, clipping) consistent with training-time settings. If you want to test a different preprocessing, retrain models with that setting; changing only inference preprocessing typically degrades scores because the input distribution shifts awa
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score 0.30691 → 0.27954 (-0.02738)
- expert 50496431 (Grandmaster) · hms · v195→v199   Avoid modifying feature-extraction or normalization parameters at inference time without retraining the model on identically processed data. Even seemingly reasonable adjustments (resolution, scaling) cause large score regressions due to distribution mismatch. If exploration is needed, treat each ch
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score 0.22795 → 0.25381 (+0.02586)
- expert 50496431 (Grandmaster) · hms · v202→v204   Do not change spectrogram preprocessing parameters (window size, log transforms, normalization) at inference unless the model is retrained with the new settings. Even small mismatches between training and inference preprocessing cause large score regressions. Test one parameter at a time and revert 
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint. | ✓ A redundant or unintended aggregation step (e.g., unweighted mean) overwrites the intended weighted blend of predictions. | ✓ The inference code contains a duplicated or residual preprocessing/transform step that was not present during training.
    leaderboard score 0.22738 → 0.34797 (+0.12060)
- expert 50496431 (Grandmaster) · hms · v213→v214   Ensure inference DataLoaders use the same batch size as configured/expected. When debugging a score regression caused by multiple simultaneous changes, isolate infrastructure settings (batch size, data loading) as a separate variable—they can have outsized, non-obvious effects on predictions.
    evidence: ✓ Inference transforms or fitted preprocessing objects differ from those used for the checkpoint.
    leaderboard score 0.26971 → 0.22478 (-0.04493)
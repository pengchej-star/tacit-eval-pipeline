# Restore training preprocessing  `T.1.1.2`   27 edits, 0 experts
19 scored cases (improvement signed by each competition's direction), median +0.00504, 13 improved


- expert 18851026 · commonlitreadabilityprize · v7→v8   Extract test embeddings from the same fine-tuned checkpoints used to produce training fold embeddings, ensuring the feature distributions seen by the meta-learner are consistent between train and test. Verify on the leaderboard that the change does not regress, since subtle differences in extraction
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.45924 (lower is better)
- expert 75145694 · equity · v16→v17   Replicate the exact preprocessing pipeline (imputer, scaler) used during training, create a dedicated inference branch for the new model, and add verbose logging that prints input shapes, loaded model details, and output statistics. Verify these logs before trusting the blended result. This catches 
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.68867 → 0.69070 (higher is better; improved by 0.00203)
- expert 75145694 · equity · v59→v60   Create a dedicated feature-preparation function for each model that replicates the exact preprocessing used during that model's training (specific imputation, encoding, derived features). Route inference through the correct function based on model identity. This avoids cross-contamination of preproc
    evidence: ✗ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ The same raw example produces different training and inference features.
    leaderboard score 0.69324 → 0.69325 (higher is better; improved by 0.00001)
- expert 53424936 · hms · v17→v20   When a complex model underperforms expectations at inference, systematically check for data-processing bugs (e.g., features computed using training-only metadata like label offsets that are unavailable at test time). Fix such leaks by using test-compatible defaults, then scale up the fold ensemble a
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.22756 (lower is better)
- expert 53424936 · hms · v19→v20   Audit every preprocessing function for dependencies on label-derived quantities. Replace any such dependency with a test-compatible default (e.g., a fixed canonical offset). After fixing, verify the score recovers or improves beyond the simpler baseline.
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.22756 (lower is better)
- expert 50376011 · hms · v20→v21   Write a dedicated inference script that exactly mirrors training: reconstruct the model architecture, restore the full config, load weights with the same utility used during training, run predictions with the same batching and data pipeline, and serialize per-model outputs for downstream ensembling.
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.41352 → 0.39943 (lower is better; improved by 0.01409)
- expert 50376011 · hms · v57→v58   Keep feature extraction parameters (e.g., spectral transform window size, normalization constants) identical between training and inference. If you want to explore a different parameter, retrain the model with that setting. A quick submission test can confirm whether a mismatch exists: if the score 
    evidence: ✓ The same raw example produces different training and inference features.
    leaderboard score 0.34376 → 0.36034 (lower is better; worse by 0.01659)
- expert 49524919 · hms · v29→v34   When introducing a new preprocessing branch, audit every function call and variable reference in the inference loop to ensure it uses the new branch's transforms, normalization, and imputation—not the old ones. Specifically check: (1) the correct transform/augmentation object is called, (2) missing-
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.55426 (lower is better)
- expert 49524919 · hms · v90→v92   Focus first on the data preprocessing and augmentation code rather than the model definitions. Check that transform function signatures, tensor shapes, and scaling conventions match what the pretrained models expect. Fix those issues in a minimal follow-up commit and verify recovery before iterating
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.26809 → 0.36298 (lower is better; worse by 0.09489)
- expert 52551258 · hms · v1→v2   Ensure the image resize, normalization, and channel formatting in the inference pipeline exactly match what was used during training. When loading a fine-tuned checkpoint, instantiate the backbone with pretrained=False so the architecture matches the saved weights and no pretrained weights are loade
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.65796 (lower is better)
- expert 52551258 · hms · v5→v7   When a model swap degrades performance, check that the inference-time preprocessing (filtering, normalization, downsampling) exactly matches what the checkpoint was trained with, and that the output transformation (e.g., softmax vs. log-softmax) is correct. Fix preprocessing alignment before conclud
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.37494 → 0.32513 (lower is better; improved by 0.04982)
- expert 52551258 · hms · v20→v21   Ensure the inference-time feature extraction (spectral transform parameters, normalization, cropping/resizing) exactly matches what was used during training. When the training pipeline is uncertain, try the most likely transform library and parameters, and measure the score change. A large improveme
    evidence: ✓ The same raw example produces different training and inference features.
    leaderboard score 0.51146 → 0.33979 (lower is better; improved by 0.17167)
- expert 52200959 · hms · v31→v32   Before retraining, audit the inference pipeline: verify the pretrained weight source is the best available, ensure input channel counts and feature mappings match what the weights expect, remove dead code that might introduce side effects, and confirm memory is properly managed between folds. Swappi
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.38167 → 0.33165 (lower is better; improved by 0.05002)
- expert 55621328 · learning · v104→v105   Apply the same text normalization at inference time that was used during training, and use the corresponding checkpoints. This ensures the tokenizer sees the same character distributions it was fine-tuned on. Verify with a leaderboard or validation check that the alignment improves the score.
    evidence: ✓ The same raw example produces different training and inference features.
    leaderboard score 0.82726 → 0.82994 (higher is better; improved by 0.00268)
- expert 55621328 · learning · v145→v146   Create a dedicated inference script per experiment variant that exactly replicates the training-time tokenizer setup (including any added tokens), text preprocessing, and model architecture. Keep checkpoint paths and blending weights as CLI arguments for flexibility, but hard-code the tokenizer and 
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.81937 → 0.82442 (higher is better; improved by 0.00504)
- expert 15082684 · ranzcr · v16→v18   Audit every preprocessing step—resolution, cropping, normalization mean/std, interpolation mode—and ensure inference exactly mirrors training. Prioritize resolution and normalization statistics, as these are the most common sources of silent mismatch.
    evidence: ✓ The same raw example produces different training and inference features. | ✗ Strict loading reports missing keys or incompatible tensor dimensions. | ✗ Sample keys or ordered feature names disagree across arrays being combined.
    leaderboard score 0.95870 → 0.96509 (higher is better; improved by 0.00639)
- expert 15173072 · ranzcr · v15→v21   Default to the canonical normalization statistics for the pretraining dataset (e.g., the dataset-wide mean/std the model was trained with). Deviating from these values almost always hurts because the model's learned features expect a specific input distribution. If the exact training stats are unkno
    evidence: ✓ The same raw example produces different training and inference features. | ✗ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score n/a → 0.95243 (higher is better)
- expert 15173072 · ranzcr · v21→v28   Always use the exact normalization mean and standard deviation that the pretrained backbone was originally trained with. Do not guess or hand-tune these values; mismatched normalization silently degrades predictions even when the model otherwise loads correctly.
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts. | ✗ Strict loading reports missing keys or incompatible tensor dimensions.
    leaderboard score 0.95243 → 0.96462 (higher is better; improved by 0.01220)
- expert 13521245 · ranzcr · v1→v2   Ensure the input preprocessing (especially image resolution and normalization) exactly matches what the checkpoint was trained with. A mismatch between the model's expected input size and the actual test-image size can depress the score far more than the choice of augmentation or caching strategy. V
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.80492 (higher is better)
- expert 13521245 · ranzcr · v12→v13   Read the expected spatial dimensions directly from the model's input tensor shape and use that to set the image decoding/resizing target, rather than maintaining a separate hardcoded resolution variable.
    evidence: ✓ The same raw example produces different training and inference features.
    leaderboard score 0.81275 → 0.83623 (higher is better; improved by 0.02348)
- expert 13702907 · ranzcr · v5→v6   Audit the full pipeline to ensure the image dimensions in the data-loading/decoding step and the model input-shape specification both match the resolution used during training. A single index or variable mismatch can cause a significant score drop without raising any runtime error.
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score n/a → 0.95131 (higher is better)
- expert 50496431 · hms · v46→v47   Revert the feature addition so the inference input matches the training input exactly. Treat any input-shape or channel change as requiring retrained weights before it can help at inference.
    evidence: ✗ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.38888 → 0.36464 (lower is better; improved by 0.02424)
- expert 50496431 · hms · v82→v84   Keep inference-time preprocessing identical to training-time preprocessing. When refactoring (removing duplicates, reordering, parameterizing), verify that the actual numerical output of the pipeline remains unchanged before submitting. Any mismatch between training and inference preprocessing will 
    evidence: ✓ The same raw example produces different training and inference features. | ✗ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.27938 → 0.30215 (lower is better; worse by 0.02277)
- expert 50496431 · hms · v93→v95   Keep inference-time preprocessing (filter bands, normalization, clipping) consistent with training-time settings. If you want to test a different preprocessing, retrain models with that setting; changing only inference preprocessing typically degrades scores because the input distribution shifts awa
    evidence: ✗ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.30691 → 0.27954 (lower is better; improved by 0.02738)
- expert 50496431 · hms · v195→v199   Avoid modifying feature-extraction or normalization parameters at inference time without retraining the model on identically processed data. Even seemingly reasonable adjustments (resolution, scaling) cause large score regressions due to distribution mismatch. If exploration is needed, treat each ch
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.22795 → 0.25381 (lower is better; worse by 0.02586)
- expert 50496431 · hms · v202→v204   Do not change spectrogram preprocessing parameters (window size, log transforms, normalization) at inference unless the model is retrained with the new settings. Even small mismatches between training and inference preprocessing cause large score regressions. Test one parameter at a time and revert 
    evidence: ✓ The same raw example produces different training and inference features. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.22738 → 0.34797 (lower is better; worse by 0.12060)
- expert 50496431 · hms · v206→v208   When experimenting with input normalization at inference, keep changes small and consistent with training preprocessing. If a normalization change (e.g., switching from linear scaling to log scaling) causes a large score regression, revert immediately rather than trying to tune it further, because t
    evidence: ✓ The same raw example produces different training and inference features. | ✗ Strict loading reports missing keys or incompatible tensor dimensions. | ✓ A stage consumes a stale variable, wrong split, or unexpected shape despite compatible artifacts.
    leaderboard score 0.22628 → 0.25986 (lower is better; worse by 0.03359)
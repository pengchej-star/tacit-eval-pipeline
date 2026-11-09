# Current version and earlier versions

Current version: **v2**, leaderboard score 0.94363 (higher is better).

## Earlier versions (oldest first; goal of the change, summary of the change, score the version reached)
v1 -> v2: Refactor the notebook into a clean inference pipeline (build tf.data input, adjust input size and batch size), remove duplicate/training/CV cells, and prepare submission — improving inference consistency and score. | change: Removed duplicated cells and unused imports (PIL, keras.preprocessing.image), set WORK_DIR and wired up train/test paths, added exploratory label plots and sample image display, centralized main parameters (BATCH_SIZE, TARGET_SIZE, EPOCHS) and made b | score after: 0.94363 (+0.00226)

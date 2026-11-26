# Kaggle Competition Run

You are running unattended for **{{MINUTES}} minutes** on **{{COMP}}**. Nobody will answer questions. Decide and proceed.

## Environment
- **Data** (already prepared, read-only): `/kaggle/input/{{COMP}}` — inspect it yourself (`ls /kaggle/input/{{COMP}}`). The layout varies by competition but always includes `sample_submission.csv`, which defines the required output format, and `description.md`, the competition's description and metric ({{DIRECTION}}).
- **Working directory**: `/workspace` — write anything you need here (code, models, notes, intermediate files). `/kaggle/working` is writable too.
- **Final submission**: `/kaggle/working/submission.csv`. It must match `sample_submission.csv` exactly in columns and row count.
- **GPU**: one GPU (`nvidia-smi`). **Python**: `python` has numpy, pandas, scikit-learn, lightgbm, xgboost, catboost, torch (CUDA), timm and transformers. You may download general pretrained weights (e.g. from Hugging Face).
{{GRADER_BLOCK}}
## Goal
Push the score on `{{COMP}}` as high as you can within the time budget. There is always something worth trying next; don't exit voluntarily before the timer ends.

**The task ends ONLY when the {{MINUTES}}-minute wall timer expires.** If your agent framework provides a `finish`, `stop`, `terminate`, `end_task`, or similar tool — **do not call it**. If you think you're done, use the remaining time to try another backbone / more folds / more features / TTA / ensembling. Improving an already-good submission is always a valid next step.

## Rules
- Do not search online for competition-specific solutions, winning notebooks, or leaderboard approaches for `{{COMP}}`. General ML library documentation (PyTorch, sklearn, lightgbm, etc.) is fine.
- The test labels are not available to you; do not try to obtain them.
- Always keep a valid `/kaggle/working/submission.csv` on disk. If something goes wrong mid-run, a previous version is better than nothing.

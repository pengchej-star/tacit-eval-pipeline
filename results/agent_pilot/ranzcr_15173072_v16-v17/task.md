# Task: write the next version of an expert's Kaggle notebook

Competition: RANZCR CLiP — Catheter and Line Position Classification (`ranzcr-clip-catheter-line-classification`). Metric: Macro AUC (multi-label); higher is better.
The competition description is in /kaggle/input/ranzcr-clip-catheter-line-classification/description.md.

/workspace/history/ holds the expert's version history for one notebook:
- v001.py ... v016.py: the code of each saved version (notebook cells separated by `# %%`);
- scores.csv: the Kaggle leaderboard score of each version (empty where the expert did not submit it).

The latest version is v016.py. Write the expert's **next version, v017**: start from v016.py and make the
change you expect to improve the score most, the way this expert would continue.

Environment
- Data: /kaggle/input/ranzcr-clip-catheter-line-classification/ (training data, unlabeled test data, sample_submission.csv). The datasets the expert
  attached (model weights, libraries) are also under /kaggle/input/, at the paths the expert's code uses.
- `python` has PyTorch with one NVIDIA GPU, timm, scikit-learn, pandas, numpy, lightgbm, xgboost and more.
- /kaggle/working/ is the notebook's working directory and scratch space.
- You may run code to test your version. Time budget: about 40 minutes in total, so save a working
  version early and refine it after.

Required output
- /workspace/solution/v017.py: a complete script that runs top to bottom with
  `cd /kaggle/working && python /workspace/solution/v017.py` and writes /kaggle/working/submission.csv in the
  format of sample_submission.csv. It must not need internet.
- /workspace/solution/NOTES.md: two to five sentences on what you changed and why.

It will be scored on held-out test labels that are not available to you. Use only /workspace and /kaggle.

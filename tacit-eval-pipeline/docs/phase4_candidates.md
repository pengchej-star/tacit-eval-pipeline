# Phase 4 prep: candidate cases (not executed yet)

Goal: pick 3–5 expert transitions `(key_id, v_k → v_k+1)` from google-quest-challenge (gquest) and
learning-agency-lab-automated-essay-scoring-2 (aes2) that are easiest to re-run, to test the Phase 4 runner.

## How they were found

`src/propose_cases.py` statically scans every human version with code in the two comps (3,190 versions;
nothing executed) and records:

- `/kaggle/input/<x>` (or `../input/<x>`) folders read. Anything other than the comp's own folder counts as external.
- deep-learning training (backward / optimizer.step / Trainer / keras fit) vs classical fitting (sklearn, LightGBM)
- pretrained-weight loading, GPU use, internet use (pip install, wget, requests, HF hub)
- Kaggle runtime (`running_time_ms` in `trajectory.json`) and Kaggle public score

```bash
python src/propose_cases.py --traceml-dir /data/user_data/pengchej/traceml/hf \
  --human-dir /data/user_data/pengchej/traceml/extracted/human \
  --comps google-quest-challenge learning-agency-lab-automated-essay-scoring-2 \
  --features-out /data/user_data/pengchej/traceml/version_features.csv --top 25
```

| comp | versions with code | no external inputs | no DL training | no external, no internet, no DL |
|---|---:|---:|---:|---:|
| gquest | 923 | 243 | 494 | 188 |
| aes2 | 2,267 | 441 | 943 | 334 |

Most versions in both comps read external Kaggle datasets: pretrained transformers/BERT/USE weights in gquest,
and pre-trained fold models, word lists and pip wheels in aes2. Consecutive pairs where both versions are
Kaggle-scored, the code changed, and neither reads external inputs or the internet: **139** (aes2 108, gquest 31).
They were ranked by: no DL training > no GPU > no pretrained weights > short Kaggle runtime > short code.
I then **read the code of the top pairs by hand**; the caveats below come from that reading, not from the regexes.

## Proposed cases, easiest first

Scores are Kaggle public-leaderboard scores (not comparable to MLE-bench; see `dataset_notes.md` §5).
Runtimes are Kaggle's, in minutes.

| # | comp | key_id (author tier) | v_k → v_k+1 | Kaggle score | Kaggle runtime | code lines | what changed |
|---|---|---|---|---|---|---|---|
| 1 | aes2 | 55844901 (Contributor) | v1 → v2 | 0.674 → 0.696 | 0.5 / 0.8 | 34 / 39 | essay-length-only GradientBoosting → length + TF-IDF features with LightGBM |
| 2 | aes2 | 55822700 (Grandmaster) | v12 → v13 | 0.704 → 0.711 | 0.4 / 0.4 | 75 / 76 | bug fix: the "unique words" feature was computed with the sentence counter |
| 3 | aes2 | 54532847 (Master) | v6 → v7 | 0.482 → 0.556 | 1.1 / 1.3 | 70 / 70 | TF-IDF (1–3-grams) + SGD: stop-word removal turned off |
| 4 | gquest | 6732618 (Master) | v4 → v5 | 0.263 → 0.297 | 2.9 / 3.2 | 138 / 176 | TF-IDF+SVD features, small PyTorch MLP: single holdout → 5-fold CV ensemble with early stopping, smaller net |
| 5 | aes2 | 55286319 (Contributor) | v10 → v11 | 0.734 → 0.740 | 0.9 / 1.4 | 201 / 202 | TF-IDF + hand-crafted features + LogisticRegression: adds an essay-length feature |

All five read only the competition's own `train.csv` / `test.csv` / `sample_submission.csv`, write
`submission.csv` to the working directory, use no pretrained weights, no GPU, and no internet.

### Why each, and what to watch for

1. **aes2 55844901 v1 → v2: best first case.** Tiny, deterministic (LightGBM's default seed; v1's
   GradientBoosting runs on a single feature), only `lightgbm`, `scikit-learn` and `scipy` needed. A real
   modelling change, with a +0.022 Kaggle gain we can check for in our environment. The notebook starts with
   `%%capture`, an IPython magic, so it must run under `ipython`, not plain `python`.
2. **aes2 55822700 v12 → v13: deterministic, Grandmaster, and a nice "tacit" edit.** A one-line bug fix in a
   feature function. Fixed seed (`random_state=42`), LightGBM + CountVectorizer. The Kaggle gain is small
   (+0.007), but both versions are deterministic, so even a small difference is a real signal. v12 still runs:
   its broken helper `split('')` is defined but never called.
3. **aes2 54532847 v6 → v7: biggest gain (+0.074) from a one-line edit.** Plain sklearn. Caveat: SGDClassifier
   has no `random_state`, so the score will vary a bit from run to run (should be fine against a 0.07 gap).
   Uses `%%time` and `display`, so it also needs `ipython`.
4. **gquest 6732618 v4 → v5: the only realistic, easy gquest case.** The easy gquest kernels without DL score
   ≤ 0.14 on Kaggle (kernel 7676170), or ~0 (6820936, which submits random "naive" predictions sampled from the
   label distribution). This one scores 0.26–0.31,
   trains a small MLP on CPU and needs `torch` (CPU) and `category_encoders`. **Two problems:**
   - v5 calls `KFold(n_splits=5, random_state=42)` without `shuffle=True`. This raises `ValueError` on
     scikit-learn ≥ 0.24 (checked on our 1.9.1). Old scikit-learn has no Python 3.11 wheels, so v5 will need a
     one-line compatibility patch (drop `random_state`, which changes nothing because the split is unshuffled).
     The runner should apply such patches openly and log them.
   - torch is not seeded, so expect some noise.
5. **aes2 55286319 v10 → v11: works but noisy.** `train_test_split` without a seed, so the 0.006 Kaggle gain
   is probably within run-to-run noise. Needs `polars`. Keep as a backup.

Backup gquest case, not recommended: 7676170 v9 → v10 (CountVectorizer 200 → 40 features, 0.056 → 0.100).
It has the same `KFold` problem, needs NLTK stopwords downloaded ahead of time, and fits a *separate*
vectorizer on the test set. So its features don't line up and its scores are close to noise.

## Implications for the runner (Phase 4)

- Run converted notebooks with `ipython` (cell magics such as `%%capture` and `%%time` appear even in simple
  kernels).
- Use a separate runtime env with the Kaggle-ish stack these need: `lightgbm`, `torch` (CPU is enough here),
  `category_encoders`, `polars`, `nltk` (+ stopwords). None are in `tacit-eval` today.
- Notebooks use both `/kaggle/input/<slug>/...` and `../input/<slug>/...`, and write `submission.csv` to the
  current directory. So the working dir should be `kaggle/working` with `../input` → `kaggle/input`.
- The code is 2019–2024 code running on a 2026 stack. Expect API breaks (the `KFold` case above); log every
  compatibility patch.
- Re-run each version more than once where the code is unseeded, to measure noise before comparing v_k and v_k+1.

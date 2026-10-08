# Phase 4: expert-version runner, first runs

Run on 2026-10-08 on Babel CPU node `babel-l5-20` (8 CPUs). Cases #1 and #2 from `phase4_candidates.md`.

## Setup

- **Run env `kaggle-run`** (Python 3.11.17, `/data/user_data/pengchej/software/anaconda3/envs/kaggle-run`).
  Exact versions in `env/kaggle-run.txt`. Main packages: numpy 2.4.6, pandas 3.0.6, scikit-learn 1.9.1,
  lightgbm 4.7.0, xgboost 3.2.0, catboost 1.2.10, polars 2.0.0, torch 2.14.1+cpu, transformers 5.19.0,
  papermill 2.7.0. NLTK stopwords/punkt/wordnet are downloaded into the env. The env has a Jupyter kernel
  named `kaggle-run`.
- **Runner `src/run_version.py`.** It runs in the `tacit-eval` env, because grading needs mlebench, and
  executes the notebook in `kaggle-run` via papermill.

```bash
conda activate tacit-eval
python src/run_version.py --comp learning-agency-lab-automated-essay-scoring-2 --key-id 55844901 --version 1 --timeout 1800
```

Per run it creates `/data/user_data/pengchej/runs/<comp>__<key_id>_vNNN__<timestamp>/`:

```
original.ipynb      the version exactly as in the TraceML tarball
notebook.ipynb      after path rewriting (+ patches, if any): this is what was executed
executed.ipynb      with all cell outputs, for debugging
run.log             papermill log (cell-by-cell, with cell output)
kaggle/input/<comp>/    read-only copies of prepared/public/* (prepared/private is never copied)
kaggle/working/         cwd of the notebook; submission.csv is picked up here
```

and appends a row to `results/runs.jsonl`:
`run_id, timestamp, comp, key_id, version, code_file, status, score, kaggle_score, above_median, runtime_s,
patches_applied, path_rewrites, submission, workdir, host, run_env, error_tail`.
`status` is one of `OK, EXEC_FAILED, TIMEOUT, NO_SUBMISSION, INVALID_SUBMISSION, GRADE_FAILED`. A
notebook that raises an error is not graded, as on Kaggle.

## Results

| case | key_id | version | status | MLE-bench score (ours) | Kaggle public score | runtime (s) | Kaggle runtime (s) | patches |
|---|---|---|---|---:|---:|---:|---:|---|
| #1 | 55844901 | v1 | OK | 0.5992 | 0.6742 | 8.3 | 28 | none |
| #1 | 55844901 | v2 | OK | **0.6640** | 0.6957 | 10.6 | 46 | none |
| #2 | 55822700 | v12 | OK | 0.6613 | 0.7043 | 3.5 | 25 | none |
| #2 | 55822700 | v13 | OK | **0.6673** | 0.7114 | 4.0 | 22 | none |

Metric: quadratic weighted kappa, higher is better. Runtime includes kernel start-up but not grading.

- **Direction matches Kaggle in both cases.** #1 improves by +0.065 here vs +0.022 on Kaggle; #2 improves by
  +0.006 here vs +0.007 on Kaggle.
- **Deterministic.** All 4 versions were run a second time (into a scratch results file, not
  `runs.jsonl`). The scores were identical, and for 55822700 v13 the `submission.csv` was byte-identical.
  So the small +0.006 in #2 is a real effect of the edit, not noise.
- **Our scores are lower than Kaggle's** (by 0.03–0.08). That is expected and not a bug: a different test set
  (MLE-bench's 1,731 essays held out of train vs Kaggle's ~8k hidden essays), ~10% less training data, and
  newer library versions.
- **Checks.** Every submission has 1,731 rows with real predictions (score spread over 1–6, not the constant
  sample submission). The executed notebooks have no errors. The only warning is LightGBM's harmless
  "Converting data to scipy sparse matrix" (55844901 v2).
- **No compatibility patches** were needed. Only `/kaggle/input/...` paths were rewritten (2–3 per notebook).

## Known limitations

- **The isolation is by construction, not a sandbox.** The notebook only sees copies of `prepared/public`,
  and nothing in its paths or environment points at the cache. But it runs as our user, so code that
  deliberately opened `/data/user_data/pengchej/mlebench-cache/<comp>/prepared/private` could read it. That
  is fine for expert notebooks. For agent-edited code we should add a container (e.g. Apptainer, binding
  only the workdir) or a permission split.
- `prepared/public/description.md` (an MLE-bench file, not on Kaggle) is also copied into `kaggle/input`.
- The run env is a 2026 stack. These two 2024 notebooks ran unchanged, but older code (e.g. 2019 gquest
  kernels) will need compat patches (see `phase4_candidates.md`). The runner has an opt-in `--patch`
  registry for that (one patch so far: `kfold_random_state_without_shuffle`), and every patch applied is
  recorded in `patches_applied`.
- Inputs are copied per run (~36 MB for aes2). For hms/ranzcr (13–26 GB) this should switch to hardlinks.

# Phase 5: case-level triage

Done 2026-10-08 for the 4 paired comps that have an MLE-bench grader: aes2 (learning-agency-lab-automated-essay-scoring-2),
gquest (google-quest-challenge), hms (hms-harmful-brain-activity-classification) and ranzcr
(ranzcr-clip-catheter-line-classification).

A **case** is one within-kernel transition `(key_id, v_k → v_k+1)`: the `edge_kind == "version"` rows of
TraceML's `data/paired/action.parquet` (human rows only). 5,983 of the 5,988 are consecutive version numbers.
The other 5 skip versions that TraceML filtered out (`adjacent = False` in the CSV). Cross-kernel `fork` and
`code_sim` edges (67) are not cases.

## Files

| file | rows | what |
|---|---:|---|
| `triage/versions.csv` | 6,170 | one row per version: status, reason, and every static flag |
| `triage/cases.csv` | 5,988 | one row per case: worse status of its two versions, reason, Kaggle scores, actions |
| `triage/external_inputs.csv` | 1,057 | one row per (kernel, external `/kaggle/input/<x>` folder): available?, resolved Kaggle ref |

```bash
# as run for the committed CSVs (Kaggle API calls bounded; see "unverified" below)
python src/triage_static.py --no-search --api-budget-min 15 --comps learning-agency-lab-automated-essay-scoring-2 \
    google-quest-challenge hms-harmful-brain-activity-classification ranzcr-clip-catheter-line-classification
python src/validate_easy_sample.py --per-comp learning-agency-lab-automated-essay-scoring-2=8 \
    --per-comp google-quest-challenge=7 --seed 0 --timeout 900 --workers 3
```

The validation was started from an offline (`--no-kaggle`) `cases.csv` while the API run was still going. That
is fine because the EASY label does not depend on the API: a version with any external input is never EASY.
The 340 EASY cases in the committed `cases.csv` are exactly the same set, so `--seed 0` gives the same sample.

## How a version is labelled (static, nothing executed)

Rules are checked in this order, and the first match wins. A case gets the worse label of its two versions.

| status | rule |
|---|---|
| `NO_CODE` | no file in the TraceML tarball (or no code cells) |
| `NON_PYTHON` | notebook language is not Python. None of these 4 comps has one |
| `MISSING_EXTERNAL_INPUT` | reads `/kaggle/input/<x>` or `../input/<x>` with `x` ≠ the competition, and `x` cannot be found or accessed on Kaggle |
| `NEEDS_INTERNET` | `pip install` from PyPI, `wget`/`curl`/`requests`, HF-hub ids in `from_pretrained("org/name")`, `pretrained=True`, `nltk.download`, `torch.hub` |
| `NEEDS_GPU` | `cuda`, `.to("cuda")`, `device="cuda"/"gpu"`, GPU tree methods, CatBoost `task_type="GPU"`, TPU, RAPIDS |
| `NEEDS_TRAINING` | deep-learning training (`.backward()`, `optimizer.step()`, `Trainer`, `model.train()`, `for epoch in …`, Keras `.fit`), or Kaggle runtime > 15 min, or runtime unknown |
| `NEEDS_EXTERNAL_DOWNLOAD` | **(added; not in the brief's list)** every external input exists and is accessible, but has to be downloaded into `kaggle/input` first |
| `EASY` | none of the above: only the competition's data, CPU, Kaggle runtime ≤ 15 min. Classical `.fit` (sklearn, LightGBM, …) is allowed |

The brief's list has no bucket for "uses external inputs that are still downloadable". Lumping those
versions into `MISSING_EXTERNAL_INPUT` would hide the largest group we could unlock next, so they get
`NEEDS_EXTERNAL_DOWNLOAD`.

**Resolving external inputs.** The folder name `x` is the slug without the owner. It is resolved through the
Kaggle API in three steps:
1. the kernel's own metadata (`kernel pull`: the data sources of its latest version);
2. the metadata of all 180 kernels in these comps;
3. an exact-slug search over datasets and kernels.

Each resolved ref is then checked once: dataset file listing, kernel pull, model get, or the competition
download probe. Answers are cached, calls have a hard deadline, and HTTP 429 is retried with backoff.

**Missing inputs are labelled "unverified" when we could not check them.** Kaggle rate-limited us hard
(HTTP 429) on kernel pulls and searches. So the final run used `--no-search --api-budget-min 15`:
- the exact-slug search ran for 150 names (20 found) and was skipped for the remaining ~300;
- access checks stopped after 15 minutes of API time.

A folder name that is not in any kernel's metadata, or whose access was never checked, is labelled
`MISSING_EXTERNAL_INPUT` with `missing_unverified = True` (reason starts with "missing (unverified: …)").
These may in fact still exist publicly. Only rows with `missing_unverified = False` are confirmed misses:
a ref we found but that returns 403/404 (private or deleted), or another competition whose rules we have
not accepted.

**Exact resolution should use Meta Kaggle instead of name search.** Meta Kaggle's `KernelVersionDatasetSources`
table (with `KernelVersionCompetitionSources` / `KernelVersionKernelSources`) gives the exact `owner/dataset`
attached to *each kernel version*. That avoids both the owner-less folder name and the "latest version only"
limit of the kernel metadata, and it needs no per-item API calls. After joining, only the per-ref access check
needs the API.

## Static results

**Versions** (all 6,170 human versions of the 4 comps in the paired split):

| comp | NO_CODE | MISSING_EXTERNAL_INPUT | NEEDS_INTERNET | NEEDS_GPU | NEEDS_TRAINING | NEEDS_EXTERNAL_DOWNLOAD | EASY | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| aes2 | 2 | 1,826 | 138 | 7 | 94 | 0 | 202 | 2,269 |
| gquest | 0 | 611 | 18 | 23 | 197 | 1 | 73 | 923 |
| hms | 0 | 1,991 | 39 | 150 | 75 | 0 | 130 | 2,385 |
| ranzcr | 0 | 515 | 30 | 31 | 16 | 0 | 1 | 593 |
| **total** | 2 | 4,943 | 225 | 211 | 382 | 1 | 406 | 6,170 |

**Cases** (5,988 within-kernel transitions; a case takes the worse of its two versions):

| comp | NO_CODE | MISSING_EXTERNAL_INPUT | NEEDS_INTERNET | NEEDS_GPU | NEEDS_TRAINING | EASY | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| aes2 | 2 | 1,797 | 138 | 7 | 107 | **157** | 2,208 |
| gquest | 0 | 597 | 18 | 21 | 184 | **66** | 886 |
| hms | 0 | 1,958 | 42 | 140 | 70 | **117** | 2,327 |
| ranzcr | 0 | 498 | 28 | 27 | 14 | **0** | 567 |
| **total** | 2 | 4,850 | 226 | 195 | 375 | **340** | 5,988 |

What the numbers say:

- **External inputs dominate.** 5,086 of 6,168 versions with code read some `/kaggle/input/<x>` other than the
  competition: pretrained weights, offline pip wheels, other people's pre-trained fold models, word lists.
  A version is labelled by the *first* matching rule, so `MISSING_EXTERNAL_INPUT` hides GPU/training needs.
  The flag columns in `versions.csv` (`gpu`, `dl_train`, `internet`, …) give the full picture: 4,319 versions
  have GPU markers and 3,210 have deep-learning training.
- **`MISSING_EXTERNAL_INPUT` is mostly *unverified*** (4,941 of 4,943 versions):
  - 3,061 versions use at least one folder name we could not resolve to any Kaggle ref (430 unique names, e.g.
    personal checkpoint uploads such as `000-007-512-adam-wr`);
  - 1,882 versions use only refs that *were* found in kernel metadata but whose access check did not fit in
    the API budget. These are likely downloadable. For example, `hideyukizushi/aes2-400-20240419134941` (used
    by 794 aes2 versions) was checked by hand and is accessible.

  Of the 71 refs whose access was actually checked, all 71 were accessible. The only confirmed miss is one
  other competition whose rules we have not accepted (2 versions). So once Meta Kaggle resolution is done, a
  large part of this bucket should move to `NEEDS_EXTERNAL_DOWNLOAD` (or to GPU/training), not stay missing.
- **EASY cases: 340, but concentrated.** They come from 33 kernels (aes2 17, hms 10, gquest 6), and ranzcr has
  none. Only 73 of them have a Kaggle score on both versions (aes2 37, hms 20, gquest 16). hms EASY cases were
  not validated: hms is not prepared yet, and many may be EDA or plotting notebooks.


## Validating the EASY label: does it actually run?

I sampled 15 EASY cases (seed 0): 8 aes2 and 7 gquest, i.e. 27 distinct versions. Each version was executed
with `src/run_version.py` (CPU, 15-min timeout, 3 runs in parallel, tag `phase5_easy_sample`) in two rounds,
both kept in `results/runs.jsonl` with a `run_round` field:

- **r1**: the original `kaggle-run` env. Runs were unpatched; a version failing with exactly the KFold error
  was retried once with that patch (tag `phase5_easy_sample_patched`).
- **r2**: after the env fixes (+`wordcloud`, `pyarrow`, `gensim`, NLTK `punkt_tab`/`punkt`/`stopwords`/
  `wordnet`) and with all known compat patches auto-applied: `kfold_random_state_without_shuffle`,
  `sklearn_get_feature_names_out`, `pandas_applymap_to_map`. These are pure API renames, and each one applied
  is recorded in `patches_applied`. Same seed, so the same 15 cases.

The sample is clustered because EASY cases are: the 7 gquest cases come from only 2 kernels (6858560, 7676170),
and 4 of the 8 aes2 cases come from kernel 56245635.

| | r1 as-is | r1 + KFold patch retry | **r2** (env fixes + auto patches) |
|---|---:|---:|---:|
| versions OK (of 27) | 2 (7%) | 4 (15%) | **13 (48%)** |
| cases with both versions OK (of 15) | 0 | 1 | **5 (33%)** |

In r2, 9 of the 13 OK versions needed a compat patch: all 8 gquest 7676170 versions (KFold, plus
`get_feature_names` from v12 on), and aes2 55144245 v26 (`applymap`). The 5 cases that ran:
- gquest 7676170 v6→v7, v12→v13, v16→v17, v24→v25;
- aes2 54551628 v22→v23.

Two caveats on the r2 OK runs:
- **aes2 54551628 v22 ran, but its predictions are near-uniform over 1–6** (QWK 0.013 here, 0.0 on Kaggle). It
  is a placeholder version, so this case is not a meaningful before/after pair.
- **aes2 56245635 v3 scored 0.642 in r1 and 0.628 in r2.** The notebook is not deterministic, so single runs of
  it are noisy.

**Failure causes.** r1 = first attempt, 25 failed versions; r2 = 14 failed versions.

| cause | r1 | r2 | details |
|---|---:|---:|---|
| package missing from our env | 12 | 5 | r1: `wordcloud` ×9, `pyarrow` ×2, `gensim` ×1 (all fixed). r2: gquest 6858560 now stops at `pyLDAvis`. Its next import is Keras, and the env has no TensorFlow/Keras at all |
| library API removed in the 2026 stack | 10 | 4 | r1: `get_feature_names` ×6, `KFold(random_state)` ×2, `applymap` ×2 (all fixed by patches). r2: aes2 56245635 v4/v12/v13/v14 fail in an EDA plot: newer seaborn/matplotlib reject the `kde=` keyword |
| NLTK data missing | 2 | 0 | `punkt_tab` (fixed) |
| out of memory | 0 | 2 | aes2 54081903 v26/v27 (polars feature engineering). The kernel was killed by the 32 GB job limit (cgroup `oom_kill` = 2) while 3 runs shared the node. In r1 these failed earlier, on `pyarrow` |
| timeout (15 min) | 0 | 1 | aes2 54826193 v3 (Kaggle runtime 3.8 min). In r1 it failed earlier, on NLTK data |
| bug in the notebook itself | 1 | 2 | aes2 56245635 v2 (`test` undefined) and 55144245 v25 (drops a missing `score` column). Neither has a Kaggle score; v26 of 55144245 runs fine |

**How accurate was the static label?**

- **What it checks held in both rounds.** No failure came from an external input, a GPU, or the internet.
  The r2 timeout and OOM are about our CPU/memory budget (3 parallel runs on a 32 GB job), not hidden GPU
  or training needs.
- **"EASY" still does not mean "runs as-is".** It means "no blocker the static scan can see". Fixing the env
  and adding three rename patches took the sample from 2/27 to 13/27 versions (0/15 → 5/15 cases). Every fix
  exposed the next problem, e.g. `wordcloud` → `pyLDAvis` → Keras, or `pyarrow` → OOM.
- **What is left:**
  - EDA/plotting code written for older seaborn/matplotlib (4);
  - packages we still lack: `pyLDAvis`, TensorFlow/Keras (5);
  - memory/time limits with parallel runs (3);
  - real bugs in unscored versions (2).

  Plot-only failures would be avoided by stubbing plotting, but that changes the notebook, so it was not done.
- **Requiring a Kaggle score helps.** Both genuine code bugs were in versions without a Kaggle score. A
  Kaggle-scored version ran end to end on Kaggle. `cases.csv` has `both_kaggle_scored` to filter on.
- gquest 6858560 also hard-codes Kaggle's train size (`train[...].sample(6079)`; MLE-bench train has 5,471
  rows), so it would fail later even with every package installed.

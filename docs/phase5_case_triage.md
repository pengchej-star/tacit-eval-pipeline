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
python src/triage_static.py --comps learning-agency-lab-automated-essay-scoring-2 google-quest-challenge \
    hms-harmful-brain-activity-classification ranzcr-clip-catheter-line-classification
python src/validate_easy_sample.py --cases <cases.csv> --per-comp learning-agency-lab-automated-essay-scoring-2=8 \
    --per-comp google-quest-challenge=7 --seed 0 --timeout 900 --workers 3
```

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
with `src/run_version.py` (CPU, 15-min timeout, tag `phase5_easy_sample` in `results/runs.jsonl`). Failures
were **not fixed**. The one exception is the existing opt-in patch `kfold_random_state_without_shuffle`: a
version failing with exactly that error was re-run once with it (tag `phase5_easy_sample_patched`).

The sample is clustered because EASY cases are: the 7 gquest cases come from only 2 kernels (6858560, 7676170),
and 4 of the 8 aes2 cases come from kernel 56245635.

| | ran as-is | ran with the existing patch |
|---|---:|---:|
| versions (27) | **2** (7%) | 4 (15%) |
| cases, both versions OK (15) | **0** | 1 (gquest 7676170 v6→v7) |

Versions that ran: aes2 54551628 v23 (QWK 0.726, 237 s), aes2 56245635 v3 (0.642, 82 s), and with the patch
gquest 7676170 v6 (0.098) and v7 (0.094), about 10 s each. All took far less than 15 min.

**Failure causes** (first attempt, 25 failed versions):

| cause | versions | details |
|---|---:|---|
| package missing from our `kaggle-run` env | 12 | `wordcloud` ×9 (used only for EDA word-cloud plots), `pyarrow` ×2 (needed by polars `.to_pandas()`), `gensim` ×1 |
| library API removed in the 2026 stack | 10 | scikit-learn `CountVectorizer.get_feature_names()` ×6 (removed in 1.2), `KFold(random_state=…)` without shuffle ×2 (fixed by the existing patch), pandas `DataFrame.applymap` ×2 (removed in pandas 3) |
| NLTK data missing | 2 | NLTK ≥ 3.9 needs `punkt_tab`; the env only has `punkt` |
| bug in the notebook itself | 1 | aes2 56245635 v2 uses `test` but defines `test_data`. This version has no Kaggle score, so it most likely failed on Kaggle too |

**How accurate was the static label?**

- **What it claims held for all 27 versions.** No failure came from an external input, a GPU, the internet, or
  a timeout.
- **"EASY" does not mean "runs as-is".** Only 2 of 27 versions (0 of 15 cases) ran unchanged, because the
  static scan does not check (a) whether every imported package and data file exists in our env, or (b) API
  breakage between the notebook's era and our 2026 stack.
- **Most failures look cheap to remove**, but per the brief none of these fixes were tried:
  - add `wordcloud`, `gensim`, `pyarrow` and NLTK `punkt_tab` to the env (14 of 25 failures);
  - add two more recorded compat patches, `get_feature_names` → `get_feature_names_out` and
    `applymap` → `map` (8 more).

  Those versions might still fail later in the notebook. For example, gquest 6858560 calls
  `train[...].sample(6079)`, hard-coding Kaggle's train size, while MLE-bench's train has 5,471 rows. So it
  would fail even with `wordcloud` installed.
- **Requiring a Kaggle score helps.** A version that was Kaggle-scored ran end to end on Kaggle. The one genuine
  code bug was in an unscored version. `cases.csv` has `both_kaggle_scored` to filter on.

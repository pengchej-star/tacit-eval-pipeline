# Phase 2: competition triage

`triage/competitions.csv` has one row per competition in TraceML's `manifests/competitions.json` (141 rows).
It was generated on 2026-10-08 by:

```bash
python src/triage_competitions.py \
  --traceml-dir /data/user_data/pengchej/traceml/hf \
  --mlebench-dir /data/user_data/pengchej/src/mle-bench \
  --mlebench-cache /data/user_data/pengchej/mlebench-cache \
  --kaggle-cache /data/user_data/pengchej/traceml/kaggle_probe.json \
  --out triage/competitions.csv
```

The Kaggle answers are cached in `kaggle_probe.json`. Rerunning the script reuses them (`--refresh` re-queries).

## Summary

| status | comps | human trajectories | versions with code | meaning |
|---|---:|---:|---:|---|
| `READY` | 2 | 98 | 3,190 | in MLE-bench, prepared, `grade-sample` verified (gquest, aes2) |
| `PREPARABLE` | 2 | 84 | 2,978 | in MLE-bench, rules accepted, download works, not prepared yet (hms, ranzcr) |
| `RULES_NOT_ACCEPTED` | 22 | 666 | 18,527 | in MLE-bench, but our Kaggle account has not accepted the rules (download returns 403) |
| `NO_GRADER_YET` | 3 | 248 | 7,243 | paired comps without an MLE-bench grader (amex, commonlit, equity). Per the brief, no grader is written yet |
| `NO_GRADER` | 105 | 3,369 | 116,592 | not in MLE-bench |
| `NO_TRAJECTORIES` | 7 | 0 | 0 | listed in `competitions.json` but no trajectories in the release |

So the 26 MLE-bench comps hold 848 trajectories / 24,695 versions with code. All 7 paired comps have their
rules accepted on our account. The 22 humans-only MLE-bench comps do not.

Sizes of the 4 MLE-bench paired comps (zip = what `mlebench prepare` downloads):

| comp | zip (GB) | MLE-bench dataset size (GB) | status |
|---|---:|---:|---|
| google-quest-challenge | 0.005 | 0.015 | READY |
| learning-agency-lab-automated-essay-scoring-2 | 0.012 | 0.036 | READY |
| ranzcr-clip-catheter-line-classification | 12.6 | 13.1 | PREPARABLE |
| hms-harmful-brain-activity-classification | 19.8 | 26.4 | PREPARABLE |

## Columns

| column | meaning |
|---|---|
| `comp`, `name`, `year`, `metric`, `score_direction` | from TraceML `competitions.json` |
| `traceml_split` | `paired`, `humans_only`, or empty if no trajectories |
| `in_mlebench` | a folder with this slug exists in `mle-bench/mlebench/competitions/` (commit `507f92e`) |
| `grader_source` | `mlebench`, `traceml_private_extension_unreleased` (amex, commonlit, equity), or `none` |
| `mlebench_complexity`, `mlebench_category`, `mlebench_dataset_gb` | from `mle-bench/experiments/competition_categories.csv` (only for MLE-bench comps) |
| `task_type` | coarse type: `cv`, `nlp`, `tabular`, `audio`, `signal`, `timeseries`, or `tabular_or_text` |
| `task_type_source` | `traceml_manifest` (29), `mlebench_categories` (19), or `kaggle_file_ext_heuristic` (93). The heuristic says `cv`/`audio` if image/audio files appear among the first 1,000 listed files, otherwise `tabular_or_text`. It is a rough guess. |
| `kaggle_n_files_listed`, `kaggle_listing_complete`, `kaggle_listed_gb` | from the Kaggle file listing, capped at 1,000 files because the API is slow (~5 s/page) for big image comps. When `kaggle_listing_complete` is False, `kaggle_listed_gb` is only a **lower bound**. Empty for 4 comps where the listing API returns no files at all (seti-breakthrough-listen, jane-street-market-prediction, data-science-bowl-2019, rsna-intracranial-hemorrhage-detection). |
| `kaggle_zip_gb` | exact size of the full download zip (`Content-Length`). Only known when the rules are accepted |
| `rules_accepted`, `download_ok`, `download_error` | from a download request that reads only the headers: 200 means accepted and downloadable, 403 "You must accept this competition's rules" means not accepted |
| `n_trajectories`, `n_versions`, `n_versions_with_code`, `n_versions_kaggle_scored` | human rows in the paired + humans_only state tables. "with code" = `raw_code_path` set (= file exists in the tarball) |
| `status`, `status_note` | see the table above |

## Caveats

- `rules_accepted` is about **this** Kaggle account (pengchej). Another account would get different results.
- `PREPARABLE` means the download works. `mlebench prepare` itself has not been tried for hms or ranzcr
  (13–26 GB each).
- For best size estimates use `kaggle_zip_gb` (exact, rules accepted only), then `mlebench_dataset_gb`, then
  `kaggle_listed_gb` (lower bound when truncated).

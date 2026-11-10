# Our own MLE-bench entries: amex, commonlit, equity

Official MLE-bench has no entry for three of the seven paired TraceML competitions:
`amex-default-prediction`, `commonlitreadabilityprize` and `equity-post-hct-survival-predictions`.
`mlebench_ext/` adds them in the same format as the official entries. Each entry has `config.yaml`,
`prepare.py`, `grade.py`, `description.md`, `leaderboard.csv` and, after the first prepare, `checksums.yaml`.
With these entries, `mlebench prepare`, `mlebench grade-sample` and `src/run_version.py` (which calls
`registry.get_competition()` and then `grade_csv()`) work for these three competitions just as they do for
google-quest or aes2.

Status (2026-10-29): commonlit and equity are prepared in `/data/user_data/pengchej/mlebench-cache` and
verified. AMEX code is written and tested on synthetic data, but the real data is **not downloaded or
prepared yet**. That run needs approval (see the last section).

## Setup (once per mle-bench clone)

```bash
source /data/user_data/pengchej/software/anaconda3/etc/profile.d/conda.sh; conda activate tacit-eval
bash mlebench_ext/link.sh      # symlinks mlebench_ext/<slug> into <mle-bench>/mlebench/competitions/
```

- `link.sh` is idempotent. It never overwrites a real (non-symlink) folder. It finds the clone through the
  installed `mlebench` package, or through `MLEBENCH_DIR=...`.
- Python imports `mlebench.competitions.<slug>.grade` through the symlink. `get_repo_dir()/description`
  also resolves through it.
- `git status` in the mle-bench clone will list the three symlinks as untracked. That is expected.
- Because the folders are symlinks, `checksums.yaml` (written by the first `mlebench prepare`) lands
  directly in `mlebench_ext/<slug>/`.
- `registry.list_competition_ids()` does **not** list the three entries, because Python 3.11's `rglob` does
  not follow symlinked folders. This only affects the CLI's "valid options" help text and `prepare --all`.
  `get_competition()`, `prepare -c <slug>` and `grade-sample` all work.

The equity grader needs **lifelines**, which was missing from `tacit-eval`. lifelines 0.30.3 pins
`pandas<3`, so a plain `pip install lifelines` would have downgraded the env's pandas from 3.0.6 to 2.3.3.
That would change the environment that expert notebooks run in. I installed it without its dependencies
instead (all the others were already present):

```bash
pip install --no-deps lifelines==0.30.3 formulaic==1.2.2 autograd==1.9.1 autograd-gamma==0.5.0 interface_meta==2.0.1
```

`pip check` now reports "lifelines 0.30.3 has requirement pandas<3.0". `concordance_index` works with
pandas 3.0.6, and it reproduces the official docstring example (0.75).

## Prepare and grade

```bash
C=/data/user_data/pengchej/mlebench-cache
mlebench prepare -c commonlitreadabilityprize --data-dir $C
mlebench prepare -c equity-post-hct-survival-predictions --data-dir $C
mlebench grade-sample <submission.csv> commonlitreadabilityprize --data-dir $C
```

If you change a `prepare.py`, delete `$C/<slug>/prepared` and rerun with `--overwrite-checksums`. Otherwise
the checksum check fails.

## Splits

All three splits use `train_test_split(test_size=0.1, random_state=0)` on Kaggle's training data, the same
convention as the official entries (e.g. aes2 and petfinder). Kaggle's own test set has no public labels, so
it is not used. Only its column list is reused. Inside each output file, rows keep their original order.

| competition | split unit | new train | test (held out) | public test columns | private answers |
|---|---|---|---|---|---|
| commonlit | excerpt (`id`) | 2,550 | 284 | `id, url_legal, license, excerpt` (no `target`, no `standard_error`) | `id, target, standard_error` |
| equity | patient (`ID`, original IDs kept) | 25,920 | 2,880 (448-531 per race_group) | train columns minus `efs, efs_time` | `ID, efs, efs_time, race_group` |
| amex | customer (`customer_ID`) | 413,021 customers | 45,892 customers (default rate 26.1%) | `test_data.csv` = all statement rows of the test customers, same columns as `train_data.csv` | `customer_ID, target` |

- **public/** holds the files that notebooks see:
  - commonlit: `train.csv`, `test.csv`, `sample_submission.csv`
  - equity: the same three, plus `data_dictionary.csv`
  - amex: `train_data.csv`, `train_labels.csv`, `test_data.csv`, `sample_submission.csv`
- **private/** holds `answers.csv`.
- No test label is in any public file. `prepare.py` asserts this, and I checked it separately.
- AMEX is split on `train_labels.csv` (one row per customer), so a customer is never on both sides.
  `train_data.csv` (about 16 GB) is streamed line by line, and each raw line is copied unchanged to
  `train_data.csv` or `test_data.csv`. RAM stays under 1 GB, and the CSV formatting is exactly Kaggle's.
- Sample submissions:
  - commonlit: `target=0.0` (as on Kaggle)
  - equity: `prediction=0.5` (as on Kaggle)
  - amex: random uniform values, seed 0

## Metrics and where they come from

| competition | metric | direction | source |
|---|---|---|---|
| commonlit | RMSE (`sklearn.metrics.root_mean_squared_error`) | lower | Kaggle Evaluation page. There is no special code; this is the same approach as the official MLE-bench RMSE entries. |
| equity | race-stratified C-index: for each `race_group`, `lifelines.utils.concordance_index(efs_time, -prediction, efs)`; score = mean - std (ddof=0) across groups | higher | Kaggle's official metric notebook `metric/eefs-concordance-index`. `score()` is copied verbatim into `grade.py`. |
| amex | M = 0.5 x (normalized Gini with negatives weighted 20x + share of defaults captured in the top 4%) | higher | Python metric notebook by Kaggle staff, `inversion/amex-competition-metric-python`, linked from the Evaluation page. `amex_metric()` is copied verbatim into `grade.py`. |

Both notebooks were pulled with `kaggle kernels pull <owner>/<slug>` on 2026-10-29.

For equity, **`prediction` is a risk score**: a higher value means the event is expected sooner. A model
that outputs P(event) scores 0.649 on our split; the same predictions with the sign flipped score 0.324.

Each `grade()` checks the submission's columns, row count, unique and matching IDs, numeric values and the
absence of NaN/inf. If a check fails it raises `InvalidSubmissionError`, and `grade_csv` then reports
`score=None, valid_submission=False`. Rows are aligned by ID, so row order in the submission does not matter.

### leaderboard.csv: medals are meaningless here

`grade_csv` needs a `leaderboard.csv` to compute medal thresholds. It also infers "lower is better" by
comparing the first row with the last. `mlebench_ext/make_leaderboard.py <slug>` downloads Kaggle's
leaderboard and converts it to MLE-bench's format.

- It calls the API directly because `kaggle competitions leaderboard --download` in kaggle 1.6.17 crashes
  with `KeyError: 'last-modified'`.
- It drops Kaggle's benchmark rows (Rank 0) and team names.
- Team counts: amex 4,874, commonlit 3,633, equity 3,325.
- The API only serves the **public** leaderboard, which was scored on Kaggle's test set, not ours. So the
  medal and above-median flags in the report do not mean anything for these three competitions. Only
  `score` and `is_lower_better` (correct for all three) should be used.

## Verification (run on 2026-10-29)

`mlebench prepare` took about 3 s per competition. Rerunning it confirmed that the zip and the prepared files
match `checksums.yaml`.

`mlebench grade-sample <cache>/<slug>/prepared/public/sample_submission.csv <slug> --data-dir <cache>`:

- commonlit: score **1.46571**. The sample predicts 0 for every row, so the expected value is
  sqrt(mean² + var) of the test targets, which matches.
- equity: score **0.5**. The prediction is constant.

Sanity checks went through `registry.get_competition()` and `grade_csv()`, the same path `run_version.py`
uses. Submissions built from the answers were written only to a temp dir, which has been deleted.

| check | commonlit (RMSE) | equity (stratified C-index) |
|---|---|---|
| perfect submission, rows shuffled | 0.0 | 1.0 (C = 1.0 in all 6 groups) |
| constant prediction | 1.04871 (train mean; expected 1.04871) | 0.5 (expected 0.5) |
| simple baseline trained on public train only | TF-IDF + Ridge: 0.74889 | HistGradientBoosting P(efs=1): 0.64853; sign flipped: 0.32384 |
| independent re-implementation | - | random predictions: 0.49406 = 0.49406 |
| official docstring example | - | 0.75 |
| malformed: missing column, missing row / duplicate ID, NaN, unknown IDs, non-numeric | all raise `InvalidSubmissionError`; `grade_csv` returns `score=None` | same |

**AMEX on synthetic data.** I used the real `train_labels.csv` (all 458,913 customers, 17 MB download) and a
synthetic `train_data.csv`: 5.25M statement rows (12 per customer on average, like the real file) with a few
narrow columns, plus a trailing blank line. `prepare()` was called through the registry.

- It split 5.25M rows in 2-3 s, with 0.64 GB peak RAM.
- Replaying the raw file showed that every row was copied **byte for byte** to the correct side.
- Test customers in `test_data.csv` are exactly the answer customers. No customer appears on both sides, and
  no test customer appears in the public `train_labels.csv`.
- Grader results:
  - perfect: 1.0, also with shuffled rows
  - random: 0.017 (expected about 0.02)
  - prediction = 1 - target: -0.5
  - noisy target: 0.5153, and an independent numpy implementation gives the same value
  - malformed submissions are rejected
- A second synthetic file with wide rows (1.9 GB, 3.7 KB/line) split at about 1 GB/s.

## AMEX full prepare: what it needs (not run; needs your OK)

Measured: the whole-competition zip is **21.98 GB**. Downloading `train_data.csv` alone is 7.16 GB. Uncached
NAS read is about 440 MB/s.

**Option A, standard (recommended):**
`mlebench prepare -c amex-default-prediction --data-dir /data/user_data/pengchej/mlebench-cache`

- **Disk:** about 90 GB at peak: the zip (22 GB), the extracted raw files (about 47 GB, of which Kaggle's
  unused `test_data.csv` is 32 GB) and the prepared files (about 16 GB). The raw folder is deleted at the
  end unless you pass `--keep-raw`, leaving about 38 GB. 1.8 TB is free.
- **RAM:** under 1 GB for `prepare()`. Ask for 8 GB to be safe. One CPU is enough. No GPU.
- **Time:** about 15-35 min.
  - Download: 4-20 min, depending on network speed. Not measured for a large file.
  - md5 of the zip: about 1 min.
  - Python unzip of about 47 GB: about 5-10 min.
  - Split: about 1-3 min.
  - md5 of the outputs: about 1 min.
- Run it as an `sbatch` CPU job. Compute nodes have internet; this node downloaded from Kaggle fine.

**Option B, lean (about 40 GB peak, skips the 32 GB `test_data.csv`):**

```bash
R=/data/user_data/pengchej/mlebench-cache/amex-default-prediction/raw; mkdir -p $R; cd $R
kaggle competitions download -c amex-default-prediction -f train_data.csv    # 7.2 GB zip
kaggle competitions download -c amex-default-prediction -f train_labels.csv  # 17 MB zip
unzip train_data.csv.zip && unzip train_labels.csv.zip && rm ./*.zip
python -c "
from pathlib import Path; from mlebench.registry import registry
c = registry.set_data_dir(Path('/data/user_data/pengchej/mlebench-cache')).get_competition('amex-default-prediction')
c.public_dir.mkdir(parents=True, exist_ok=True); c.private_dir.mkdir(parents=True, exist_ok=True)
c.prepare_fn(raw=c.raw_dir, public=c.public_dir, private=c.private_dir)
(c.public_dir / 'description.md').write_text(c.description)"
```

Option B writes no `checksums.yaml`, and a later `mlebench prepare` would still try to download the full zip.
Grading works either way: it only needs `prepared/private/answers.csv`.

Suggested check after the real prepare: the "mean P_2" benchmark from the metric notebook should score
roughly 0.57 on our test customers. It scores 0.572773 on all of Kaggle's training data.

## Caveats and what is not verified

- **Not comparable to TraceML.** TraceML's agent runs used an unreleased MLE-bench extension for these three
  competitions. Our splits, test sets and therefore scores are not the same as theirs, and not comparable to
  Kaggle leaderboard scores either. Always re-run expert baselines on our split.
- **Leakage through external inputs.** The held-out test rows come from Kaggle's *training* data. An external
  dataset or checkpoint built from the full Kaggle training set has therefore seen our test labels.
  - Examples: commonlit models fine-tuned on all of `train.csv`, and AMEX preprocessed feature sets with the
    target merged in.
  - Such versions can score unrealistically well.
  - AMEX notebooks that read Kaggle's test via an external parquet dataset will also predict the wrong
    customers. Their submission then fails as invalid.
  - The same problem exists for the official MLE-bench entries. It should be flagged in version triage.
- AMEX was not run on the real data. The column layout, line endings and real file size are untested. The
  code only assumes that `customer_ID` is the first column, and it asserts that.
- The AMEX metric is Kaggle's Python notebook version. Kaggle's own scoring backend could break ties
  differently. That matters only for heavily tied predictions.
- Leaderboards are Kaggle's public leaderboards, so medal flags are meaningless (see above).
- The `description.md` files are short paraphrases of the Kaggle overview, data and evaluation pages, not
  verbatim copies.
- No expert notebook version has been run against these entries yet. `src/run_version.py` was not changed.

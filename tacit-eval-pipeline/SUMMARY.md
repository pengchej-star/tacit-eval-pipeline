# Progress summary: executable evaluation for tacit-knowledge experiments

*Status as of 2026-10-08. All numbers come from `results/runs.jsonl`, `triage/*.csv` and `docs/`.*

## 1. Goal

We used to judge an agent's next step by comparing its *plan* with the expert's next edit (LLM judge, 0–2
similarity). Instead, we want to **execute** the code and **grade** its `submission.csv` on the held-out
MLE-bench split, as TraceML does. A second goal is to find out which TraceML cases (adjacent expert versions
`v_k → v_k+1`) can actually be run today.

## 2. What I did

- **Built a run + grade pipeline** (`src/run_version.py`). It takes one expert notebook version, runs it in an
  isolated Kaggle-like folder that sees only the public data, and grades its `submission.csv` with the
  MLE-bench grader. Every run is logged.
- **Mapped the TraceML release.** Each `(key_id, version)` maps to one notebook; 148,530 of 149,483 human
  versions have code.
- **Triaged all 141 TraceML competitions**: is there a grader, can we download the data, how large is it.
- **Triaged all 5,988 cases** in the 4 paired competitions that have a grader, statically (without running
  them): external inputs, GPU, internet, training, runtime.
- **Validated end to end.** I re-ran 2 expert cases with full grading, then executed a random sample of 15
  "EASY" cases twice: before and after fixing the run environment.

## 3. Key results

**Expert re-runs (aes2; metric QWK, higher is better).** Both improvements reproduce in our environment, and
repeat runs gave identical scores.

| case | v_k → v_k+1 (our score) | Kaggle public score | same direction? |
|---|---|---|---|
| aes2 55844901 v1 → v2 | 0.599 → 0.664 | 0.674 → 0.696 | yes |
| aes2 55822700 v12 → v13 | 0.661 → 0.667 | 0.704 → 0.711 | yes |

**The 7 paired competitions.**
- **Ready**: aes2 and gquest are prepared, and grading is verified.
- **Downloadable, not prepared yet**: hms (20 GB zipped) and ranzcr (13 GB zipped). Rules are accepted and the
  download works.
- **No public grader**: amex, commonlit and equity (see §4).

**Case triage** (static, aes2 / gquest / hms / ranzcr):

| comp | EASY | missing external input* | needs training | needs GPU | needs internet | no code | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| aes2 | 157 | 1,797 | 107 | 7 | 138 | 2 | 2,208 |
| gquest | 66 | 597 | 184 | 21 | 18 | 0 | 886 |
| hms | 117 | 1,958 | 70 | 140 | 42 | 0 | 2,327 |
| ranzcr | 0 | 498 | 14 | 27 | 28 | 0 | 567 |

\*almost all unverified, see §5.

**Executing the 15 sampled EASY cases** (aes2 + gquest; r2 = after adding missing packages and three
API-rename patches):

| round | versions run OK (of 27) | cases with both versions OK (of 15) |
|---|---:|---:|
| r1 | 2 (4 with a retry patch) | 0 (1) |
| r2 | **13** | **5** |

## 4. Why only 4 of the 7 paired competitions are gradable

- **amex, commonlit and equity are not in the public MLE-bench.**
- **The TraceML authors graded them with a private MLE-bench extension.** Their agent `task.md` even points
  commonlit to a `prepared/public` folder, but the prepare/grade code for these three was never released.
- **Options:** (a) write our own `prepare.py` / `grade.py` for each, splitting train into train/test and using
  the metric from TraceML's `competitions.json`; or (b) ask the authors (Jiarui Yan) for their extension.

## 5. Caveats

- **Our scores are not comparable to Kaggle scores.** MLE-bench re-splits Kaggle's training data into a new
  test set (e.g. 1,731 essays for aes2 vs Kaggle's ~8k hidden essays). Only compare scores from our pipeline.
- **The "missing external input" labels are mostly unverified.** 4,941 of the 4,943 versions with that label
  are unverified, because Kaggle's API rate-limited the lookups. Many of these inputs are probably still
  downloadable.
- **EASY ≠ runnable as-is.** The static label checks inputs, GPU and internet, and those checks held. But
  2019–2024 code breaks on a 2026 library stack: missing packages, removed APIs, old plotting code. Some
  notebooks also hit memory or time limits on CPU.
- **No sandbox yet.** Expert code can't see the answers through its inputs, but it runs as our user. Agent-written
  code needs container isolation.

## 6. Next steps

1. Run the first **agent-edited** versions against their expert baselines on the aes2 cases that already work.
2. Resolve external inputs exactly with Meta Kaggle's `KernelVersionDatasetSources` table, then download the
   inputs that still exist. This should make a large share of the "missing" cases runnable.
3. Prepare hms and ranzcr, and use a GPU node for the GPU/training cases.
4. Decide on amex, commonlit and equity: build our own graders or ask the authors.

## 7. Details

- [README.md](README.md): what the repo does, setup, commands
- [docs/dataset_notes.md](docs/dataset_notes.md): the TraceML data and how versions map to notebooks
- [docs/phase2_competition_triage.md](docs/phase2_competition_triage.md) and `triage/competitions.csv`
- [docs/phase3_grader_smoke_test.md](docs/phase3_grader_smoke_test.md): grader check
- [docs/phase4_runs.md](docs/phase4_runs.md): first expert re-runs
- [docs/phase5_case_triage.md](docs/phase5_case_triage.md) with `triage/versions.csv` and `triage/cases.csv`: case triage and EASY validation

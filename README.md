# tacit-eval-pipeline

Executable evaluation for the tacit-knowledge project. Given a Kaggle competition and a piece of code (an
expert notebook version from the [TraceML](https://huggingface.co/datasets/jerryyan/TraceML) dataset, later an
agent-edited version), the pipeline runs the code in an isolated Kaggle-like workdir, picks up
`submission.csv`, and grades it with the competition's held-out MLE-bench grader. This replaces "LLM judge
compares the agent's plan with the expert's next edit" with "run it and score it".

It also triages which competitions and which expert transitions `(key_id, v_k → v_k+1)` can be run today,
and why the others cannot.

## Setup (CMU Babel)

Large files live under `/data/user_data/$USER` (compute nodes only). Two conda envs (Python 3.11):

```bash
# 1. tacit-eval: orchestration + grading (mlebench)
conda create -n tacit-eval python=3.11 && conda activate tacit-eval
git clone https://github.com/openai/mle-bench.git && (cd mle-bench && git lfs fetch --all && git lfs pull)
pip install -e ./mle-bench huggingface_hub pyarrow pandas nbconvert
# needs ~/.kaggle/kaggle.json (legacy API key; mlebench pins kaggle<1.7)

# 2. kaggle-run: the stack notebooks execute in (pinned in env/kaggle-run.txt, CPU torch)
conda create -n kaggle-run python=3.11 && conda activate kaggle-run
pip install -r env/kaggle-run.txt --extra-index-url https://download.pytorch.org/whl/cpu
python -m ipykernel install --prefix "$CONDA_PREFIX" --name kaggle-run
python -m nltk.downloader -d "$CONDA_PREFIX/share/nltk_data" stopwords punkt wordnet

# 3. TraceML data: notebooks + tables (see docs/dataset_notes.md)
hf download jerryyan/TraceML --repo-type dataset --revision 6472e74ba6393d4b87bb7ff8e4246e154d359b20 \
   --local-dir /data/user_data/$USER/traceml/hf --include "data/*" "extras/*" "manifests/*" trajectories_human.tar.gz
mkdir -p /data/user_data/$USER/traceml/extracted && \
  tar -xzf /data/user_data/$USER/traceml/hf/trajectories_human.tar.gz -C /data/user_data/$USER/traceml/extracted
```

All commands below are run from the repo root in the `tacit-eval` env.

## Usage

**Prepare a competition** (you must first accept its rules on kaggle.com):

```bash
mlebench prepare -c learning-agency-lab-automated-essay-scoring-2 --keep-raw --data-dir /data/user_data/$USER/mlebench-cache
mlebench grade-sample /data/user_data/$USER/mlebench-cache/learning-agency-lab-automated-essay-scoring-2/prepared/public/sample_submission.csv \
   learning-agency-lab-automated-essay-scoring-2 --data-dir /data/user_data/$USER/mlebench-cache   # smoke test
```

**Run and grade one version** (an expert version, or any `.ipynb`/`.py` via `--code-file`):

```bash
python src/run_version.py --comp learning-agency-lab-automated-essay-scoring-2 --key-id 55844901 --version 2 --timeout 900
# compat patches (API renames) are applied by default and recorded; --patches none to disable
```

This creates `/data/user_data/$USER/runs/<comp>__<key_id>_vNNN__<time>/` (read-only copies of `prepared/public`
as `kaggle/input/<comp>`, the notebook before/after execution, the log). It appends one row to
`results/runs.jsonl`: status, MLE-bench score, Kaggle score, runtime, patches, error tail.

**Triage**:

```bash
python src/triage_competitions.py --traceml-dir /data/user_data/$USER/traceml/hf \
   --mlebench-dir <mle-bench clone> --mlebench-cache /data/user_data/$USER/mlebench-cache \
   --kaggle-cache /data/user_data/$USER/traceml/kaggle_probe.json          # -> triage/competitions.csv
python src/triage_static.py --comps learning-agency-lab-automated-essay-scoring-2 google-quest-challenge \
   hms-harmful-brain-activity-classification ranzcr-clip-catheter-line-classification
                                                                          # -> triage/versions.csv, cases.csv
python src/validate_easy_sample.py --per-comp learning-agency-lab-automated-essay-scoring-2=8 \
   --per-comp google-quest-challenge=7 --seed 0 --timeout 900             # executes a sample of EASY cases
```

Kaggle API answers are cached, so reruns are cheap.

## Results so far

Expert re-runs (aes2, metric QWK, higher is better; Phase 4):

| key_id | version | status | MLE-bench score (ours) | Kaggle public score | runtime |
|---|---|---|---:|---:|---:|
| 55844901 | v1 | OK | 0.5992 | 0.6742 | 8 s |
| 55844901 | v2 | OK | **0.6640** | 0.6957 | 11 s |
| 55822700 | v12 | OK | 0.6613 | 0.7043 | 4 s |
| 55822700 | v13 | OK | **0.6673** | 0.7114 | 4 s |

Both transitions improve in our environment as they did on Kaggle. Re-runs gave identical scores, and no
patches were needed.

Triage (details in `triage/` and the docs):

- **Competitions** (`triage/competitions.csv`, 141 TraceML comps): 26 are in MLE-bench. 2 are `READY` (aes2,
  gquest: prepared and grading verified). 2 are `PREPARABLE` (hms, ranzcr: rules accepted, 13–26 GB). 22 are
  `RULES_NOT_ACCEPTED` on our Kaggle account. 3 are `NO_GRADER_YET` (amex, commonlit, equity), 105 are
  `NO_GRADER`, and 7 have no trajectories.
- **Cases** (`triage/cases.csv`, 5,988 transitions `v_k → v_k+1` in aes2, gquest, hms, ranzcr; static, nothing
  executed):

  | comp | MISSING_EXTERNAL_INPUT* | NEEDS_INTERNET | NEEDS_GPU | NEEDS_TRAINING | NO_CODE | EASY | total |
  |---|---:|---:|---:|---:|---:|---:|---:|
  | aes2 | 1,797 | 138 | 7 | 107 | 2 | 157 | 2,208 |
  | gquest | 597 | 18 | 21 | 184 | 0 | 66 | 886 |
  | hms | 1,958 | 42 | 140 | 70 | 0 | 117 | 2,327 |
  | ranzcr | 498 | 28 | 27 | 14 | 0 | 0 | 567 |

  \* almost all *unverified*: the input's Kaggle ref was not found, or its access check was rate-limited.
  Many are probably downloadable (see `docs/phase5_case_triage.md`).
- **EASY ≠ runs as-is.** The same 15 sampled EASY cases (aes2 + gquest) were executed twice (`run_round` in
  `results/runs.jsonl`):

  | round | versions OK (of 27) | cases OK (of 15) |
  |---|---:|---:|
  | r1: original env, no patches (KFold patch on retry) | 2 (4) | 0 (1) |
  | r2: + `wordcloud`/`pyarrow`/`gensim`/NLTK data, all compat patches auto-applied | **13** | **5** |

  Remaining r2 failures (14 versions):
  - 5 × still-missing packages (`pyLDAvis`; no TensorFlow/Keras in the env);
  - 4 × EDA plots broken by newer seaborn/matplotlib;
  - 2 × out of memory and 1 × 15-min timeout, with 3 parallel runs on a 32 GB CPU job;
  - 2 × real bugs in versions that have no Kaggle score.

  None failed because of what the static label checks (external inputs, GPU, internet).

## Known limitations

- **Kaggle scores and MLE-bench scores are not comparable.** MLE-bench re-splits Kaggle's train set into its own
  train/test (e.g. aes2 test = 1,731 held-out essays vs Kaggle's ~8k hidden ones). Only compare scores produced
  by this pipeline, and always re-run the expert baseline.
- **Older code may need compatibility patches.** The run env is a 2026 stack (pandas 3, scikit-learn 1.9).
  Known patches (pure API renames) are auto-applied (`--patches all`, default) where they match and recorded
  in `patches_applied`. The env still lacks some packages that Kaggle's image has (e.g. TensorFlow).
- **gquest mostly relies on pretrained weights** (BERT/USE/... from external Kaggle datasets). Its runnable,
  self-contained notebooks are few and weak (Kaggle score ≤ 0.14, best 0.31 with a small MLP).
- **No container isolation.** The notebook only gets copies of `prepared/public`, and nothing points at the
  answers, but it runs as our user. Code that deliberately opened `prepared/private` could read it. Add a
  container (e.g. Apptainer) before running agent-written code.
- **amex, commonlit and equity have no grader.** They are not in MLE-bench (the TraceML authors used an
  unreleased extension), so they are marked `NO_GRADER_YET`.
- Static triage is regex-based: it can miss dynamically built paths or packages missing from our env.
  See the measured accuracy in `docs/phase5_case_triage.md`.

## Next steps

1. Run an agent-edited version (`--code-file`) against its expert baseline on the EASY aes2 cases.
2. Resolve external inputs exactly with Meta Kaggle's `KernelVersionDatasetSources` table (exact
   `owner/dataset` per kernel version) instead of searching Kaggle by folder name. That will turn the
   "unverified" `MISSING_EXTERNAL_INPUT` labels into confirmed missing or downloadable.
3. Widen the runnable set. After round r2, the next cheap steps are:
   - add `pyLDAvis` and TensorFlow/Keras to `kaggle-run`;
   - run memory-heavy notebooks one at a time (or on a bigger job);
   - prefer cases where both versions have a Kaggle score.

   Then download the external datasets that are still available (`NEEDS_EXTERNAL_DOWNLOAD`) into
   `kaggle/input`, and use a GPU node for `NEEDS_GPU` / `NEEDS_TRAINING`.
4. `mlebench prepare` hms and ranzcr (13–26 GB each; rules already accepted), with hardlinks instead of copies.
5. Container isolation for agent code. Decide with the TraceML authors (Jiarui Yan) how amex, commonlit and
   equity were graded.

## Docs

- [docs/dataset_notes.md](docs/dataset_notes.md): TraceML layout, `(key_id, version)` → notebook mapping, score columns
- [docs/phase2_competition_triage.md](docs/phase2_competition_triage.md): competition triage columns and summary
- [docs/phase3_grader_smoke_test.md](docs/phase3_grader_smoke_test.md): `mlebench prepare` / `grade-sample`, schema check
- [docs/phase4_candidates.md](docs/phase4_candidates.md): how the first cases were chosen
- [docs/phase4_runs.md](docs/phase4_runs.md): runner design and first results
- [docs/phase5_case_triage.md](docs/phase5_case_triage.md): case triage and validation of the EASY label

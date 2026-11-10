# tacit-eval-pipeline — brief for Claude Code

## Context

This repo belongs to a CMU (Sherry Wu / Niki Kittur group, Bosch-sponsored) project on
*tacit knowledge* in ML engineering. The team extracts "knowledge items" from expert Kaggle
trajectories and tests whether giving them to a coding agent improves its next step.

Today that test compares the agent's *proposed plan* with the expert's actual next edit
(LLM judge, 0–2 similarity). The advisors find that too rigid. **This repo replaces it with
executable evaluation:** run code, produce `submission.csv`, grade it with the competition's
held-out grader — the same evaluation TraceML (arXiv 2608.26086) uses.

This repo is a standalone module. It does not need to plug into the team's experiment code yet.

## Deliverables (first version)

1. A runnable pipeline: given a competition slug and a piece of code (an expert version from
   the TraceML dataset, later an agent-edited version), execute it and grade the submission.
2. Tested end to end on at least one or two cases.
3. A triage table of which cases are runnable and which are not, with reasons:
   - inputs complete → easy
   - data or test set missing
   - external checkpoint or dataset missing
   - needs heavy training
   - and so on

Push to `github.com/pengchej-star/tacit-eval-pipeline`. Collaborator `yyqbeatrice` (Yaqing) reviews it.

## What is already known (verified)

- **TraceML toolkit** (`github.com/JerryYan123/TraceML`, `pip install -e .`, CLI `traceml`).
  It is an analysis toolkit: `extract`, `label`, `report`, `from-released`.
  - `traceml record` runs a CLI agent and grades every new `submission.csv` with
    `mlebench grade-sample <submission> <slug> --data-dir $TRACEML_MLEBENCH_CACHE`.
  - It does **not** re-execute human notebooks. That part is ours to build.
- **HF dataset** `jerryyan/TraceML` (checked via the HF API):
  - **`trajectories_human.tar.gz` (2.9 GB): the raw human `.ipynb` per version** (outputs
    stripped). This is where expert code lives. Download it to `/data/user_data/$USER`, not `$HOME`.
  - `data/{paired,humans_only,experiment_run}/{state,action}.parquet` (paired state ≈ 6.7 MB,
    humans_only state ≈ 55 MB). Rows carry `key_id, comp, version_number, is_agent, group, score,
    coarse_tags, fine_tags, summary`; `key_id` joins to the tarball.
  - `extras/`:
    - `kernels.parquet`: per-kernel license and metadata
    - `trajectory_index.parquet`
    - `nodes.parquet`, `edges.parquet`, `trees.parquet`: lineage graph
  - `manifests/`: `competitions.json` (metric and score direction for 141 comps),
    `filter_rules.json`, and `schemas/`.
  - `trajectories_experiment_run/`: 32 Codex (gpt-5.4-mini, 12 h) runs on the 7 paired comps,
    each with `task.md`, `run_meta.json`, `submission.csv` and per-version code.
  - `code/`: `01_extract … 04_label` dataset pipeline and `05_toolkit` (superseded by the GitHub toolkit).
  - **No code for running or grading submissions is released**, and nothing documents how the
    non-MLE-bench comps were prepared.
  - Their `task.md` points the agent at `<mlebench cache>/<slug>/prepared/public` even for
    commonlit, so the authors used a private MLE-bench extension.
  - One gquest kernel (6810482) was removed for a label leak.
- **Paired competitions (7):** amex-default-prediction, commonlitreadabilityprize,
  equity-post-hct-survival-predictions, google-quest-challenge,
  hms-harmful-brain-activity-classification, learning-agency-lab-automated-essay-scoring-2,
  ranzcr-clip-catheter-line-classification.
- **Coverage in official MLE-bench** (`github.com/openai/mle-bench`, `mlebench/competitions/`):
  - Of the 7 paired competitions, only google-quest, hms, aes2 and ranzcr are in it.
    amex, commonlit and equity are not. The authors' extension for them is not released.
  - Options for those three:
    - (a) write our own MLE-bench competition entries (`config.yaml`, `prepare.py`
      splitting train into train/test, `grade.py` with the metric from `competitions.json`)
    - (b) ask the authors (Jiarui Yan, CMU)

    **Do not do (a) in the first version.** Mark them `NO_GRADER_YET` and move on.
  - Of the 141 TraceML competitions, 26 are in MLE-bench.
- **MLE-bench** needs Python >= 3.11 and pins `kaggle>=1.6,<1.7`, so it authenticates with the
  legacy `~/.kaggle/kaggle.json`, not the new access tokens. Its README requires git-lfs.
  - `mlebench prepare -c <slug> --data-dir <cache>` writes `<cache>/<slug>/prepared/{public,private}`.
  - `public` holds train, an unlabeled test and sample_submission.
  - `private` holds the answers.
  - MLE-bench re-splits Kaggle's train set, so scores are **not** comparable to the Kaggle
    leaderboard scores stored in TraceML. Always re-run expert baselines in our environment.
- **Starting points:** google-quest-challenge and learning-agency-lab-automated-essay-scoring-2
  (small text data). ranzcr and hms are large image/signal datasets.

## Environment: CMU Babel (SLURM)

- Login node: editing, git, pip, small downloads. **No heavy compute on the login node.**
- GPU work: `srun -p <partition> --gres=gpu:1 --time=... --pty bash` or `sbatch`.
  Check `sinfo` for partition names.
- Large data goes in `/data/user_data/$USER` (compute nodes only), not `$HOME`.
  Use `/data/user_data/$USER/mlebench-cache` as the MLE-bench data dir.
- Check whether compute nodes have internet (Kaggle and HF). If not, download on the login
  node or via a transfer node.
- Ask the user before launching any job longer than ~30 minutes or using more than 1 GPU.

## Plan (do in order; stop and report after each phase)

**Phase 0 — env.**
- Create a conda env with Python 3.11.
- Install `mle-bench` (git clone + git lfs + `pip install -e .`) and the TraceML toolkit
  (no `[label]` extra needed).
- Verify `kaggle competitions list` works.

**Phase 1 — dataset inventory → `docs/dataset_notes.md`.**
- Download the `data/`, `extras/` and `manifests/` parquet and json files.
- Download `trajectories_human.tar.gz` to `/data/user_data/$USER/traceml`.
- Record the columns of each parquet.
- List the tarball layout with `tar -tzf … | head` before extracting.
- Answer:
  - how a `(key_id, version_number)` maps to a notebook file in the tarball
  - how many versions have code, per competition
  - whether the paired split is fully covered
- Note the per-version Kaggle score column. Remember it is not comparable to MLE-bench scores.

**Phase 2 — competition triage → `triage/competitions.csv`.**
One row per TraceML competition, with these columns:

- in MLE-bench (or in TraceML's own additions)
- task type
- data size (`kaggle competitions files`)
- whether rules are accepted / download works
- number of trajectories and versions with code
- status

**Phase 3 — grader smoke test.**
- `mlebench prepare` google-quest and aes2.
- `mlebench grade-sample` their `sample_submission.csv` and confirm a score comes back.

**Phase 4 — expert-version runner (`src/run_version.py`).**
Input: `(key_id, version_number)` or a code file plus a slug. Steps:

1. Materialize the code. Convert `.ipynb` to `.py` with nbconvert, keeping the cell order.
2. Make an isolated workdir with `kaggle/input/<slug>` symlinked to `prepared/public`
   and `kaggle/working`.
3. Rewrite `/kaggle/input` and `/kaggle/working` paths.
4. Run with a timeout, logging stdout/stderr.
5. Find `submission.csv` and grade it.
6. Append a row to `results/runs.jsonl` (key_id, version, status, score, runtime, error tail).

- Never let run code read `prepared/private`.
- Re-run expert `v_k` and `v_{k+1}` for at least one trajectory to get in-environment baselines.

**Phase 5 — version-level static triage → `triage/versions.csv`.**
For every version with code in feasible competitions, scan without executing:

- `/kaggle/input/<x>` references other than the competition itself (external datasets or
  checkpoints; check whether each is publicly downloadable via `kaggle datasets`)
- training calls vs load-only (`.fit(`, `trainer.train`, `model.train()` vs `load_state_dict`,
  `from_pretrained` of local paths)
- internet use and GPU use

Assign one status:

- `EASY`: inputs complete, inference only or light training
- `NEEDS_TRAINING`
- `MISSING_EXTERNAL_INPUT`
- `NO_GRADER` (competition not in MLE-bench); for amex, commonlit and equity use `NO_GRADER_YET`
- `NO_CODE`
- `EXEC_FAILED` (filled from Phase 4 runs)

**Phase 6 — README + push.**
- The README covers how to install, prepare a competition, run a version, the triage summary
  (counts per status) and known limitations.

## Repo layout

```
src/        run_version.py, triage_static.py, prepare.py, utils
triage/     competitions.csv, versions.csv
results/    runs.jsonl (small); large outputs stay out of git
docs/       dataset_notes.md
```

Never commit data, model weights, `kaggle.json` or tokens. Add them to `.gitignore` from the start.

## Working style

The user is new to this stack. Explain each phase's result in a few plain sentences, show the
exact commands you ran, and say clearly what you could not verify.

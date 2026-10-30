# Handoff: the 7 agent-vs-expert pivot cases (2026-10-30)

These are the 7 pivots run end to end on Oct 29–30. For each one, expert v_k, the agent's v_k+1′ and expert v_k+1
were run and graded on our split. The results and their reading are in `docs/agent_pivots_2026-10-30.md`.

`pivots.csv` has one row per pivot. Rebuild it with `python src/handoff_pivots.py`.

## Columns

| column | meaning |
|---|---|
| `comp`, `key_id`, `kernel`, `author_tier` | competition, TraceML key_id (= Kaggle kernel id), `author/slug`, Kaggle tier |
| `v_k`, `v_k1` | the pivot: TraceML `version_number` before and after (the `v_old`/`v_new` of the pivot labels) |
| `metric`, `higher_is_better` | from TraceML's `manifests/competitions.json` |
| `model_source` | `trained in notebook`: the notebook fits its model on our train split (clean). `attached weights`: it loads weights trained on all of Kaggle's train set, which contains our test rows (leakage, scores inflated) |
| `score_expert_v_k`, `score_expert_v_k1`, `score_agent_v_k1` | our scores: MLE-bench split for aes2, hms and ranzcr; our own split and grader for equity (`docs/own_graders.md`). Not comparable to Kaggle scores |
| `agent_minus_expert` | agent v_k+1′ minus expert v_k+1, signed so that > 0 means the agent is better |
| `kaggle_score_v_k`, `kaggle_score_v_k1` | Kaggle public LB score from TraceML, for reference |
| `agent_model`, `agent_minutes`, `agent_cost_usd`, `agent_turns` | the agent run: Claude Code with Claude Opus 5.5 via the CMU AI gateway, 40 min and $10 cap, no extracted knowledge. Cost is Claude Code's own estimate |
| `runtime_s_v_k`, `runtime_s_v_k1`, `runtime_s_agent` | wall-clock seconds to run and grade each version on Babel |
| `external_inputs`, `external_inputs_agent` | Kaggle datasets and kernels mounted under `/kaggle/input` (`kind:owner/slug[@version]`) |
| `run_env` | Python environment (package lists in `env/`) |
| `patches` | compatibility patches the runner applied (`src/run_version.py`, `PATCHES`) |
| `kaggle_url_v_k`, `kaggle_url_v_k1` | the exact expert versions on Kaggle |
| `expert_code` | where the expert notebooks are in TraceML's `trajectories_human.tar.gz` |
| `agent_dir` | the agent's output in this repo: `vNNN.py` (its v_k+1′), `NOTES.md` (its own notes), `task.md` (the prompt), `meta.json` |
| `expert_run_ids`, `agent_run_id` | rows in `results/runs.jsonl` and `results/agent_runs.jsonl` |

## Caveats

- One run per case, for the agent and for the experts. Rerun noise: about 0.005 KL for hms 49981285; aes2 and
  equity reproduce within 0.001.
- hms 49524919: the expert's step goes the other way on our split than on Kaggle.
- Not included: equity 77450317 v9→v10 (3rd-place solution). It could not run: an attached model dataset is unknown,
  and its helper scripts hard-code `/kaggle` paths.

# Tacit knowledge of ML experts: extraction and application

From the version histories of expert Kaggle notebooks (the [TraceML](https://huggingface.co/datasets/jerryyan/TraceML) human trajectories) this project builds

1. a **taxonomy** of what one can do to improve a solution: a tree of decisions → options → actions, with the **desiderata** (yes/no checks) of every decision;
2. an **attention map** per decision: what experts checked before choosing, in which order, how much evidence was enough, and when they came back;

and then tests whether an agent that reads this as memory improves code better than one without it.

The work is in [new_extraction/](new_extraction/). The only external dependency is an LLM endpoint (and, for the agent parts, the `claude` and `codex` CLIs).

## Repository map
| path | content |
|---|---|
| `new_extraction/` | the extraction pipeline, the agent alternative for steps 1-4, the application experiment (this README describes it) |
| `episode_pipeline/` | the earlier pipeline that produced `new_extraction/data/episode_items.jsonl` (trajectories → episodes → rationales) |
| `tacit-eval-pipeline/` | executable evaluation: run a code version in a Kaggle-like workdir and grade it with MLE-bench; `agent_generation/` has the earlier Codex runner and the TraceML planning block |
| `TraceML/` | the TraceML dataset (`human/<kernel id>/versions/vNNN.ipynb`) and toolkit |
| `BLADE/` | the BLADE benchmark (reference) |
| `doc/`, `arxived/` | papers (`Tacit_new.pdf` is the proposal) and old runs |

## new_extraction

### Setup
```bash
cd new_extraction
pip install -r requirements.txt            # python >= 3.10
cp .env.example .env                       # LITELLM_API_KEY (OpenAI-compatible proxy; URL in config.yaml)
```
`common.py` reads `new_extraction/.env`. The LLM is called through LiteLLM (`litellm.api_base`, `model.generator`, `stage_models` in `config.yaml`); if the proxy keeps failing the same model is tried on Azure when `AZURE_OPENAI_*` is set.

### Inputs (`new_extraction/data/`)
| file | content |
|---|---|
| `selection.csv` | the top 10 experts (notebook authors) of each of 7 competitions, ranked by best public score |
| `actions.parquet` | per version→version edit: TraceML action labels, `goal_nl`, `diff_summary`, magnitude |
| `scores.json` | public leaderboard score of every version |
| `episode_items.jsonl` | the trajectories cut into episodes; 856 episodes, 1,674 items, each with an *instance* and a *general* rationale (goal / context / action) |
| `topdown_skeleton.json` | the LLM-written top-down tree used by the pipeline method |
| `tasks.yaml` (next to `data/`) | per competition: name, score direction, short description |

Competitions: ranzcr-clip-catheter-line-classification, amex-default-prediction, commonlitreadabilityprize, equity-post-hct-survival-predictions, google-quest-challenge, hms-harmful-brain-activity-classification, learning-agency-lab-automated-essay-scoring-2 (70 experts, 3,393 edits, 2,019 with a score; scores are signed so `delta > 0` is always an improvement). No raw code or diff is read by the pipeline; the LLM sees TraceML's goal / change summary / labels and the scores.

### The steps
Steps 1-4 produce a **tree with desiderata** and can be done in one of two ways; steps 5-8 and 10 are the same for both.

```
 data/episode_items.jsonl
        │
        ├── method A  pipeline_tree/   (LLM calls, steps 1-4)  ─┐
        └── method B  agent_tree/      (one coding agent)       ─┤  3_merged_tree.json + 4_desiderata.json
                                                                 ▼
                       step 5 visits → 6 scores → 7 enough/order → 8 returns → 10 export
```

**Method A: `pipeline_tree/`** (original code; `python run.py` runs it)
| step | file | what it does |
|---|---|---|
| 1 top-down | `topdown.py` | the LLM writes the tree "what can one change to improve a solution" (no task data); reuses `data/topdown_skeleton.json` |
| 2 items + clustering | `items.py`, `cluster.py` | one item per episode rationale, clustered on its *general action* bottom-up (edits → actions → decisions); close pairs merge, grey-zone pairs go to the LLM |
| 3 merge | `merge.py` | matches every action to a skeleton node, adds the rest as new nodes, checks that children are real alternatives |
| 4 desiderata | `desiderata.py` | per decision node the LLM writes yes/no checks with how to observe them; deduplicated into a registry |
| (stability) | `stability.py` | half-vs-half comparison of the bottom-up trees; no longer part of `run.py` |

**Method B: `agent_tree/`** (a coding agent reads the jsonl itself and writes the tree and desiderata; see its README)
- `prompt.md` is the one prompt; `run_claude.sh` (Claude Code, `claude-sonnet-5-5`), `run_codex.sh` (Codex, `gpt-6-astra`), `run_both.sh`. Each agent runs in a fresh `/tmp` dir with only the data file, so it has no chat history or repo access. Results: `agent_tree/runs/<agent>/output/{tree.json,desiderata.json,notes.md}`; `validate.py` checks them.
- `to_pipeline.py <agent>` converts an agent's output into `out/pooled_episode_agent_<agent>/{3_merged_tree.json,4_desiderata.json,...}` (refuses to overwrite if steps 5-8 results already exist there).
- `build_compare.py` adds the agent trees to `tree_compare.html`.

**Steps 5-8 and 10** (root of `new_extraction/`)
| step | file | what it does |
|---|---|---|
| 5 visits | `visits.py` | each edit is a walk down the tree; at every decision node on it the LLM reconstructs from what was visible before the edit (earlier edits, scores, change summary) which checks were settled (yes / no / not_checked) and in what order. Round 1 may propose `new_checks`; they are merged per node and added to the registry, and round 2 re-annotates the affected edits. Each edit is annotated on its own: it sees the text of the expert's earlier edits but not their annotations |
| 6 scores | `scores.py` | an LLM writes an importance and a direction per check from ≤10 recorded visits |
| 7 enough / order | `scores.py` | with those scores: lower quartile of the leader's probability / margin = "enough", median number of checks, checks ordered by how often they came first |
| 8 returns | `returns.py` | a return = an expert comes back to a node and takes an option passed over earlier; trigger tallied from the preceding edits |
| 10 export | `export.py` | the files an agent reads: `application/taxonomy.md` (tree only: names, ids, decide/desiderata lines), `application/attention/<node>.md`, `application/evidence/registry.md`, `application/cases/<node>.md` |

### Running
```bash
python run.py                                   # method A + 5-8 + 10 on all 7 competitions
python run.py --suffix _x --from 5 --to 8       # steps 5-8 on an existing out/pooled_episode_x/
python run.py --suffix _x --from 10             # export only
```
Results go to `out/pooled_episode[_suffix]/` (`1_…` to `8_…` json, `application/`). Every LLM stage caches its answers in jsonl files, so an interrupted run resumes; delete the stage's files to redo it. To use method B for steps 1-4:
```bash
cd agent_tree && ./run_both.sh                              # or run_codex.sh / run_claude.sh
python to_pipeline.py codex                                 # writes out/pooled_episode_agent_codex/{3_merged_tree,4_desiderata}.json
cd .. && python run.py --suffix _agent_codex --from 5 --to 8 && python run.py --suffix _agent_codex --from 10
```
Cross-file conventions: item id `<ep_id>#<k>` (`<kernel>:e<n>#<k>`), step id `<kernel>:<v_old>-><v_new>`, tree node ids `T.<i>…`, registry check ids `E<nn>`.

Time and cost (7 competitions × 10 experts): clustering several thousand short calls, desiderata/scores ~100-150 each, visits ~3,000 calls per round (two rounds); roughly 2.5-4 h with `model.workers: 32`, dominated by the visit rounds.

### Configuration (`config.yaml`)
`scope` (competitions, experts per competition), `items.mode` (`episode` | `label`), `cluster` (target ratios, merge thresholds), `visits.new_checks`, `scores` (temperature, `min_visits`), `model`, `stage_models` (stronger model for desiderata and visits), `embedding`, and the `task:` slots. All prompts are in `prompts.py` and use `<<slot>>` placeholders filled from `task:`, so they carry no task-specific wording.

### Comparing trees: `tree_compare.html`
Open it in a browser. Checkboxes choose which trees are shown (`bu` = bottom-up, `mg` = merged, plus one per agent); search, expand-depth buttons and the item/desiderata details work on all of them. `tools/make_tree_compare.py` makes the base page; run `agent_tree/build_compare.py` after it (and after every new agent run) to add the agent trees.

## Application: does the memory help an agent? (`new_extraction/application/`)
An agent gets an expert's code version, the task description and a summary of the earlier versions, and revises the code to improve the score. It writes `revised_code.py` and `report.json` (one yes/no item per observation or check, in the order made, and a summary of the changes). Three conditions share one prompt (`prompt.md`):
- `memory`: plus an instruction and the `memory/` folder (`taxonomy.md` and `attention/` of the Codex tree; no `cases/`, no `evidence/`);
- `no_memory`: the shared prompt only;
- `traceml_instruction`: plus the TraceML planning block (`planning_instruction.md`).

Agents: Codex `gpt-6-astra` and Claude Code `claude-fable-5-1` (same reasoning effort, `AGENT_EFFORT`, default medium), each in an isolated temp dir with its own `CODEX_HOME` / no settings, 10 minutes per run, at most 4 runs at once and never two on the same case.
- `select_cases.py` → `cases/cases.json`: 3 steps per competition, preferring large score improvements (not from a broken starting run, not a pure re-run, ≤2 per expert; ranzcr includes expert 13848868). The gold step is stored in the case file but never shown to the agent.
- `tasks/<comp>.md`: task descriptions (MLE-bench `description.md` where it exists; amex, commonlit and equity still need the Kaggle text pasted in; only competitions with a pasted description are run).
- `python run_application.py --prepare | --print-prompt CASE COND | --run [--agents] [--cases] [--conditions] [--workers 4] [--minutes 10]`; results in `runs/<agent>/<case>/<condition>/` with a `meta.json` (time, timeout, outputs found).

## Known limitations
- **Step 5 is inference.** TraceML records the edit summary and the score, not what the expert looked at; `not_checked` mixes "did not look" with "cannot be told from the summary". Annotations of one expert's edits are independent, so a check settled earlier is not carried to later visits of the same node.
- Checks come from the LLM prior plus a few edit summaries per node; some are generic, and proposals added in step 5 are often near-duplicates.
- The alternatives check flags many nodes (children that are not clean alternatives); it is recorded, the tree is not repaired.
- Attention statistics pool visits of all competitions and experts; scores (step 6) are LLM-guessed; nodes with < ~10 visits are indicative.
- The memory used in the application experiment was built from the same experts whose steps are used as test cases; a clean comparison needs a memory that excludes the case's expert.
- Visits of a competition's experts use that competition's description, but clustering and matching see only the competition-agnostic *general* rationale, so actions from different competitions can share a cluster by design.

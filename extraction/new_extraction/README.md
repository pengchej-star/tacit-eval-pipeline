# new_extraction — tacit-knowledge extraction from expert trajectories

> **Changes on Nov 7 (Pengcheng)**: step 5 now annotates each (edit, decision node) with the answer masked, shuffles the checks, can show the notebook at v_old (`paths.notebooks`), and the level-0 merge cap is 0.38. `visits.masked: false` in config.yaml runs the original Nov 4 step 5 unchanged. See `../HANDOFF.md`, or `git diff cc38323 e3347ed -- extraction/new_extraction` for the exact changes.

Implements "3a Extraction" of the *Tacit Knowledge Representation* proposal (Tacit_new.pdf, "Envisioned implementation"): from many experts' version histories it builds

1. a **taxonomy** of what can be done (a decision tree: decision → options → … → actions), from two directions (LLM prior + observed expert actions), and
2. an **attention map** per decision node: what experts checked before choosing, in what order, how much was enough, and when they came back.

Everything needed to run is in this folder (code, inputs in `data/`, prompts). The only external dependency is an LLM endpoint.

## 1. Quick start
```bash
pip install -r requirements.txt            # python >= 3.10
cp .env.example .env                       # put LITELLM_API_KEY in it (OpenAI-compatible proxy, URL in config.yaml)
python run.py                              # all 7 competitions, 10 experts each (see §4 for time/cost)
python run.py --comps ranzcr-clip-catheter-line-classification,commonlitreadabilityprize --n-experts 2 --suffix _smoke   # small trial
python run.py --from 5                     # resume/re-run from step 5 (earlier results are cached in out/)
```
Results go to `out/pooled_episode[_suffix]/`. Every LLM stage caches its answers in jsonl files there, so an interrupted run resumes where it stopped; to redo a stage, delete its files (table in §3).
The LLM is called through LiteLLM (`litellm.api_base` and `model.generator` in `config.yaml`, default `wine-claude-opus-4-6`); embeddings (`embedding.model`) through the same proxy. If the proxy keeps failing, the same model is tried on Azure AI Foundry when the `AZURE_OPENAI_*` variables are set.

## 2. Inputs (`data/`)
| file | content | origin |
|---|---|---|
| `selection.csv` | the top 10 experts (Kaggle notebook authors) of each of 7 competitions, ranked by best public score | TraceML human trajectories |
| `actions.parquet` | per version→version edit of these 70 experts: TraceML action labels (`fine_actions`), `goal_nl`, `diff_summary` (the code-change summary), magnitude | TraceML `paired/action.parquet` |
| `scores.json` | public leaderboard score of every notebook version | TraceML trajectories |
| `episode_items.jsonl` | the experts' trajectories segmented into episodes, with one *instance* and one *general* rationale (goal / context / action) per item | earlier episode pipeline |
| `topdown_skeleton.json` | the top-down tree used for the reported run (written by the LLM, no competition information in its prompt) | step 1 |
| `tasks.yaml` (folder root, not in data/) | per competition: name, score direction (max/min), description | hand-written |

`tools/build_data.py` shows how `data/` was cut from the raw sources (only needed to rebuild). **No raw notebook code or diff is read anywhere**; the LLM only sees TraceML's goal / change summary / labels and the leaderboard scores.
Competitions: ranzcr-clip-catheter-line-classification, amex-default-prediction, commonlitreadabilityprize, equity-post-hct-survival-predictions, google-quest-challenge, hms-harmful-brain-activity-classification, learning-agency-lab-automated-essay-scoring-2 (3393 transitions, 2019 with a score; scores are signed so that `delta > 0` always means improvement, also for lower-is-better metrics).

## 3. Pipeline (all competitions are processed together)
Order: skeleton → items of **all** competitions pooled → **one** bottom-up clustering → match to the skeleton → desiderata → visit records of all experts → scores. No competition is extracted on its own or merged into another's tree.

| step | file | what it does | output in `out/pooled_episode/` |
|---|---|---|---|
| 1 top-down | `topdown.py` | LLM writes the tree "what can one change to improve a solution" (4 levels, no task data). Reuses `data/topdown_skeleton.json` if present | `1_topdown.json` |
| 2a items | `items.py` | episode mode (default): one item per episode rationale, clustered on its **general action** text. `--mode label`: one item per edit from TraceML labels + change summary (works, not used for the reported run) | `2a_items.json` |
| 2b clustering | `cluster.py` | edits → actions → decisions, recursively: average-linkage on embeddings; close pairs merge, grey-zone pairs are put to the LLM ("same action?" at level 0, "alternatives in the same decision?" above, "same branch?" higher); "no" is a cannot-link; clusters with low-confidence merges are reviewed and may be split; each cluster is named by the question it answers | `2b_bottomup.json`, `2b_pairs_*`, `2b_review_*` |
| 3 merge | `merge.py` | LLM matches every action to a skeleton node (exact / broader / none). Exact matches fill that node; the rest become new nodes under the right decision; skeleton branches nobody visited stay as empty options. Then an LLM checks that each node's children are real alternatives (recorded, not repaired) | `3_merged_tree.json`, `3_action_map.json`, `3_match.jsonl`, `3_check.jsonl` |
| 4 desiderata | `desiderata.py` | per decision node the LLM sees the options and the experts' edits under them and writes yes/no checks ("what would you need to know to choose among these") with how to observe them; checks are deduplicated into a shared registry | `4_desiderata.json` |
| 5 visits | `visits.py` | each edit is a walk down the tree; at every node on it the LLM reconstructs, from what was visible before the edit (earlier edits, scores, change summary), which checks were settled (yes / no / not_checked) and in what order. **Round 1** may also propose `new_checks`; they are merged per node (same as existing / same as another / rejected as generic), added to the registry (`origin: visits`), and **round 2** re-annotates the affected edits against the full list | `5_visits.json`, `5_new_checks.json`, `4_desiderata_base.json` (list before the additions) |
| 6 scores | `scores.py` | an LLM reads each node, its checks and ≤10 recorded visits and writes an importance and a direction per check (the only scoring method kept) | `6_scores.json` |
| 7 enough / order | `scores.py` | with those scores, rank the options at each visit using only the checked items; lower quartile of the leader's probability / margin = "enough" threshold; median number of checks; order checks by how often they came first | `7_enough.json` |
| 8 returns | `returns.py` | a return = an expert comes back to a node and takes an option passed over earlier; trigger tallied from the preceding edits (regression after a single / bundled change, k scored steps without a new best, …) | `8_returns.json` |
| stability test (PDF step 3) | `stability.py` | build the bottom-up tree from half of the experts and from the other half (rank parity) and compare which skeleton nodes are populated at depth 1–3 | `9_stability.json` |
| export | `export.py` | the files an agent would read | `application/` |

`application/`: `taxonomy.md` (the tree with decisions, options, desiderata, empty/new markers), `attention/<node>.md` (check first / then / more, enough-when, come-back-when, loaded one node at a time), `evidence/registry.md` (one definition per check), `cases/<node>.md` (past applications: expert, versions, evidence state, score change; majority state per check for multi-edit items).

Cross-file conventions: item id `<kernel>:e<n>#<k>`; step id `<kernel>:<v_old>-><v_new>`; tree node ids `T.<i>…` (skeleton) and `….n<k>` (added from data); registry check ids `E<nn>`.

## 4. Cost and time (reported run: 7 competitions × 10 experts)
~1674 episode items → ~700 actions; ~3000 edits annotated per round. LLM calls: clustering several thousand short calls, desiderata/scores ~100–150 each, visits ~3000 per round (two rounds, long outputs). Expected wall time with `model.workers: 32`: roughly 2.5–4 hours, dominated by the two visit rounds, then the stability test and the (serial-round) clustering. The proxy took 64 parallel calls in a test without errors; lower `model.workers` if you see rate limits.

## 5. Configuration (`config.yaml`)
- `scope`: `comps` (null = all in `tasks.yaml`), `n_experts` per competition. `items.mode`: `episode` | `label`.
- `cluster`: target ratios, `auto_merge` / `max_dist` (cosine distance thresholds for level 0 and higher), `max_levels`, `root_k`.
- `visits.new_checks`: switch the check-discovery/round-2 mechanism off.
- `scores`: softmax temperature of `ranking_now` (hand-set), `min_visits` for a threshold.
- `model`: model name, temperature, workers, retries. `embedding`: embedding model.
- `task:` the **prompt slots** (see §6).

## 6. Using the prompts for another task
All prompts are in `prompts.py` and contain no task-specific wording; they use placeholders `<<name>>` that `common.fill` takes from `config.yaml → task:` (domain, actor, artifact, what an "edit" is, the objective, the progress signal, areas to cover, evidence sources, and a few example actions used to show the expected granularity). To extract from another kind of task, change those values and supply that task's `actions.parquet`/`episode_items.jsonl`/`scores.json` in the same format (and a `tasks.yaml` entry). The Kaggle/TraceML specifics live only in `data.py` and `items.py`.

## 7. Known limitations
- **Step 5 is inference.** TraceML records the edit summary and the score, not what the expert looked at. `not_checked` is the default and mixes "did not look" with "cannot be told from the summary". Without raw code the LLM is more conservative than with it.
- Step 4's checks come from LLM prior plus a few edit summaries per node, so some checks are generic; step 5 adds missing ones but proposals are often near-duplicates and concentrate at the root.
- The alternatives check flags many nodes (most "decision" nodes contain children that are not clean alternatives); it is recorded in `check` on each node, the tree is not repaired.
- Attention statistics pool visits of all competitions and of all experts by visit (an expert who passes a node often counts more); `expert_vote_top_prob_q25` in `7_enough.json` is the per-expert variant. Thresholds are not yet split by expert tier or competition stage.
- Scores (step 6) are LLM-guessed: the counted and no-score variants and their held-out comparison were removed. Numbers at nodes with < ~10 visits are indicative.
- Stability test covers the split of experts only (not the "more competitions" or BLADE legs of the proposal).
- Visits of a competition's experts are annotated with that competition's description, but clustering and matching see only the competition-agnostic *general* rationale, so actions from different competitions can end up in the same cluster by design.

## 8. Folder map
`run.py` (entry), `common.py` (config, LLM client with proxy→Azure fallback, embeddings, caching helpers), `prompts.py`, `data.py`, `items.py`, `topdown.py`, `cluster.py`, `merge.py`, `desiderata.py`, `visits.py`, `scores.py`, `returns.py`, `stability.py`, `export.py`, `config.yaml`, `tasks.yaml`, `data/`, `tools/build_data.py`, `out/` (results; `embed_cache.json` is an embedding cache shared by runs), `archive_old_runs/` (results of earlier, superseded versions of this pipeline — LLM-tagged intents, competition-by-competition runs, 2-expert smoke runs; kept for reference, safe to delete).

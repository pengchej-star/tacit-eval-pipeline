# Knowledge the agents took in the 9 large-delta episodes (Nov 26)

Input for the turn-level question (Zheyuan): without the cheatsheet, did the agent miss the expert's ("gold")
knowledge, and with the cheatsheet, did it find it? If it did not find it, where did retrieval go wrong?

**Runs.** These are the 9 episodes from Yaqing's Nov 19 slide ("Experts' transitions with large delta"). Each was run
with Claude Code using Opus 5.5 and Haiku 5.5, with and without the cheatsheet: 36 runs, 35 with a result. The
missing run is hms 53762022 Opus without the cheatsheet, which was put on hold.
- Prompt: one step (`src/app_iterate_prompt_onestep.md`), 30 min cap, one run per cell.
- Inputs: the agent starts from the expert's start version, with whatever inputs could still be downloaded.
- Cheatsheet: Yaqing's leave-one-out memory with the episode's own competition left out
  (`memory_leave_one_out/<comp>`).
- Scores are on our MLE-bench split. The commonlit scores are inflated by leakage: the checkpoints were trained on
  Kaggle's full train set.

## Files

| file | what |
|---|---|
| `results/large_delta_knowledge/runs.csv` | one row per run: status, score, the agent's change, its tree node, match with the gold, cheatsheet files and nodes opened, knowledge the agent reports, its own action summary, run dir |
| `results/large_delta_knowledge/summary.md` | the three tables below |
| `triage/large_delta_gold.csv` | per episode: the expert's next step, the gold nodes, whether the gold step was possible with the agent's inputs |
| `triage/large_delta_run_labels.csv` | per run: the agent's change, its node, match (yes / partial / no / na) |
| `src/large_delta_knowledge.py` | builds the first two from the run dirs and the two label CSVs |

Rebuild with `python src/large_delta_knowledge.py`. Add `--episodes .../new_extraction/data/episode_items.jsonl` to
also write Yaqing's 9 episodes verbatim to `gold_items.jsonl`, which stays out of git.

## How the labels were made

- **Gold.** The gold is what the expert did in the episode: the change log of each step, and Yaqing's knowledge items
  for the episode (`episode_items.jsonl`, `ep_id` in the gold CSV).
- **Gold nodes.** I placed the gold in that competition's leave-one-out tree. Node ids are local to each tree:
  T.5.1 in hms is a different node from T.5.1 in commonlit.
- **Labels are hand-made, not from an automated judge.** Claude read each report and tree and wrote the labels
  (Nov 26). Please check the ones you rely on.
- **What a run is compared against.** The prompt allows one change. A run is "yes" if its change is the expert's
  next step, or the episode's main lever. It is "partial" if it took the gold node with a different setting, or a
  sibling option under the same parent.
- **"Opened gold node / branch."** This comes from the files the agent actually opened, taken from its transcript
  (`memory_reads`). It does not come from what the agent says it used.
- **taxonomy.md itself lists every node and its one-line desiderata.** So an agent can pick a node without opening
  any attention or case file. Four cheatsheet runs did exactly that.

## Findings

1. **The gold step was possible in only 2 of 9 episodes:** gquest 7253130 and hms 52200959.
   - In 2 more, the inputs forced it. For ranzcr 13521245, every agent had to switch to the expert's new
     checkpoint. For hms 52551258, v2's own checkpoint is missing, so the agent has to build from other ones.
   - In commonlit 18423958 it was partly possible.
   - In the other 4 it needed checkpoints that are private or that would have to be trained: commonlit 18426209,
     hms 49524919, 53762022 and 50496431.

   A miss in those 4 says little about the knowledge.
2. **Matches, cheatsheet vs no cheatsheet:**
   - Opus: 4 ✓ and 2 ~ with the cheatsheet, against 3 ✓ and 1 ~ without (8 runs without, since one has no result).
   - Haiku: 2 ✓ with, against 1 ✓ without.

   The cheatsheet moved the choice toward the gold in 4 pairs:
   - ranzcr Opus;
   - gquest Opus (gold node, but a different setting, and the lowest score of the four);
   - hms 52200959 Haiku (picked from taxonomy.md alone; the run did not finish);
   - hms 50496431 Opus (gold parent node).

   It moved the choice away in 2 pairs: hms 49524919 Opus and hms 50496431 Haiku. With one run per cell, this is
   not a measurable effect.
3. **Restore bias.** 17 of 35 runs chose a "restore" option: revert to the last verified configuration, or restore
   validated ensemble members (T.2.1.3, T.2.2.2, T.5.1.4).
   - This was the gold when the expert also restored: commonlit 18423958 and hms 52200959.
   - It was the wrong branch where the expert built forward instead:
     - 18426209: add a new member;
     - 53762022: rebuild the weak model's pipeline;
     - 50496431: add a new model family.

   The history the agent sees shows a recent regression in all of these. With or without the cheatsheet, both
   models take that as "undo it". The cheatsheet reinforces this: T.5.2.2 "retain the smaller backbone",
   T.2.2.2 and T.5.1.4 are what the agents opened and cited.
4. **The misses are retrieval misses, not application misses.**
   - None of the 10 cheatsheet runs labelled ✗ opened the gold node. 4 of them opened a node in the right top-level
     branch.
   - The 2 partial runs opened the gold node or its parent and then picked a different setting or a sibling option.
   - Agents open 1–3 nodes and stop. Haiku often reads only taxonomy.md.
5. **Score vs gold.** Matching the gold did not track score. Where scores exist, the four cells of an episode are
   usually within noise of each other. For example: gquest 0.423–0.458; ranzcr 0.865–0.868; hms 49524919
   0.868–0.889.

## Tables

### Per episode: the expert's step and what each agent chose

Each cell shows: match with the gold (✓ yes, ~ partial, ✗ no) · the agent's node · score on our split.
Lower is better for commonlit and hms. FAIL / TIMEOUT means the revised code did not produce a submission.

| case | expert's next step | gold nodes | gold possible? | Opus no | Opus cheat | Haiku no | Haiku cheat |
|---|---|---|---|---|---|---|---|
| commonlit 18423958 v4->v8 | revert ALBERT-large to RoBERTa-base (v3 setup), then add T5 / DistilBERT members and tune blend weights | T.2.1.3, T.5.2.2, T.6.1.1, T.6.2.2.2 | partial | ✓ T.2.1.3 · 0.299 | ✓ T.2.1.3 · 0.299 | ✓ T.2.1.3 · 0.299 | ✓ T.2.1.3 · 0.299 |
| commonlit 18426209 v3->v5 | equal blend weights, then add a new mean-pooling member; leave the broken large swap | T.6.2.2.1, T.6.1.1 | no | ✗ T.2.1.3 · 0.235 | ✗ T.2.1.3 · 0.235 | ✗ T.2.1.3 · 0.235 | ✗ T.2.1.3 · 0.235 |
| gquest 7253130 v3->v5 | lr 3e-5 -> 1e-5 and dropout 0.2 -> 0.1, then dropout back to 0.2 | T.5.3, T.5.2 | yes | ✗ T.7.2 · 0.458 | ~ T.5.3 · 0.423 | ✗ T.3.4.3 · 0.430 | ✗ T.4.4.1 · 0.426 |
| hms 49524919 v54->v55 | add a 2D EfficientNet spectrogram family to the 1D EEGNet folds | T.5.1.1 | no | ~ T.5.1.5 · 0.868 | ✗ T.6 · 0.869 | ✗ T.5.3 · 0.887 | ✗ T.6 · 0.889 |
| hms 52551258 v2->v3 | replace FastViT with an ensemble of EEG CNN-RNN checkpoints + filtering, one refactor | T.4.1.1, T.5.1.1 | forced | ✓ T.4.1.1 · 1.052 | ✓ T.4.1.1 · 0.876 | ✗ T.6 · FAIL | ✗ T.6 · TIMEOUT |
| hms 53762022 v8->v9 | after a single-model diagnostic, rebuild that model's pipeline (features, group folds) instead of returning to the blend | T.2.4.2, T.3.1, T.5.1.3 | no | – no result | ✗ T.5.1.4 · 0.857 | ✗ T.5.1.4 · FAIL | ✗ T.5.1.4 · FAIL |
| hms 52200959 v34->v38 | remove os._exit so all three families run, then weights from (1 - LB) | T.5.1.4, T.5.3.2 | yes | ✓ T.5.1.4 · FAIL | ✓ T.5.1.4 · 0.515 | ✗ T.5.2.3 · TIMEOUT | ✓ T.5.1.4 · TIMEOUT |
| ranzcr 13521245 v6->v10 | better checkpoint + matching test resize, then a resize sweep | T.5.3, T.1.1.3, T.4.3.4 | forced | ✗ T.7.3.4 · 0.868 | ✓ T.1.1.3 · 0.865 | ✗ T.7.3.4 · 0.868 | ✗ T.7.3.4 · 0.868 |
| hms 50496431 v29->v32 | drop in-notebook spectrograms, add NetOneImage (EfficientNet-B3), re-run once | T.5.1.1, T.2.3, T.1.10 | no | ✗ T.2.2.2 · 0.762 | ~ T.5.1.4 · 1.410 | ~ T.1.6 · FAIL | ✗ T.2.2.2 · FAIL |

Node names for each tree are in `runs.csv` (`gold_nodes`, `agent_node`). Notes on each cell are in
`triage/large_delta_run_labels.csv`. Some cells need that context: for example, the ranzcr agents that added TTA had
already done the expert's step as a required fix, and the hms 50496431 Opus scores come from fallbacks.

### Counts (runs with a result)

| | match ✓ | partial ~ | no ✗ | same top-level branch as gold |
|---|---|---|---|---|
| Opus, no cheatsheet | 3 | 1 | 4 | 5 of 8 |
| Opus, cheatsheet | 4 | 2 | 3 | 7 of 9 |
| Haiku, no cheatsheet | 1 | 1 | 7 | 5 of 9 |
| Haiku, cheatsheet | 2 | 0 | 7 | 4 of 9 |

### Cheatsheet runs: did the agent open the gold part of the tree?

See `results/large_delta_knowledge/summary.md` (third table) or the `memory_nodes_opened`, `opened_gold_node` and
`knowledge_reported` columns of `runs.csv`.

# TraceML dataset notes (Phase 1)

Inventory of the HF dataset [`jerryyan/TraceML`](https://huggingface.co/datasets/jerryyan/TraceML),
pinned at revision `6472e74ba6393d4b87bb7ff8e4246e154d359b20` (checked 2026-10-08).
Everything below was computed from the downloaded files unless marked *unverified*.

## 1. Where things live (Babel)

| What | Path |
|---|---|
| conda env (Python 3.11.16) | `/data/user_data/pengchej/software/anaconda3/envs/tacit-eval` |
| mle-bench clone (commit `507f92e`, LFS pulled, 322 files) | `/data/user_data/pengchej/src/mle-bench` |
| TraceML toolkit clone (commit `202cc49`) | `/data/user_data/pengchej/src/TraceML` |
| HF download (parquet, json, tarball) | `/data/user_data/pengchej/traceml/hf/` |
| full tarball listing (`tar -tzvf`) | `/data/user_data/pengchej/traceml/tar_listing.txt` |
| extracted human notebooks (6.1 GB, 178,598 files) | `/data/user_data/pengchej/traceml/extracted/human/` |
| MLE-bench data dir (empty until Phase 3) | `/data/user_data/pengchej/mlebench-cache` |

Commands used:

```bash
source /data/user_data/pengchej/software/anaconda3/etc/profile.d/conda.sh
conda create -y -n tacit-eval python=3.11 && conda activate tacit-eval
git clone https://github.com/openai/mle-bench.git && (cd mle-bench && git lfs fetch --all && git lfs pull)
git clone https://github.com/JerryYan123/TraceML.git
pip install -e ./mle-bench && pip install -e ./TraceML && pip install huggingface_hub pyarrow pandas nbconvert

export HF_HOME=/data/user_data/pengchej/hf-home
REV=6472e74ba6393d4b87bb7ff8e4246e154d359b20; OUT=/data/user_data/pengchej/traceml/hf
hf download jerryyan/TraceML --repo-type dataset --revision $REV --local-dir $OUT \
   --include "extras/*" "manifests/*" README.md DATASHEET.md
hf download jerryyan/TraceML data/{paired,humans_only,experiment_run}/{state,action}.parquet \
   --repo-type dataset --revision $REV --local-dir $OUT
hf download jerryyan/TraceML trajectories_human.tar.gz --repo-type dataset --revision $REV --local-dir $OUT
sha256sum $OUT/trajectories_human.tar.gz   # d44c8a08...39f9cf, matches the HF LFS sha256
tar -tzvf $OUT/trajectories_human.tar.gz > tar_listing.txt   # inspected before extracting
tar -xzf  $OUT/trajectories_human.tar.gz -C extracted --no-same-owner --no-same-permissions
```

Not downloaded (not needed yet): `models/` (2 × 3.4 GB Qwen3 labelers), `trajectories_experiment_run/`
(~1.1 GB agent runs), `trajectories_toolkit_demo/`, `code/`.

## 2. Files and columns

### `data/{split}/state.parquet`: one row per version

| split | rows | content |
|---|---:|---|
| `paired` | 15,206 | 7 comps; 13,692 human rows (430 kernels) + 1,514 agent rows (codex 488, mlevolve 1,026) |
| `humans_only` | 135,791 | 127 other comps; 4,035 human kernels |
| `experiment_run` | 3,852 | 30 Codex gpt-5.4-mini runs on the 7 paired comps |

Columns (same in all three splits):
`key_id, version_number, comp, group, track, model, coarse_tags, fine_tags, summary, keywords, score,
branch_id, depth, stage, orig_version_number, is_best_branch, is_agent, node_id, parent_id, edge_kind,
tree_id, ctime, score_public, score_private, submission_id, submission_date, is_valid_submission,
kernel_id, version_id, raw_code_path, alt_parents_json`

- `group`: author tier for humans (`Contributor / Expert / Master / Grandmaster`, 23 rows `?`),
  agent scaffold for agents (`codex`, `mlevolve`).
- `track` / `model`: which labeler produced the tags (`llm_v3` + `gpt-5-mini-2025-08-07`, or
  `qwen3_1.7b_distill` + `final`). These are about the *labels*, not the code.
- `raw_code_path`: absolute path on the authors' server
  (`/usr1/data/weiwei/jerry/.../kaggle_kernels/kernels/<kernel_id>/versions/vNNN.ipynb`). Not usable
  directly, but it tells you whether a code file exists (see §3).

### `data/{split}/action.parquet`: one row per transition `v_old → v_new`

Rows: paired 14,726, humans_only 133,125, experiment_run 3,822. Columns:
`key_id, comp, group, v_old, v_new, model, coarse_actions, fine_actions, intents, magnitude, score_effect,
goal_nl, diff_summary, score_old, score_new, orig_v_old, orig_v_new, depth_old, depth_new, stage_old,
stage_new, is_best_branch, is_agent, edge_kind, edge_kind_label, parent_node_id, child_node_id,
parent_kernel_id, child_kernel_id, tree_id, ctime_old, ctime_new`

### `extras/`

| file | rows | columns |
|---|---:|---|
| `kernels.parquet` | 4,847 | `kernel_id, kernel_slug, comp, author_user_id, author_username, author_tier, score_is_max, best_public_score, best_private_score, private_rank, percentile, medal, version_count, raw_dir, n_versions, span_days, chain_n_versions, chain_span_days, n_scored, score_range, n_substantive, line_range, is_rich_iter, license, license_verified_via` |
| `trajectory_index.parquet` | 4,665 (4,465 human + 200 agent) | `key_id, comp, group, is_agent, is_best_branch, n_versions, n_scored, min_score, max_score, tree_id, n_branches, max_depth` |
| `nodes.parquet` | 174,558 | `node_id, tree_id, comp, kernel_id, version_id, version_in_kernel, ctime, date, depth, branch_id, parent_id, edge_kind, score_public, score_private, is_valid_submission, score_kind, submission_id, submission_date, author_tier, author_username, best_private_score, score_is_max, medal, total_lines, raw_code_path, alt_parents_json` |
| `edges.parquet` | 3,995,719 | `parent_id, child_id, edge_kind, sim` |
| `trees.parquet` | 2,721 | `tree_id, comp, n_nodes, n_kernels, n_branches, max_depth, n_roots, roots_json` |

### `manifests/`

- `competitions.json`: dict keyed by comp slug, **141 entries**, each with
  `name, year, deadline, launch, task_type, metric, score_direction, {gold,silver,bronze,median}_threshold`.
  Only **134** of them have trajectories. The 7 with none: `ai4code, google-gemma-3n-hackathon,
  landmark-recognition-2019, leash-belka, med-gemma-impact-challenge, openai-to-z-challenge, youtube8m-2018`.
  Metadata quality varies: `task_type` is empty for many comps, and some `metric` values are bare Kaggle
  metric IDs (e.g. `39244296` for lmsys-chatbot-arena).
- `filter_rules.json`, `license_verification_log.json`, `pii_redaction_log.json`, `schemas/` (state/action
  schemas + fine-tag vocabularies).

## 3. Tarball layout and the `(key_id, version_number)` → file mapping

`trajectories_human.tar.gz` (2.96 GB compressed, 8.4 GB raw; 178,598 files, all regular files or dirs,
no symlinks, absolute paths or `..`):

```
human/<kernel_id>/meta.json          # Kaggle kernel metadata (slug, url, author, comp, medal, best scores)
human/<kernel_id>/trajectory.json    # per-version list: version_id, version_number, date, total_lines,
                                     #   lines_inserted/changed_from_prev, running_time_ms, linked_score{public,private}
human/<kernel_id>/versions/vNNN.ipynb  # 167,410 files (nbformat 4, outputs stripped)
human/<kernel_id>/versions/vNNN.py     #   1,494 files (script kernels)
```

4,847 kernel dirs (= rows of `kernels.parquet`). `NNN` is always zero-padded to 3 digits.

**Mapping (verified on all 149,483 human state rows):**

```
file = extracted/human/{key_id}/versions/v{version_number:03d}.ipynb   # or .py if no .ipynb
```

- For humans, `key_id == kernel_id` (100% of rows).
- `version_number == orig_version_number` (100%); no renumbering for humans.
- `raw_code_path` agrees with this rule in 100% of rows where it is set (kernel dir and `vNNN`).
- **`raw_code_path` is null ⇔ there is no code file in the tarball.** 148,530 / 149,483 human rows
  have a file; the 953 without are concentrated in 37 kernels (26 kernels missing from the tarball
  entirely, 11 kernels missing individual versions).
- 29 kernels have both `.py` and `.ipynb` files (never the same version number).
- The tarball holds **more** than the state tables: 381 kernels and 20,374 version files have no state row
  (they were dropped by the TraceML filters). They have code but no labels or scores in the parquet.
- Agent rows are **not** in this tarball. `experiment_run` rows have `raw_code_path = versions/vNNN.py`,
  relative to `trajectories_experiment_run/run_*/extracted/`. The 1,514 paired agent rows (codex and
  mlevolve) have no `raw_code_path`, so their code does not seem to be released (*not checked further*).

## 4. How many versions have code

| split | kernels | version rows | rows with code |
|---|---:|---:|---:|
| paired (human) | 430 | 13,692 | 13,411 |
| humans_only | 4,035 | 135,791 | 135,119 |
| all 26 MLE-bench comps | 848 | 24,764 | 24,695 |

**Is the paired split fully covered?** Almost: 13,411 / 13,692 (97.9%). The gaps:

- commonlitreadabilityprize: kernel 17074381 (221 versions) and 18736642 (24): not in the tarball
- equity-post-hct-survival-predictions: kernel 76576022 (34): not in the tarball
- learning-agency-lab-automated-essay-scoring-2: kernel 54558568 v1 and v2 (kernel present, these two files missing)

gquest kernel 6810482 (removed for a label leak) is absent from both the tables and the tarball.

**The 4 paired comps in MLE-bench (notebooks opened and parsed):**

| comp | kernels | versions | with code | non-empty code | median / max code lines | Kaggle-scored versions | Kaggle runtime p50 / p90 (min) |
|---|---:|---:|---:|---:|---|---:|---|
| google-quest-challenge | 37 | 923 | 923 | 923 | 236 / 1,420 | 359 | 9.6 / 98.7 |
| learning-agency-lab-automated-essay-scoring-2 | 61 | 2,269 | 2,267 | 2,267 | 449 / 1,517 | 987 | 8.2 / 95.4 |
| hms-harmful-brain-activity-classification | 58 | 2,385 | 2,385 | 2,385 | 407 / 2,918 | 1,317 | 2.1 / 82.8 |
| ranzcr-clip-catheter-line-classification | 26 | 593 | 593 | 593 | 223 / 754 | 311 | 5.5 / 93.9 |

All 6,168 files parse; 6,163 are notebooks (all Python, 0 outputs left) and 5 are `.py`. "Code lines" =
non-blank lines in code cells. The runtime is Kaggle's `running_time_ms` from `trajectory.json`
(present for 99.9% of these versions). It is a rough guide to cost, not a measurement on our hardware.

Counting the versions filtered out of the state tables too, the tarball has gquest 42 kernels / 1,139 files,
aes2 64 / 2,390, hms 64 / 2,929, ranzcr 26 / 630.

### All paired comps and all MLE-bench comps

| comp | split | MLE-bench | task | metric (dir) | kernels | versions | with code | Kaggle-scored |
|---|---|---|---|---|---:|---:|---:|---:|
| equity-post-hct-survival-predictions | paired | no | tabular | Stratified Concordance Index (race-stratified) (higher) | 99 | 3258 | 3224 | 1587 |
| commonlitreadabilityprize | paired | no | nlp | RMSE (lower) | 103 | 2826 | 2581 | 1265 |
| hms-harmful-brain-activity-classification | paired | yes | cv | Symmetric KL Divergence (lower) | 58 | 2385 | 2385 | 1317 |
| learning-agency-lab-automated-essay-scoring-2 | paired | yes | nlp | Quadratic Weighted Kappa (QWK) (higher) | 61 | 2269 | 2267 | 988 |
| amex-default-prediction | paired | no | tabular | Mean(Normalized Gini, Default Rate at top 4%) (M) (higher) | 46 | 1438 | 1438 | 356 |
| google-quest-challenge | paired | yes | nlp | Mean Spearman correlation (higher) | 37 | 923 | 923 | 359 |
| ranzcr-clip-catheter-line-classification | paired | yes | cv | Macro AUC (multi-label) (higher) | 26 | 593 | 593 | 311 |
| siim-isic-melanoma-classification | humans_only | yes | cv | AUC (higher) | 88 | 2482 | 2472 | 718 |
| petfinder-pawpularity-score | humans_only | yes | cv | RMSE (lower) | 92 | 2152 | 2152 | 833 |
| aptos2019-blindness-detection | humans_only | yes | cv | Quadratic Weighted Kappa (QWK) (higher) | 78 | 1846 | 1846 | 659 |
| rsna-breast-cancer-detection | humans_only | yes |  | ProbFScoreBetaMicro (higher) | 42 | 1241 | 1241 | 469 |
| vesuvius-challenge-ink-detection | humans_only | yes |  | DiceFBeta (higher) | 18 | 1182 | 1182 | 745 |
| siim-covid19-detection | humans_only | yes |  | OpenImagesObjectDetectionAP (higher) | 36 | 1159 | 1159 | 602 |
| ventilator-pressure-prediction | humans_only | yes |  | MAE (lower) | 42 | 1138 | 1138 | 464 |
| rsna-miccai-brain-tumor-radiogenomic-classification | humans_only | yes |  | AUC (higher) | 40 | 1055 | 1055 | 415 |
| plant-pathology-2021-fgvc8 | humans_only | yes |  | FScoreMicro (higher) | 37 | 963 | 963 | 468 |
| us-patent-phrase-to-phrase-matching | humans_only | yes |  | PearsonCorrelationCoefficient (higher) | 35 | 848 | 848 | 484 |
| champs-scalar-coupling | humans_only | yes |  | GroupMeanLogMAE (lower) | 26 | 668 | 668 | 248 |
| uw-madison-gi-tract-image-segmentation | humans_only | yes |  | Dice3DHausdorff (higher) | 25 | 648 | 648 | 306 |
| rsna-2022-cervical-spine-fracture-detection | humans_only | yes |  | WeightedMeanColumnwiseLogLoss (lower) | 14 | 576 | 576 | 355 |
| lmsys-chatbot-arena | humans_only | yes |  | 39244296 (lower) | 14 | 592 | 562 | 25 |
| chaii-hindi-and-tamil-question-answering | humans_only | yes |  | Jaccard (higher) | 21 | 518 | 491 | 300 |
| icecube-neutrinos-in-deep-ice | humans_only | yes |  | MeanAngularError (lower) | 11 | 394 | 394 | 137 |
| google-research-identify-contrails-reduce-global-warming | humans_only | yes |  | 38195349 (higher) | 13 | 362 | 362 | 226 |
| h-and-m-personalized-fashion-recommendations | humans_only | yes |  | MAP@{K} (higher) | 14 | 300 | 300 | 94 |
| seti-breakthrough-listen | humans_only | yes |  | AUC (higher) | 5 | 151 | 151 | 49 |
| alaska2-image-steganalysis | humans_only | yes |  | WeightedAUC (higher) | 7 | 132 | 132 | 53 |
| freesound-audio-tagging-2019 | humans_only | yes |  | WeightedLabelRankingAveragePrecision (higher) | 2 | 95 | 95 | 4 |
| bms-molecular-translation | humans_only | yes |  | LevenshteinMean (lower) | 6 | 92 | 92 | 35 |

"Kaggle-scored" = rows with a non-null `score`, i.e. versions that produced a leaderboard submission on Kaggle.

## 5. Score columns

- **`score` is the Kaggle public leaderboard score**: it equals `score_public` in 100% of the 65,784 human
  rows where it is set, and is null exactly when `score_public` is null. `score_private` (Kaggle private LB)
  is also present. Only 44% of human version rows have a score, because many versions were never submitted.
- Direction comes from `competitions.json → score_direction`.
- **These are not comparable to MLE-bench scores.** MLE-bench re-splits Kaggle's train set into its own
  train/test, so the test set differs. Expert baselines must be re-run in our environment (Phase 4).
- `trajectory.json → linked_score{public,private}` carries the same information per version.

## 6. Open questions / not verified

- Whether the 26 kernels missing from the tarball (e.g. commonlit 17074381) can be fetched from Kaggle
  directly (`kaggle kernels pull`). Not tried.
- Where the code for the 1,514 paired agent rows (codex and mlevolve) lives. It is not in `trajectories_human.tar.gz`
  and `raw_code_path` is null.
- 14 notebook versions in the 4 comps have no kernelspec language metadata. Not inspected; they parse
  and contain code.
- Kaggle runtimes were on Kaggle's GPUs/TPUs. They say nothing direct about runtime on Babel.

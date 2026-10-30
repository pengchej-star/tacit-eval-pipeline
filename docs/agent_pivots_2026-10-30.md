# Agent vs expert at seven pivot points (2026-10-29/30)

This extends the two-case pilot (`docs/agent_pilot_2026-10-29.md`) with five more pivot steps, picked the night
before the group meeting.

Setup is the same as the pilot:
- The agent (Claude Code + Claude Opus 5.5 via the CMU AI gateway) sees the expert's v1..v_k, their Kaggle scores,
  the competition's public data and the expert's attached inputs. It writes v_k+1′.
- Budget: 40 min, $10 cap, one GPU, in a container that hides the answers. No extracted knowledge.
- Expert v_k, expert v_k+1 and agent v_k+1′ are all run and graded on the MLE-bench split, in the same environment
  and the same SLURM job (`slurm/pivot_case.sbatch`).

## Results

| case (pivot) | model in the notebook | metric | expert v_k | expert v_k+1 | **agent v_k+1′** | agent vs expert v_k+1 | agent time / cost |
|---|---|---|---:|---:|---:|---|---|
| hms `49981285` v38→v39 (Expert) | trained in notebook (RF) | KL ↓ | 1.1323 | 1.1177 | **0.9696** | better | 7 min / $0.33 |
| aes2 `54551628` v13→v14 (Contributor) | trained in notebook (TF-IDF+SVM) | QWK ↑ | 0.7064 | 0.7293 | **0.7494** | better | 15 min / $0.50 |
| equity `73937748` v2→v3 (Master) | trained in notebook (GBDT) | C-index ↑ | 0.6750 | 0.6773 | **0.6784** | tie (+0.0011) | 8 min / $0.28 |
| ranzcr `13848868` v34→v35 (Grandmaster) | attached weights | AUC ↑ | 0.9656 | 0.9707 | **0.9714** | tie (+0.0007) | 3 min / $0.23 |
| ranzcr `15173072` v16→v17 (Contributor) | attached weights | AUC ↑ | 0.9676 | 0.9754 | **0.9883** | better, but see leakage | 3 min / $0.18 |
| ranzcr `15164527` v28→v29 (Expert) | attached weights | AUC ↑ | 0.9858 | 0.9872 | **0.9852** | worse (−0.0020) | 11 min / $0.64 |
| hms `49524919` v7→v8 (Grandmaster) | attached weights | KL ↓ | 0.5048 | 0.6135 | **0.4922** | better; expert step reversed here | 22 min / $0.73 |

Kaggle leaderboard scores of the expert step, for reference:

| case | Kaggle v_k → v_k+1 |
|---|---|
| hms 49981285 | 0.9572 → 0.9172 |
| aes2 54551628 | 0.6839 → 0.7138 |
| equity 73937748 | 0.6762 → 0.6791 |
| ranzcr 13848868 | 0.9484 → 0.9559 |
| ranzcr 15173072 | 0.9522 → 0.9571 |
| ranzcr 15164527 | 0.9606 → 0.9639 |
| hms 49524919 | 0.4984 → 0.4596 |

**The expert's step goes the same direction here as on Kaggle in 6 of 7 cases.** The exception is hms 49524919.

**Run-to-run noise.** Re-running unchanged versions:
- the hms random forest (49981285) moved by 0.004–0.006 KL;
- aes2 54551628 and equity 73937748 reproduced exactly or within 0.001.

**Not run: equity `77450317` (3rd-place solution) v9→v10.**
- v9 needs a third attached dataset, `cibmtr-models`. The notebook metadata gives only its id (6727025), which we
  could not map to a Kaggle dataset.
- Its helper scripts (`!python /kaggle/input/cibmtr-scripts/*.py`) hard-code `/kaggle/input` paths, which our path
  rewrite (notebook code only) does not reach.

Total agent spend for the night was about $3, by Claude Code's own estimates. Five killed runs are not counted;
each was stopped within a few minutes.

## What the agents did

**hms 49981285: a different route, much better.**
- The expert's step changed the train/validation subsampling, the spectrogram blur and the RF's `min_samples_leaf`.
- The agent kept the features and changed how the RF output becomes probabilities. Instead of a hard cluster pick,
  it takes a soft average of k-means cluster centres, weighted by the sharpened `predict_proba`. Both knobs are
  tuned on the validation split.
- This suits KL, which punishes confident wrong picks.

**aes2 54551628: a different route, better.**
- The expert tuned TF-IDF and the SVM.
- The agent replaced the SVC classifier with Ridge regression (rounded to 1–6), since QWK rewards ordinal closeness.
- It also fixed a preprocessing bug: the digit-stripping regex never ran (missing `regex=True`).

**equity 73937748: the same idea as the expert.**
- The expert added LightGBM next to XGBoost and rank-blended them.
- The agent rank-blended tuned XGBoost, CatBoost and LightGBM.

**ranzcr 13848868 (pilot): the expert's exact edits plus flip TTA.**

**ranzcr 15173072: the same fix as the expert, plus a fold ensemble.**
- It reverted v16's normalization mean to the ImageNet values; v16's change had lowered the LB score. That is what
  the expert's v17 did.
- It also ensembled all 5 fold checkpoints with flip TTA, and loaded weights with `strict=True`.
- The extra folds were trained on most of our test images, so part of the +0.013 is likely leakage.

**ranzcr 15164527: worse.**
- The agent read v24–v28 as single-fold probes and went back to v23's full blend (5 folds + 3 single models, rank
  weights). The full blend was the expert's best on Kaggle (0.9681).
- On our split the blend scores below the single-fold versions. That is consistent with leakage favouring
  particular checkpoints, but we have not checked.
- The expert's v29 only fixed the fold-selection condition.

**hms 49524919 (pilot): a 4-set ensemble chosen on saved OOF predictions.**

## Reading

- **The agent matched or beat the expert's next step in 6 of 7 cases.**
- **Clean cases.** In the three where the notebook trains its own model (no leakage), the agent was clearly better
  in two and tied in one. Its routes differed from the expert's in two of the three.
- **None of this supports "expert > agent without knowledge" yet.** Caveats:
  - one agent run per case;
  - attached-weight cases leak, so the four ranzcr/hms-inference rows are weak evidence either way;
  - the clean cases come from Expert/Contributor/Master authors, not Grandmasters;
  - Opus 5.5 is much stronger than TraceML's gpt-5.4-mini.

## Fixes made to run these cases

- **Competition data under the original name.** The runner and the agent workspace also stage the competition data
  under any case-variant folder name the code uses (equity reads `/kaggle/input/equity-post-HCT-survival-predictions`).
- **ranzcr sample_submission.** It is staged with the Kaggle column layout. MLE-bench grades 9 of the 11 classes
  and drops two columns, so notebooks indexing `iloc[:, 1:12]` failed. The grader reads only its 9 classes.
- **Compatibility shims in the GPU env** (`env/kaggle-run-gpu-sitecustomize.py`):
  - the legacy albumentations names (`RandomBrightness`, `RandomContrast`, `Cutout`, `IAA*`);
  - `torch.load` defaulting to `weights_only=False`, as before torch 2.6.
- **Per-case venvs for equity**, so a notebook's `!pip install` does not change a shared env.
- **ranzcr 15164527 needs `ttahara/ranzcr-clip-weights-for-multi-head-model-v2`**, which static triage missed: the
  code builds the path with `Path`.

## Files

- Agent code and notes: `results/agent_pilot/<comp>_<key>_v<k>-v<k+1>/`
- Agent grades: `results/agent_runs.jsonl`
- Expert rows: `results/runs.jsonl` (tag `pivot:expert`)

# Pilot: agent writes the expert's next version at a pivot point (2026-10-29)

Setup:
- The agent (Claude Code + Claude Opus 5.5 via the CMU AI gateway, `wine-claude-opus-5-5`) sees an expert's
  versions v1..v_k: their code and Kaggle scores, the competition's public data and the expert's attached inputs.
  It writes v_k+1.
- It runs in an Apptainer container that hides /home and /data, so it cannot reach the answers
  (`src/agent_step.py`). It has one GPU and a 40-minute budget, and gets no extracted knowledge.
- Its version is then executed and graded exactly like the expert's versions (`run_version.py`, MLE-bench split).
- The two cases are pivot steps (Yaqing's `pivot_labels.csv`) in two of Yaqing's 70 notebooks.

| case | metric | expert v_k | expert v_k+1 | **agent v_k+1** | agent time / cost |
|---|---|---:|---:|---:|---|
| ranzcr `ttahara/ranzcr-multi-head-model-inference` v34 → v35 | AUC ↑ | 0.96561 | 0.97073 | **0.97143** | 3 min, $0.23 |
| hms `gunesevitan/hms-hbac-inference` v7 → v8 | KL ↓ | 0.50482 | 0.61345 | **0.49224** | 22 min, $0.73 |

On Kaggle, the expert's v_k → v_k+1 went 0.9484 → 0.9559 (ranzcr) and 0.4984 → 0.4596 (hms). Costs are
Claude Code's own estimates; the gateway exposes no usage to cross-check them. Agent code and notes:
`results/agent_pilot/`. Grades: `results/agent_runs.jsonl`.

## What each agent did

**ranzcr.**
- The agent read the attached weights' `settings.yml` and found they were trained at 512×512. It noticed that
  the expert's 512 versions (v31/v32) scored best.
- Its v35 makes **the same two edits as the expert's v35**: `IMAGE_SIZE` 640 → 512, and `CONVERT_TO_RANK` off.
- It also adds horizontal-flip TTA, since training used HorizontalFlip.
- Result: 0.0007 above the expert.
- The "knowledge" behind this pivot (infer at the training resolution) was recoverable from files the expert had
  attached.

**hms.**
- The expert's v8 switched to the v1.3 checkpoints and turned on flip TTA.
- The agent instead ensembled all four 5-fold model sets in the attached dataset (20 models). It chose this by
  scoring the out-of-fold predictions the training runs had saved: OOF KL 0.635 for all four sets, against 0.741
  for the best single set.
- It also added per-spectrogram caching and an fp32 fallback for a NaN from fp16.

## Caveats

- **One run per case.** Agent runs vary, so these are anecdotes, not estimates.
- **Leakage.** All weights here were trained on Kaggle's full train set, which contains the MLE-bench test rows.
  Absolute scores are inflated. On hms the expert's own step even reverses direction here (better on Kaggle,
  worse on our split), so hms is not a usable human baseline.
- **Inference-only pivots with rich attached inputs** (configs, OOF files) give the agent much of the information
  the expert had. Pivots that need choices not visible in the files may separate human and agent more.
- **Opus 5.5 is a much stronger model than TraceML's gpt-5.4-mini.**

So far there is no sign that the expert's next step beats the agent's at these pivots. Testing the hypothesis
(expert > agent without knowledge, agent + knowledge ≈ expert) needs:
- more cases;
- repeated agent runs;
- a weaker or knowledge-free baseline model (e.g. gpt-5.4-mini, also on the gateway);
- clean (training) or Kaggle-graded cases.

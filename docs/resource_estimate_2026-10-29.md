# Compute needed to run the expert notebooks (estimate, 2026-10-29)

Question from the team: if we run the human expert code as it is, especially the best-scoring version of each of the
top-10 notebooks per competition (Yaqing's 70 kernels, `triage/selection.csv`), what resources do we need and how
long will it take? And what if Babel stays hard to use (last section)?

Nothing was executed for this estimate. It comes from the static triage (`triage/selection_versions.csv`) and the
runtimes Kaggle recorded for each version. Table: `triage/top_versions.csv` (one row per kernel, built by
`python src/top_versions.py`).

## The 70 best versions

| comp | grader | needs GPU | DL training | Kaggle runtime median / max | total | all external inputs located | largest external input | competition data |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| aes2 | MLE-bench | 10 | 6 | 7 min / 1.3 h | 3.7 h | 4 | 24 GB | 0.04 GB |
| gquest | MLE-bench | 9 | 7 | 16 min / 1.7 h | 6.6 h | 2 | 10 GB | 0.02 GB |
| hms | MLE-bench | 9 | 2 | 5 min / 15 min | 0.8 h | 4 | 41 GB | 26 GB |
| ranzcr | MLE-bench | 10 | 0 | 7 min / 54 min | 2.3 h | 6 | 2.5 GB | 13 GB |
| amex | none yet | 3 | 0 | 54 min / 11.9 h | 35.0 h | 7 | 18 GB | 50 GB |
| commonlit | none yet | 10 | 1 | 14 min / 1.3 h | 3.6 h | 1 | 42 GB | < 0.01 GB |
| equity | none yet | 9 | 9 | 24 min / 3.7 h | 10.3 h | 5 | 54 GB | 0.01 GB |
| **total** | | **60** | **25** | **11 min / 11.9 h** | **62 h** | **29** | | |

- **Workload**: 37 run inference with saved models (weights from external Kaggle datasets), 25 train a neural net,
  4 fit classical models (LightGBM etc.), 4 only blend other submissions.
- **Runtime on Kaggle**: 39 finish in under 15 min, 17 in 15–60 min, 7 in 1–3 h, 6 take over 3 h (5 of those are
  amex, on CPU). Total 62 h: 29 h for GPU notebooks, 34 h for CPU notebooks.
- **"Needs GPU"** = the code calls CUDA or trains a neural net. Kaggle gave these a P100 or 2×T4 (16 GB each),
  about 30 GB RAM and a 12 h session cap. Two notebooks were written for Kaggle's TPU.
- **External inputs** (pretrained weights, preprocessed data, other notebooks' outputs): all 70 use at least one.
  For 41 we could not locate at least one input on Kaggle yet (unverified: name search only).
  The located ones total ≥ 294 GB (179 datasets, of which 95 have a measured size).

## Estimate

**Per run** (one notebook version): 1 GPU with ≥ 16 GB memory (any Babel GPU), 4–8 CPU cores, 32 GB RAM, no
internet (66 / 70). Disk: competition data (up to 50 GB) plus external inputs (up to 54 GB per notebook).

**All 70 once** (assuming inputs and graders were available):
- Kaggle compute: 62 h (29 h GPU, 34 h CPU).
- On Babel, take the same: its GPUs are faster than a P100/T4, but inference notebooks in code competitions only
  scored Kaggle's tiny public test when committed, and our MLE-bench test split is much larger (aes2: 1,731
  essays vs 3).
- Multiply by 2–3 for failed runs and reruns (in the Oct 23 sweep, under half of the easy versions ran as-is).
- **Budget: about 60–90 GPU-hours and 70–100 CPU-hours.**
- Disk: about 0.5 TB (inputs ≥ 294 GB + ~90 GB competition data); the 2 TB quota on `/data/user_data` is enough.
- 13 runs take over 1 h and up to 12 h. On the `preempt` partition these are likely to be killed and restart
  from zero.

**What can run today**: 16 of the 70 have a grader and every external input located: aes2 4, hms 4, ranzcr 6, gquest 2.
- All 16 need a GPU, and 14 of them are inference-only.
- Kaggle time is 6.8 h in total. They need 114 GB of downloads (47 datasets), and ranzcr must be prepared first (13 GB).
- The other 54 are blocked by an unlocated input (41) or by a missing grader (amex, commonlit and equity: 30;
  the two overlap).

**Reproducing the TraceML agent baseline** (`trajectories_experiment_run/*/run_meta.json`):
- Codex + gpt-5.4-mini.
- 1 GPU per run, 12 h wall clock, hard kill at 13.2 h.
- The baseline condition (`rebut_12h_base`) is 7 runs, one per paired competition: **84 GPU-hours, each 12 h
  without interruption.** All 32 runs (skill, base, ablations) would be 384 GPU-hours.
- It also needs an OpenAI API budget.
- Preemption restarts a run from zero, so this needs a GPU that is not preemptible.

**End-to-end evaluation** later: each evaluated step means one run of the agent-edited notebook. That is about the
same time as the expert version: median 11 min, mean 53 min.

## Caveats

- Static labels are regex-based. "Needs GPU" can miss TensorFlow code that uses the GPU implicitly; it was
  widened to include every notebook that trains a neural net.
- External inputs marked missing are unverified. Meta Kaggle's `KernelVersionDatasetSources` would resolve them
  exactly.
- One kernel's best version has no recorded Kaggle runtime (ranzcr `goldenlock/image-model-single-model-…`).
- Kaggle runtimes are wall clock on Kaggle hardware, not measurements on Babel. Task 1 of this week (time one
  notebook per competition on Babel) replaces them with real numbers.

## If Babel stays hard to use

Babel today: our account only has the `preempt` partition. On Oct 29 a GPU job was preempted after 6 min, and
CPU-only jobs waited 40+ min (low fair-share, and the CVPR deadline on Nov 16 keeps GPUs ~90% allocated). The
non-preemptible `general` partition rejects our QoS. The Babel wiki is behind CMU login, so its rules for getting
`general` access were not read.

Options (researched 2026-10-29; prices are list prices for GPU only):

| option | cost | how to get it | longest uninterrupted run | expert notebooks | 12 h agent runs |
|---|---|---|---|---|---|
| Babel `general` partition | free | account change via advisor (process not verified) | 2 days (LTI page) | yes | yes, best fit |
| CMU ORCHARD (Google Cloud, 296 H100) | compute free in the pilot; storage billed | PI submits a request; needs an ACCESS ID; a 30-min Bootstrap job first | General queue: 1 GPU, 12 h, "will not be interrupted" | yes | almost (12 h < TraceML's 13.2 h hard kill) |
| PSC Bridges-2 via NSF ACCESS Explore | free | short proposal + advisor letter; days to ~2 weeks (unofficial) | 48 h | yes | yes (OpenAI API from compute nodes not verified) |
| NAIRR Pilot Start-Up | free, up to 2,000 GPU-h for 3 months | advisor letter; ~2–3 weeks | depends on host | yes | yes |
| Kaggle | free, ~30 GPU-h per week | immediate | 12 h session | yes: same paths and similar hardware, code runs almost unchanged | no |
| Rented on-demand GPU (RunPod Secure Cloud, Lambda) | ~$0.6–4 per GPU-h | immediate | not preempted | yes | yes |
| Spot instances, Modal, Vast, RunPod Community | cheapest | immediate | preemptible | yes | no (a preempted run restarts from zero) |

- **Rented GPU, cost:**
  - Expert notebooks (60–90 GPU-h): about $35–100 on an L4 or A6000.
  - Agent baseline (~92 GPU-h incl. the hard-kill margin): about $55 (L4 / A6000) to $300 (H100).
  - All 32 agent runs: $230–1,300.
  - The OpenAI API for the agent comes on top. gpt-5.4-mini is $0.75 / $4.50 per M input / output tokens (aggregator price); tokens per run are unknown.
- **Kaggle route for the expert notebooks:**
  1. Upload MLE-bench `prepared/public` as a private dataset (limit 200 GB; hms 26 GB and ranzcr 13 GB fit).
  2. Attach the public weight datasets, push each notebook with `kaggle kernels push`, then download `submission.csv`.
  3. Grade on Babel, so the answers never leave Babel.
  - 60–90 GPU-h is 2–3 weeks of one account's quota. CPU sessions (the amex LightGBM runs) do not use GPU quota.
- **Credit programs are too slow for this month:**
  - AWS Cloud Credit for Research: up to $5k, 90–120 days.
  - Google Cloud research credits: PhD students and faculty.
  - OpenAI Researcher Access: up to $1k, quarterly review, credits around Jan 2027 at the earliest.
- **For a fair agent baseline, match TraceML's GPU.** A 12 h budget buys very different amounts of training on an
  L4 and on an H100. `run_meta.json` only gives the device index (`"gpu": "2"`), so the GPU type still has to come
  from the paper or the authors.

Suggested order:
1. Ask Sherry now for **Babel `general` access** and an **ORCHARD request** (the PI submits it). Both are free and
   not preemptible.
2. **Agent baseline:** if neither arrives within about a week, rent one on-demand GPU of the same type TraceML used.
3. **Expert notebooks:** keep short runs on Babel `preempt`, and send long or overflow runs to Kaggle.
4. **Longer term:** ACCESS Explore (Bridges-2, 48 h jobs) or a NAIRR Start-Up.

Checked against the official page: the ORCHARD queues and the ACCESS ID requirement (cmu.edu/rcd/request.html,
cmu.edu/rcd/faq.html). Not verified:
- Babel's `general` access process;
- ORCHARD turnaround;
- internet access from ORCHARD and Bridges-2 compute nodes;
- Kaggle's concurrent-session limit and whether a notebook's environment can be pinned when pushed through the API;
- Colab and AWS spot prices.

Sources: [CMU RCD request](https://www.cmu.edu/rcd/request.html), [CMU RCD FAQ](https://www.cmu.edu/rcd/faq.html),
[LTI Babel page](https://lti.cs.cmu.edu/misc-pages/hpc1/babel.html), [PSC Bridges-2 guide](https://www.psc.edu/resources/bridges-2/user-guide/),
[ACCESS project types](https://allocations.access-ci.org/project-types), [NAIRR Start-Up](https://nairrpilot.org/opportunities/startup-project),
[Kaggle notebooks docs](https://www.kaggle.com/docs/notebooks), [Kaggle kernel metadata](https://github.com/Kaggle/kaggle-api/blob/main/docs/kernels_metadata.md),
[RunPod pricing](https://www.runpod.io/pricing), [Lambda pricing](https://lambda.ai/pricing), [Modal preemption](https://modal.com/docs/guide/preemption),
[AWS research credits](https://aws.amazon.com/government-education/research-and-technical-computing/cloud-credit-for-research/),
[OpenAI Researcher Access](https://openai.com/form/researcher-access-program).

## First GPU runs (Oct 29, evening)

GPU env `kaggle-run-gpu` (CUDA torch + timm, `env/kaggle-run-gpu.txt`) works on an L40S. Two of the 16 "runnable
today" best versions were run as 1-GPU jobs, and both failed within seconds on a missing Python module. The cause
was not the GPU; it was two gaps in how we fetch external inputs:

| version | error | cause |
|---|---|---|
| hms ryanirl/hms-baseline-sub v18 | `No module named 'eeg_cnn_rnn_w1'` | we download the **current** version of dataset `ryanirl/hms-models`; the expert's notebook used an older version that still had this file |
| aes2 lenferdetroud/aes2-tuning-ensemble v2 | `No module named 'aes2_preproces_cache_vectorize'` | a Kaggle **utility script** (mounted under `/kaggle/usr/lib/<slug>/` and put on the Python path); the static triage only looks for `/kaggle/input/...` references, so it never fetched it |

So "all external inputs located" is optimistic: an input can be located but be the wrong version, and utility
scripts are not detected at all.

**Partial fix:** a notebook's metadata (`metadata.kaggle.dataSources`) lists the exact inputs Kaggle attached:
`datasetVersion` (dataset version id), `kernelVersion` (the exact notebook version whose output or utility script was
used), the competition data bundle, and `metadata.kaggle.accelerator`. Resolving inputs from these ids removes both
gaps. But only the newer competitions carry it: every sampled version of aes2, hms and equity (2024–25) has it, and
none of gquest, ranzcr, commonlit and amex (2020–22) does. For those, exact versions still need Meta Kaggle's
`KernelVersionDatasetSources` table (or picking the dataset version that predates the notebook version).

A third run, ranzcr ttahara/ranzcr-multi-head-model-inference v41, hit the same problem after two environment fixes:
- first `cv2` and `albumentations` were missing; both are now added to the GPU env;
- then `timm` said `Unknown model (resnet200d_320)`. The notebook appends a bundled timm copy (dataset
  `yasufuminakama/pytorch-image-models`) to `sys.path`. Our installed timm 1.0.30 shadows that copy, and the
  current version of the dataset (timm 0.4.13) no longer has that model either. The expert used an older
  version, and this 2021 notebook has no `dataSources` metadata to say which.

Then three GPU versions that need **no external inputs** (`n_external == 0`, PyTorch) were run, to test the GPU
itself and to time it:

| version | result | Babel vs Kaggle runtime |
|---|---|---|
| gquest pavelvpster/google-q-a-labeling-tf-idf-pytorch v5 | **OK**: MLE-bench 0.337 (Kaggle 0.297) | 79 s on an L40S vs 194 s |
| gquest alonalon/hirarchical-attention-with-text-augmentation v8 | failed: `gensim.summarization` was removed in gensim 4 | – |
| hms hideyukizushi/hms-only-spectrograms-efficientnetv2… v6 | trained, then failed: loads `best_model_fold0.pth` from an input folder that the static triage missed | 207 s vs 190 s (training part) |

Then ranzcr v41 was rerun with dataset version 5 (timm 0.3.2) and a new compat patch, `prefer_attached_libraries`,
which turns `sys.path.append(<input path>)` into `sys.path.insert(0, ...)`. The attached timm then loads, but it
imports `torch._six`, which torch 2 removed.

**Tally: 1 of 6 GPU versions ran.** The GPU itself works; one data point says Babel is about 2.5× faster than
Kaggle. Every failure was about old library versions or external inputs:
- a deleted dataset version: `ryanirl/hms-models` returns 404 for every old version;
- utility scripts;
- inputs referenced by a dynamically built path;
- old library versions needing old dependencies (timm 0.3 → torch < 2, gensim < 4).

### Leakage: expert models trained on Kaggle's full train set

MLE-bench builds its test set from Kaggle's **train** set, because Kaggle's own test labels are private. An expert
notebook that loads weights or features prepared outside the notebook (37 of the 70 best versions are
"inference, saved models") used models that were most likely trained on all of Kaggle's train set. Our test rows
are part of that set. Example: aes2 v2 loads `X.pickle` / `y.pickle` that a preprocessing kernel computed on the
full train set. Such a version has seen our test labels, so its MLE-bench score is inflated, and so is the score of
any agent edit that starts from it. Only versions that train inside the notebook on `prepared/public` are scored
cleanly. The same applies to our own amex, commonlit and equity splits (see `docs/own_graders.md`). This needs a
team decision before investing in making inference-only versions run.

## Measured on Babel (update, Oct 30)

Task 1 asked for measured times. Every version that ran and was graded on Babel so far (`results/runs.jsonl`,
status OK: Oct 23 sweep, GPU tests, pivot runs):

| comp | versions run | runtime median / max |
|---|---:|---:|
| aes2 | 92 | 72 s / 15 min |
| hms | 70 | 18 s / 13 min |
| gquest | 37 | 17 s / 2 min |
| ranzcr (GPU) | 6 | 88 s / 2 min |
| equity | 2 | 34 s / 39 s |
| amex, commonlit | 0 | not measured |

These are not the same versions as the 70 above. They are mostly light notebooks (classical models, inference),
because the heavy training notebooks mostly did not run yet, so they understate the heavy ones.

**One pivot case** (the 7 in `docs/agent_pivots_2026-10-30.md`):
- One SLURM job runs expert v_k, the agent and expert v_k+1, and grades all three.
- Wall clock: 13–28 min on one node with 1 GPU and 8 CPUs.
- Agent (Claude Code + Opus 5.5): 3–22 min (mean 10) and $0.18–0.73 (mean $0.41) per run, by Claude Code's own
  cost estimate. $2.89 for all 7.

**Projections**, assuming $0.41 and about 17 node-minutes per agent run (agent time plus running and grading its code):
- Next round: 7 pivots × with/without knowledge × 3 repeats = 42 agent runs, about $17 and 12 node-hours.
- 42 human pivots have both versions running on Babel already (aes2 20, gquest 14, hms 4, ranzcr 3, equity 1; by
  author tier 31 Contributor, 5 Expert, 3 Master, 3 Grandmaster). All of them × 2 × 3 = 252 agent runs, about $105
  and 70 node-hours.

**Larger scopes** (all 7 paired competitions; Kaggle's recorded runtime, before failed runs and reruns):

| scope | versions | Kaggle runtime | needs GPU |
|---|---:|---:|---:|
| 70 best versions (above) | 70 | 62 h | 86% |
| all 3,315 human pivots (Yaqing's labels) | 5,289 | ~3,100 h | 60% |
| all human versions with code (427 notebooks) | 13,411 | ~9,100 h (4,300 GPU + 4,900 CPU) | 56% |

- Median 5 min per version, but a long tail: the mean is 41 min, and amex and equity notebooks run for hours.
- Agent at all 3,315 pivots, with and without knowledge, once each: 6,630 runs, about $2,700 of API. Each run also
  runs the edited notebook (about as long as the expert version, mean 35 min), about 5,000 node-hours.
- Static triage of the 5,289 pivot versions: 83% need external inputs we have not prepared; 225 are inputs-complete
  and light.
- Source: `/data/user_data/pengchej/traceml/versions_7comps.csv` (static triage of all 7 comps) joined with
  `pivot_labels.csv` (not in git).

**Cost by scope** (slide 2 of the Oct 30 deck). Rental prices are on-demand list prices from comparison sites
(Oct 2026, indicative): A100 80 GB about $1.2–2.8 per GPU-hour, H100 about $2.7–4.3; the table uses $2 and $3.

| scope | agent API | GPU-hours (A100 class) | wall clock | rented A100 / H100 |
|---|---:|---:|---:|---:|
| next round: 7 pivots, ± knowledge, 3 runs each (42 runs) | ~$17 | ~12 h | ~3 h on 4 GPUs | ~$25 / ~$35 |
| all 42 pivots that run today, same design (252 runs) | ~$105 | ~70 h | ~9 h on 8 GPUs | ~$140 / ~$210 |
| all 3,315 human pivots, ± knowledge, once (6,630 runs) | ~$2,700 | ~5,000 h (±2×) | ~1 week on 32 GPUs | ~$10k / ~$10k |
| TraceML's own baseline, 7 × 12 h | OpenAI, unknown | 84 h | 12 h on 7 GPUs | ~$170 / ~$250 |

- The Babel cards we got (L40S, A6000, A100 40 GB, RTX 6000 Ada, L40, RTX Pro 6000) are all about A100 class for
  this work. Babel has no H100 on our partition.
- The all-pivots row: the 5,289 expert versions, one run of each agent-edited notebook and the agent's own time,
  from Kaggle runtimes (mean 35 min per version) halved for A100-class cards, plus 1.5× for failed runs.
- On an H100, GPU-bound parts run about 2× faster, but the agent's thinking time does not shrink. So the small rows
  cost a bit more on an H100 and the large row costs about the same.

**Per version and total** (final slide 2 of the Oct 30 deck; same assumptions as above, totals include 1.5× for
failed runs):

| | one version | all versions (7 comps) |
|---|---|---|
| expert version, re-run | ~20 min on an A100 (median 3 min) | 13,411 versions: ~7,000 GPU-h |
| agent writes a version and runs it | ~35 min on an A100 + $0.41 API | 3,315 pivots × ± knowledge = 6,630: ~4,000 GPU-h + ~$2,700 API |
| total | | ~11,000 GPU-h + ~$2,700 API |

On 32 GPUs: about 2 weeks on Babel (free) or rented A100s (~$22k), about 10 days on rented H100s (~$23k).

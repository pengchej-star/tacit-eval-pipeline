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

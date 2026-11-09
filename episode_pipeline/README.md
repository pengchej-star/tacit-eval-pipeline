# Episode-level tacit-knowledge pipeline (extraction_v1), 2026-10-22 .. 2026-10-28

Pipeline: trajectories -> episodes -> episode-level rationales -> cross-expert rules. All model calls: wine-claude-opus-4-6 via the CMU LiteLLM proxy.

## code/
- episodes.py           segment each notebook trajectory into episodes (one call per trajectory; 7 fixed patterns: sweep, probe, revert, build, fix, consolidate, explore)
- episode_extract.py    one call per episode: search process, feedback response, exit, and L2/L3 rationales with step-id instances
- knowledge.py          lever vocabulary (<=40 categories), per-cell induction of rules supported by >=2 kernels, chunked consolidation
- prompts.py            all prompts (EPISODE_SYSTEM, EPISODE_EXTRACT_SYSTEM, VOCAB/MAP/INDUCE/CONSOLIDATE_SYSTEM, plus the step-level ones)
- config.yaml           sections episodes / episode_extract / knowledge (context limits used: code 6000, diff 14000, history 12000 chars)
- llm.py, data.py       proxy client; step-level data loader.  root_data.py = ../data.py (TraceML data layer the scripts import as `root`)
- build_runnable_steps.py, extract.py, cluster.py   step-level pipeline (the 7 runnable cases)
Inputs not included: data/TraceML (paired split action.parquet + notebooks), .env with LITELLM_API_KEY.

## results/
- selection.csv                      the 70 selected trajectories (plus kernel 7676170 was added on the command line)
- episodes.jsonl/.md                 71 trajectories, 3419 transitions -> 867 episodes
- episodes_strat.jsonl, ep_strat.*   stratified pilot: 134 episodes (1 sweep + 1 other per trajectory) -> 295 items
- episode_rationales.jsonl/.md       full run: 862 episodes -> 1892 items (134 reused from the pilot)
- knowledge_strat.*                  rules from the pilot (111 rules with >=2 kernels)
- knowledge_full.*                   rules from the full run (602 rules with >=2 kernels; 42 with >=5; vocab, per-cell checkpoints, raw and consolidated rules)
- runnable.*, clusters_runnable.*    step-level extraction + LLM clustering of the 7 runnable cases (2026-10-21)

Rule record: name, level (L2 method / L3 strategy), context, action, exceptions, support (item ids '<kernel>:e<n>#<k>'), kernels, comps, tiers, new_best counts, examples with step ids.
Known weaknesses: consolidation leaves synonymous rules split (compute support per rule family); numeric thresholds in rule text are model summaries, not statistics; confidence is uninformative.

# agent_tree

Replaces steps 1-4 of the pipeline (`../pipeline_tree`) (skeleton, clustering, merge, desiderata) with a single agent that reads `../data/episode_items.jsonl` itself and writes the tree and the desiderata. Two agents do it independently so the trees can be compared.

| file | |
|---|---|
| `prompt.md` | the one prompt both agents get (edit this) |
| `run_claude.sh` | Claude Code, `claude-sonnet-5-5` (override: `CLAUDE_MODEL`) |
| `run_codex.sh` | Codex, `gpt-6-astra` (override: `CODEX_MODEL`; **check the exact id**) |
| `run_both.sh` | both in parallel |
| `validate.py` | `python validate.py runs/claude`: every item placed once, ids consistent, desiderata for every decision node |

Output: `runs/<agent>/output/{tree.json,desiderata.json,notes.md}`, plus `transcript.jsonl` (full tool trace).

## Isolation
Each agent runs in a fresh `/tmp` directory containing only `episode_items.jsonl`; the prompt is passed as the argument. No chat history, no repo, no CLAUDE.md of the project.
- Claude: `--no-session-persistence --setting-sources "" --strict-mcp-config --disable-slash-commands`, auto-memory off, web tools off. The user-level `~/.claude/CLAUDE.md` (if you have one) is still read; `--bare` would drop it but needs an `ANTHROPIC_API_KEY`.
- Codex: temporary `CODEX_HOME` with only `auth.json` copied (your `~/.codex/AGENTS.md` is not read), `--ephemeral`, sandbox `workspace-write`.
- Neither Bash tool is a hard filesystem jail; they are told only about the temp dir.

## Output format
`tree.json` is close to `new_extraction`'s `3_merged_tree.json` (nested `children`, ids `T.i.j`, leaf `items`), and `desiderata.json` has per-node `groups -> checks {check, how, pushes}` as in the step-4 prompt. Not yet done: dedupe checks into the shared registry (`E01...`) and add `all_items`/`experts`/`n_edits` per node; a converter is needed before step 5 (`visits.py`) can read it.

## Not run yet
Nothing has been run. Check before the first run: `codex` is not installed on this machine (`which codex` is empty), and the exact Codex model id.

## Attention map (steps 5-8) on the Codex tree
- `to_pipeline.py codex`: converts `runs/codex/output` into `../out/pooled_episode_agent_codex/` (`3_merged_tree.json`, `4_desiderata.json`, plus copies of `2a_items.json`, `trans.json`).
- **Method 1 (original code):** `cd .. && python run.py --suffix _agent_codex --from 5 --to 8` (needs `../.env`, python with `requirements.txt`, e.g. `/opt/miniconda3/bin/python3`).
- **Method 2 (Codex agent):** `prompt_attention.md` (edit this) + `run_codex_attention.sh` (`CODEX_EFFORT` default medium). `prep_attention.py` builds the agent's working dir (`jobs.jsonl` = one line per edit with its walk through the tree, checks, history). Output: `runs/codex_attention/output/{visits,scores,enough,returns}.json`.

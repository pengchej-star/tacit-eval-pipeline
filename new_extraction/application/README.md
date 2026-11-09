# application — does the extracted memory help an agent improve code?

An agent gets an expert's code version (v_old), the task description and the summary of the earlier versions, and revises the code to improve the score. Output: `revised_code.py` and `report.json` (one yes/no item per observation/check, in the order made, plus an `action_summary`).

| file | |
|---|---|
| `prompt.md` | the one prompt shared by all conditions (edit this) |
| `memory_instruction.md` | the paragraph added in the `memory` condition |
| `planning_instruction.md` | the TraceML planning block added in the `traceml_instruction` condition (copy of `tacit-eval-pipeline/agent_generation/planning_instruction.md`; `{{HOURS}}` is filled from `PLANNING_HOURS`, default 2) |
| `tasks/<comp>.md` | task descriptions: **paste the official Kaggle text** into each file (the script warns while the TODO is there) |
| `cases/cases.json` | the 21 selected cases (3 per competition) incl. the hidden gold step; made by `select_cases.py` |
| `memory/` | `taxonomy.md` + `attention/` of the Codex-tree run (`out/pooled_episode_agent_codex/application`); no `cases/`, no `evidence/` |
| `run_application.py` | prepare / print prompt / run |
| `workspaces/` | what each agent sees (made by `--prepare`) |

Conditions: `memory` (shared prompt + memory paragraph + `memory/`), `no_memory` (shared prompt), `traceml_instruction` (shared prompt + planning block).
Agent: Codex `gpt-6-astra` (`CODEX_MODEL`, `CODEX_EFFORT`, default medium), isolated temp dir and `CODEX_HOME` as in `agent_tree/`.

```bash
python select_cases.py                          # re-select cases
python run_application.py --prepare             # build workspaces/, run nothing
python run_application.py --print-prompt ranzcr_13848868_v18 memory
python run_application.py --run --cases ranzcr_13848868_v18 --conditions memory,no_memory
```
Results: `runs/<case>/<condition>/`.

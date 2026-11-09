# Task: improve the score of an existing Kaggle solution

You are working on improving the current version of code (a notebook converted into a script) for a machine learning task. Your job is to revise the current code so that it scores better.

## What you have (all in the current directory)
- `task.md`: the competition description, the metric and the direction of the metric.
- `current_code.py`: the current version (**v{{V_OLD}}**) of the solution. Its notebook cells are separated by `# %%` lines; cell outputs are not included.
- `history.md`: the leaderboard score of the current version and a summary of every earlier version (what was changed and the score it reached). It contains nothing about later versions.
- The competition data is **not** available here. Work from the code, the description and the history.

## What to do
Revise `current_code.py` so that it has a credible path to a better leaderboard score ({{DIRECTION}}). Decide yourself what to change; you may change one thing or several. Keep a working end-to-end pipeline that writes the submission in the format the competition requires, and keep the Kaggle paths and the structure of the code unless you have a reason to change them. Do not run training or inference (there is no data); you may run a syntax check.

## Time limit
You have **at most {{MINUTES}} minutes** in total for this task, including reading, deciding and writing. The session is stopped when the time is up, and only the files in `output/` at that moment count. So write a first complete version of both output files early, and refine them if time remains.

## Rules
- Do not look for other participants' or humans' solutions, notebooks or write-ups of this competition, and do not use the internet. General library knowledge is fine.
- Do not read files outside the current directory.
- Do not describe the code in chat; write the files below.

## Output
Write two files into `output/` (create the directory):

1. `output/revised_code.py`: the complete revised code, in the same format as `current_code.py` (cells separated by `# %%` lines).

2. `output/report.json`: a record of what you looked at before deciding and what you changed:
```json
{
  "observations": [
    {"observation": "<one yes/no statement>", "result": "yes", "evidence": "<what you looked at and what it showed>"},
    {"observation": "<another statement>", "result": "no", "evidence": "..."}
  ],
  "action_summary": "<a short summary of the changes you made to the code and why>"
}
```
- `observations`: every observation or check that you made while deciding what to change, in the order you made them (for example whether a score trend has flattened, whether an option was already tried, whether the code does X). Each observation is **one** yes/no statement about the situation, answered `"yes"` or `"no"` in `result`. Put every check in its own item: do not combine several checks in one item, do not use "and"/"or" to join two questions, and do not list a check you did not actually make. `evidence` says where the answer came from (a line of the code, a score in the history, the task description, ...).
- `action_summary`: what you changed, in a few sentences.
{{CONDITION_BLOCK}}
## Completion condition
Before finishing, check that `output/revised_code.py` is valid Python (apart from notebook magics), that `output/report.json` is valid JSON of the form above, and that every observation has `result` equal to `"yes"` or `"no"`. Then finish.

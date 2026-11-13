# Task: improve the score of an existing Kaggle solution

You are working on improving the current version of code (a notebook converted into a script) for a machine learning task. Your job is to revise the current code so that it scores better.

## What you have
In `/workspace` (the current directory):
- `task.md`: the competition description, the metric and the direction of the metric.
- `current_code.py`: the current version (**v{{V_OLD}}**) of the solution. Its notebook cells are separated by `# %%` lines; cell outputs are not included.
- `history.md`: the leaderboard score of the current version and a summary of every earlier version (what was changed and the score it reached). It contains nothing about later versions.

In `/kaggle`, laid out as on Kaggle:
- `/kaggle/input/{{COMP}}/`: the competition data (training data with labels, the unlabeled test data, `sample_submission.csv`). The test labels are not available.
- `/kaggle/input/<dataset>/`: the datasets the code attaches (for example model weights and libraries), at the paths the code uses.
- `/kaggle/working/`: the working directory of the code and your scratch space.

`python` has PyTorch with one NVIDIA GPU, timm, scikit-learn, pandas, numpy, lightgbm, xgboost and more. There is no internet access for the code.

## What to do
Revise `current_code.py` so that it has a credible path to a better leaderboard score ({{DIRECTION}}). Decide yourself what to change; you may change one thing or several. Keep a working end-to-end pipeline that writes the submission in the format the competition requires, and keep the Kaggle paths and the structure of the code unless you have a reason to change them.

You can run code. Run your revision the way it will be scored, `cd /kaggle/working && python /workspace/output/revised_code.py`, fix what fails, and use the training data to check your changes where that is meaningful. Your revision will be run once more after the session, the same way, and scored on the held-out test labels.

## Time limit
You have **at most {{MINUTES}} minutes** in total for this task, including reading, deciding, running and writing. The session is stopped when the time is up, and only the files in `/workspace/output/` at that moment count. So write a first complete version of both output files early.

This time is meant for iterating, so plan to use most of it. Run `date` at the start and check it as you go. Once a first version runs end to end, keep going: test further changes on the training data (for example on a held-out fold), debug what fails, compare each change with your best version so far, and keep the best one in `output/`. Do not finish before about {{MIN_MINUTES}} minutes have passed unless you have run out of changes worth testing; in that case say why in `stop_reason`. Leave a few minutes at the end for the final end-to-end run and the report.

## Rules
- Do not look for other participants' or humans' solutions, notebooks or write-ups of this competition, and do not use the internet. General library knowledge is fine.
- Do not read files outside `/workspace` and `/kaggle`.
- Do not describe the code in chat; write the files below.

## Output
Write two files into `/workspace/output/` (create the directory):

1. `output/revised_code.py`: the complete revised code, in the same format as `current_code.py` (cells separated by `# %%` lines). It must run top to bottom with `cd /kaggle/working && python /workspace/output/revised_code.py` and write `/kaggle/working/submission.csv`.

2. `output/report.json`: a record of what you looked at before deciding and what you changed:
```json
{
  "observations": [
    {"observation": "<one yes/no statement>", "result": "yes", "evidence": "<what you looked at and what it showed>"},
    {"observation": "<another statement>", "result": "no", "evidence": "..."}
  ],
  "action_summary": "<a short summary of the changes you made to the code and why>",
  "stop_reason": "<why you stopped: time nearly used up, or why no further change was worth testing>"
}
```
- `observations`: every observation or check that you made while deciding what to change, in the order you made them (for example whether a score trend has flattened, whether an option was already tried, whether the code does X, what a run of the code showed). Each observation is **one** yes/no statement about the situation, answered `"yes"` or `"no"` in `result`. Put every check in its own item: do not combine several checks in one item, do not use "and"/"or" to join two questions, and do not list a check you did not actually make. `evidence` says where the answer came from (a line of the code, a score in the history, the task description, the output of a run, ...).
- `action_summary`: what you changed, in a few sentences.
- `stop_reason`: one sentence.
{{CONDITION_BLOCK}}
## Completion condition
Before finishing, check that `output/revised_code.py` runs end to end and writes `/kaggle/working/submission.csv`, that `output/report.json` is valid JSON of the form above, and that every observation has `result` equal to `"yes"` or `"no"`. Then finish.

"""Summarize a batch of expert-version runs: how many run and get graded, and why the others fail.

Each (key_id, version) counts once, by its latest run. Failures are put in coarse categories from the status and the
error message. Also reports, per kernel that had a runnable version before the batch, how many of its other versions run.

Usage:
  python src/sweep_report.py --results results/runs.jsonl --tag sweep-1023
"""

import argparse
import json
import re
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
SHORT = {"learning-agency-lab-automated-essay-scoring-2": "aes2", "google-quest-challenge": "gquest",
         "hms-harmful-brain-activity-classification": "hms", "ranzcr-clip-catheter-line-classification": "ranzcr"}
# checked in order; the first match wins
RULES = [
    ("missing package", r"ModuleNotFoundError|No module named"),
    ("out of memory", r"DeadKernelError|Kernel died"),
    ("needs GPU", r"CUDA|cuda|OpenCL|NVIDIA|nvidia|GPU"),
    # "Invalid value ... for dtype": pandas 3 raises where pandas 2 upcast the column with a warning
    ("old code vs new libraries",
     r"AttributeError|ImportError|cannot import name|unexpected keyword|deprecated|Invalid value .* for dtype"),
    ("file or path not found", r"FileNotFoundError|No such file"),
]
STATUS = {"OK": "runs and is graded", "MISSING_EXTERNAL_INPUT": "external input missing", "TIMEOUT": "timeout",
          "NO_SUBMISSION": "runs but writes no submission.csv", "INVALID_SUBMISSION": "submission invalid",
          "GRADE_FAILED": "submission invalid"}


def category(row):
    if row["status"] != "EXEC_FAILED":
        return STATUS.get(row["status"], row["status"])
    text = row.get("error_tail") or ""
    final = text.split("[final error]")[-1]
    for name, pattern in RULES:
        if re.search(pattern, final):
            return name
    return "error in the notebook code"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", type=Path, nargs="+", default=[REPO / "results/runs.jsonl"])
    ap.add_argument("--tag", default="sweep", help="only versions with a run whose tag starts with this")
    args = ap.parse_args()

    rows = [json.loads(l) for p in args.results for l in p.read_text().splitlines() if l.strip()]
    R = pd.DataFrame(rows)
    R = R[R.key_id.notna() & R.version.notna()].assign(version=lambda d: d.version.astype(int))
    tagged = R[R.tag.fillna("").str.startswith(args.tag)]
    before = R[~R.tag.fillna("").str.startswith(args.tag)]
    ok_before = set(before[before.status == "OK"].key_id)
    keys = set(zip(tagged.key_id, tagged.version))
    latest = R.sort_values("timestamp").groupby(["key_id", "version"]).tail(1)
    L = latest[[k in keys for k in zip(latest.key_id, latest.version)]].copy()
    L["comp"] = L.comp.map(SHORT).fillna(L.comp)
    L["stage"] = L.tag.str.split(":").str[-1]
    L["category"] = L.apply(category, axis=1)
    L["ok"] = L.status == "OK"

    print(f"{len(L)} versions run; {int(L.ok.sum())} run and are graded\n")
    print(pd.crosstab(L.category, L.comp, margins=True, margins_name="total")
          .sort_values("total", ascending=False).to_string(), "\n")
    print(pd.crosstab(L.category, L.stage, margins=True, margins_name="total")
          .sort_values("total", ascending=False).to_string(), "\n")
    no_kaggle = L[~L.ok & L.kaggle_score.isna()]
    print(f"failed versions with no Kaggle score (likely failed on Kaggle too): {len(no_kaggle)} of {int((~L.ok).sum())}")
    print(f"OK versions with no Kaggle score: {int((L.ok & L.kaggle_score.isna()).sum())}\n")

    A = L[L.key_id.isin(ok_before)]
    if len(A):
        per = A.groupby(["comp", "key_id"]).agg(other_versions=("ok", "size"), run_ok=("ok", "sum"))
        per["share"] = (per.run_ok / per.other_versions).round(2)
        print("kernels that already had a runnable version: how many of their other versions run")
        print(per.to_string())
        print(f"total: {int(per.run_ok.sum())} / {int(per.other_versions.sum())}")


if __name__ == "__main__":
    main()

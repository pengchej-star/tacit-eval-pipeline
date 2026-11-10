"""Maintained table of expert cases we have actually run: which run directly, and what blocks the rest.

Rebuilds triage/runnable_cases.csv from results/runs.jsonl. Run it after every batch of runs.

One row per case (key_id, v_k -> v_k+1) where both versions have been run. Each version uses its *latest* run. A case is runnable when the latest run of both versions is OK (graded submission).
Columns include the expert (kernel slug, author, tier), Kaggle links to both exact versions, our MLE-bench
scores next to the Kaggle public scores, whether the improvement direction matches, the compat patches and
external inputs used, and for non-runnable cases the first blocker.

Cases come from triage/cases.csv (4 gradable comps) and triage/selection_cases.csv (Yaqing's 70 kernels).

Usage:
  python src/runnable_cases.py
"""

import argparse
import getpass
import json
import re
from pathlib import Path

import pandas as pd

from run_version import shell_errors

USER_DATA = Path("/data/user_data") / getpass.getuser()
REPO = Path(__file__).resolve().parents[1]
SHORT = {"learning-agency-lab-automated-essay-scoring-2": "aes2", "google-quest-challenge": "gquest",
         "hms-harmful-brain-activity-classification": "hms", "ranzcr-clip-catheter-line-classification": "ranzcr",
         "amex-default-prediction": "amex", "commonlitreadabilityprize": "commonlit",
         "equity-post-hct-survival-predictions": "equity"}


def as_list(v):
    """Older rows predate some fields; pandas turns the missing ones into NaN."""
    return v if isinstance(v, list) else []


def first_error(row):
    """A one-line reason for a failed run: the first exception line in error_tail, else the status."""
    if row is None:
        return "not run"
    if row["status"] == "OK":
        return ""
    text = row.get("error_tail") if isinstance(row.get("error_tail"), str) else ""
    if row["status"] == "EXEC_FAILED" and "[shell cell" not in text and isinstance(row.get("workdir"), str):
        # rows written before run_version surfaced shell-cell errors: recover them from the executed notebook
        text = shell_errors(Path(row["workdir"]) / "executed.ipynb") + text
    for line in text.splitlines():
        m = re.search(r"\b(\w+(?:Error|Exception)):\s*(.*)", line)
        if m and m.group(1) not in ("PapermillExecutionError",):
            return f"{row['status']}: {m.group(1)}: {m.group(2)}"[:200]
    return f"{row['status']}: {text.strip().splitlines()[0][:150]}" if text.strip() else row["status"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", type=Path, default=REPO / "results/runs.jsonl")
    ap.add_argument("--traceml-dir", type=Path, default=USER_DATA / "traceml/hf")
    ap.add_argument("--out", type=Path, default=REPO / "triage/runnable_cases.csv")
    args = ap.parse_args()

    runs = pd.DataFrame([json.loads(l) for l in args.results.read_text().splitlines() if l.strip()])
    runs = runs[runs.key_id.notna() & runs.version.notna()].copy()
    runs["version"] = runs.version.astype(int)
    latest = {(r["key_id"], r["version"]): r for r in runs.sort_values("timestamp").to_dict("records")}

    cases = pd.concat([pd.read_csv(REPO / "triage/cases.csv", dtype={"key_id": str}),
                       pd.read_csv(REPO / "triage/selection_cases.csv", dtype={"key_id": str})])
    cases = cases.drop_duplicates(["key_id", "v_k", "v_k1"])
    cases = cases[[(k, a) in latest and (k, b) in latest for k, a, b in zip(cases.key_id, cases.v_k, cases.v_k1)]]

    selection = set(pd.read_csv(REPO / "triage/selection.csv", dtype={"key_id": str}).key_id)
    kern = pd.read_parquet(args.traceml_dir / "extras/kernels.parquet",
                           columns=["kernel_id", "kernel_slug", "author_username", "author_tier"])
    kern = kern.assign(key_id=kern.kernel_id.astype(str)).set_index("key_id")
    state = pd.concat(pd.read_parquet(args.traceml_dir / f"data/{s}/state.parquet",
                                      columns=["key_id", "version_number", "version_id"]) for s in ("paired", "humans_only"))
    version_id = {(k, int(v)): vid for k, v, vid in zip(state.key_id, state.version_number, state.version_id)
                  if pd.notna(vid)}
    direction = {c: m["score_direction"] for c, m in
                 json.loads((args.traceml_dir / "manifests/competitions.json").read_text()).items()}

    def link(slug, key_id, v):
        vid = version_id.get((key_id, v))
        return f"https://www.kaggle.com/code/{slug}?scriptVersionId={int(vid)}" if slug and vid else ""

    rows = []
    for c in cases.itertuples():
        a, b = latest.get((c.key_id, c.v_k)), latest.get((c.key_id, c.v_k1))
        ok = bool(a and b and a["status"] == "OK" and b["status"] == "OK")
        slug = kern.kernel_slug.get(c.key_id) if c.key_id in kern.index else None
        slug = slug if isinstance(slug, str) and slug else None
        sign = 1 if direction.get(c.comp) == "higher" else -1
        ours = (b["score"] - a["score"]) * sign if ok else None
        theirs = ((b["kaggle_score"] - a["kaggle_score"]) * sign
                  if a and b and pd.notna(a.get("kaggle_score")) and pd.notna(b.get("kaggle_score")) else None)
        patches = sorted({p["name"] for r in (a, b) if r for p in as_list(r.get("patches_applied"))})
        externals = sorted({x["spec"] for r in (a, b) if r for x in as_list(r.get("external_inputs"))})
        rows.append({
            "runnable": ok,
            "comp": SHORT.get(c.comp, c.comp),
            "key_id": c.key_id,
            "author": kern.author_username.get(c.key_id) if c.key_id in kern.index else None,
            "tier": kern.author_tier.get(c.key_id) if c.key_id in kern.index else None,
            "in_yaqing_selection": c.key_id in selection,
            "v_k": c.v_k,
            "v_k1": c.v_k1,
            "score_v_k": a and a["score"],
            "score_v_k1": b and b["score"],
            "kaggle_score_v_k": a and a.get("kaggle_score"),
            "kaggle_score_v_k1": b and b.get("kaggle_score"),
            "improves_ours": None if ours is None else ours > 0,
            "improves_kaggle": None if theirs is None else theirs > 0,
            "direction_matches": None if ours is None or theirs is None else (ours > 0) == (theirs > 0),
            "runtime_s_v_k": a and a["runtime_s"],
            "runtime_s_v_k1": b and b["runtime_s"],
            "patches": ";".join(patches),
            "external_inputs": ";".join(externals),
            "blocker": "" if ok else (first_error(a) if not a or a["status"] != "OK" else first_error(b)),
            "static_status": c.status,
            "last_run": max(r["timestamp"] for r in (a, b) if r),
            "kaggle_url_v_k": link(slug, c.key_id, c.v_k),
            "kaggle_url_v_k1": link(slug, c.key_id, c.v_k1),
        })
    out = pd.DataFrame(rows).sort_values(["runnable", "comp", "key_id", "v_k"], ascending=[False, True, True, True])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)

    print(f"wrote {args.out}: {len(out)} cases run, {int(out.runnable.sum())} runnable "
          f"({int((out.runnable & out.in_yaqing_selection).sum())} in Yaqing's selection)")
    show = ["comp", "key_id", "author", "v_k", "v_k1", "score_v_k", "score_v_k1", "kaggle_score_v_k",
            "kaggle_score_v_k1", "direction_matches", "patches"]
    print(out[out.runnable][show].to_string(index=False))
    if (~out.runnable).any():
        print("\nnot runnable (first blocker):")
        print(out[~out.runnable][["comp", "key_id", "v_k", "v_k1", "blocker"]].to_string(index=False, max_colwidth=110))


if __name__ == "__main__":
    main()

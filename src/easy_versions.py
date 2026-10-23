"""List every static-EASY version with its run outcome: triage/easy_versions.csv.

One row per version that triage_static.py labels EASY, with the expert (notebook, author, Kaggle tier), the Kaggle
score and runtime, our latest run (status, coarse failure reason from sweep_report.py, MLE-bench score), whether the
version is part of a runnable case, and a link to the exact Kaggle version. Re-run after new runs.

Usage:
  python src/easy_versions.py --versions <triage dir>/versions.csv
"""

import argparse
import getpass
import json
from pathlib import Path

import pandas as pd

from runnable_cases import SHORT
from sweep_report import category

USER_DATA = Path("/data/user_data") / getpass.getuser()
REPO = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--versions", type=Path, default=USER_DATA / "traceml/triage_4comp_refresh/versions.csv")
    ap.add_argument("--results", type=Path, default=REPO / "results/runs.jsonl")
    ap.add_argument("--cases", type=Path, default=REPO / "triage/runnable_cases.csv")
    ap.add_argument("--traceml-dir", type=Path, default=USER_DATA / "traceml/hf")
    ap.add_argument("--out", type=Path, default=REPO / "triage/easy_versions.csv")
    args = ap.parse_args()

    V = pd.read_csv(args.versions, dtype={"key_id": str})
    E = V[V.status == "EASY"][["comp", "key_id", "version", "kaggle_score", "kaggle_runtime_min"]]

    runs = pd.DataFrame([json.loads(l) for l in args.results.read_text().splitlines() if l.strip()])
    runs = runs[runs.key_id.notna() & runs.version.notna()].assign(version=lambda d: d.version.astype(int))
    latest = {(r["key_id"], r["version"]): r for r in runs.sort_values("timestamp").to_dict("records")}

    cases = pd.read_csv(args.cases, dtype={"key_id": str})
    cases = cases[cases.runnable]
    in_case = set(zip(cases.key_id, cases.v_k)) | set(zip(cases.key_id, cases.v_k1))

    kern = pd.read_parquet(args.traceml_dir / "extras/kernels.parquet",
                           columns=["kernel_id", "kernel_slug", "author_username", "author_tier"])
    kern = kern.assign(key_id=kern.kernel_id.astype(str)).set_index("key_id")
    state = pd.concat(pd.read_parquet(args.traceml_dir / f"data/{s}/state.parquet",
                                      columns=["key_id", "version_number", "version_id"]) for s in ("paired", "humans_only"))
    version_id = {(k, int(v)): int(vid) for k, v, vid in zip(state.key_id, state.version_number, state.version_id)
                  if pd.notna(vid)}

    rows = []
    for e in E.itertuples():
        r = latest.get((e.key_id, e.version))
        k = kern.loc[e.key_id] if e.key_id in kern.index else None
        slug, vid = (k.kernel_slug if k is not None else None), version_id.get((e.key_id, e.version))
        rows.append({
            "comp": SHORT.get(e.comp, e.comp),
            "key_id": e.key_id,
            "version": e.version,
            "notebook": slug,
            "author": k.author_username if k is not None else None,
            "tier": k.author_tier if k is not None else None,
            "kaggle_score": e.kaggle_score,
            "kaggle_runtime_min": round(e.kaggle_runtime_min, 1) if pd.notna(e.kaggle_runtime_min) else None,
            "ran": r is not None,
            "status": r["status"] if r else "NOT_RUN",
            "outcome": category(r) if r else "not run",
            "score": r["score"] if r else None,
            "in_runnable_case": (e.key_id, e.version) in in_case,
            "run_env": Path(r["run_env"]).name if r and r.get("run_env") else None,
            "last_run": r["timestamp"] if r else None,
            "kaggle_url": f"https://www.kaggle.com/code/{slug}?scriptVersionId={vid}" if slug and vid else "",
        })
    out = pd.DataFrame(rows).sort_values(["comp", "key_id", "version"])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)
    print(f"wrote {args.out}: {len(out)} easy versions from {out.key_id.nunique()} notebooks; "
          f"{int(out.ran.sum())} run, {int((out.status == 'OK').sum())} OK, {int(out.in_runnable_case.sum())} in a runnable case")
    print(out.groupby("comp").agg(versions=("version", "size"), notebooks=("key_id", "nunique"),
                                  ok=("status", lambda s: int((s == "OK").sum()))).to_string())


if __name__ == "__main__":
    main()

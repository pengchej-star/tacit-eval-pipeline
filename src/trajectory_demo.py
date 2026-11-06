"""Lay out one expert trajectory as readable files: every version as a .py, a diff for every step, and a timeline.

For a TraceML key_id, writes demo/<name>/:
  versions/vNN.py        the notebook's cells in order (markdown cells as comments, `# %% [n]` between cells)
  diffs/vNN_to_vMM.diff  unified diff between consecutive versions
  timeline.csv           one row per version: Kaggle score, our score on the MLE-bench split (if run), lines,
                         and for the step into it: TraceML's goal, magnitude, labels, and Yaqing's pivot flag

Usage:
  python src/trajectory_demo.py --key-id 54532847 --name aes2_tfidf_54532847
"""

import argparse
import difflib
import getpass
import json
from pathlib import Path

import pandas as pd

USER_DATA = Path("/data/user_data") / getpass.getuser()
REPO = Path(__file__).resolve().parents[1]


def notebook_to_py(path):
    nb = json.loads(path.read_text())
    out = []
    for i, cell in enumerate(nb.get("cells", []), 1):
        src = "".join(cell.get("source", "")).rstrip()
        if not src:
            continue
        if cell.get("cell_type") == "code":
            out.append(f"# %% [{i}]\n{src}\n")
        else:
            out.append(f"# %% [{i}] markdown\n" + "\n".join("# " + line for line in src.splitlines()) + "\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key-id", required=True)
    ap.add_argument("--name", required=True, help="folder name under demo/")
    ap.add_argument("--human-dir", type=Path, default=USER_DATA / "traceml/extracted/human")
    ap.add_argument("--traceml-dir", type=Path, default=USER_DATA / "traceml/hf")
    ap.add_argument("--versions-table", type=Path, default=USER_DATA / "traceml/versions_7comps.csv")
    ap.add_argument("--pivot-labels", type=Path, default=REPO / "pivot_labels.csv")
    args = ap.parse_args()

    out = REPO / "demo" / args.name
    (out / "versions").mkdir(parents=True, exist_ok=True)
    (out / "diffs").mkdir(parents=True, exist_ok=True)

    files = sorted((args.human_dir / args.key_id / "versions").glob("v*.ipynb"))
    code = {int(f.stem[1:]): notebook_to_py(f) for f in files}
    width = max(2, len(str(max(code))))
    name = {v: f"v{v:0{width}d}" for v in code}
    for v, text in code.items():
        (out / "versions" / f"{name[v]}.py").write_text(text)
    vs = sorted(code)
    for a, b in zip(vs, vs[1:]):
        diff = difflib.unified_diff(code[a].splitlines(keepends=True), code[b].splitlines(keepends=True),
                                    fromfile=f"{name[a]}.py", tofile=f"{name[b]}.py", n=2)
        (out / "diffs" / f"{name[a]}_to_{name[b]}.diff").write_text("".join(diff))

    table = pd.read_csv(args.versions_table, dtype={"key_id": str})
    table = table[table.key_id == args.key_id].set_index("version")
    runs = [json.loads(l) for l in (REPO / "results/runs.jsonl").read_text().splitlines() if l.strip()]
    ours = {}
    for r in sorted(runs, key=lambda r: r["timestamp"]):
        if str(r.get("key_id")) == args.key_id and r["status"] == "OK":
            ours[int(r["version"])] = r["score"]
    steps = {}
    if args.pivot_labels.exists():
        p = pd.read_csv(args.pivot_labels, dtype={"key_id": str})
        for r in p[p.key_id == args.key_id].itertuples():
            # pivot_labels.csv stores a list of names; TraceML's action.parquet a list of {action, parent, ...}
            labels = [d["action"] if isinstance(d, dict) else d
                      for d in (json.loads(r.fine_actions) if isinstance(r.fine_actions, str) else [])]
            steps[int(r.v_new)] = {"from": int(r.v_old), "goal": r.goal_nl, "magnitude": r.magnitude,
                                   "labels": ";".join(labels), "pivot": bool(r.pivot), "pivot_axes": r.pivot_axes}
    rows = []
    for v in vs:
        s = steps.get(v, {})
        rows.append({"version": name[v],
                     "kaggle_score": table.kaggle_score.get(v),
                     "our_score": ours.get(v),
                     "code_lines": len([l for l in code[v].splitlines() if l.strip() and not l.startswith("#")]),
                     "lines_changed": (sum(1 for l in (out / "diffs" / f"{name[s['from']]}_to_{name[v]}.diff")
                                           .read_text().splitlines()
                                           if l[:1] in "+-" and not l.startswith(("+++", "---")))
                                       if s.get("from") in name else None),
                     "pivot": s.get("pivot"), "pivot_axes": s.get("pivot_axes"), "magnitude": s.get("magnitude"),
                     "traceml_labels": s.get("labels"), "traceml_goal": s.get("goal")})
    pd.DataFrame(rows).to_csv(out / "timeline.csv", index=False)
    print(pd.DataFrame(rows).drop(columns=["traceml_goal"]).to_string(index=False))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()

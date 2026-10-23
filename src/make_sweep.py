"""List the expert versions for a batch run (no execution). Writes a TSV: comp, key_id, version, stage, kaggle_runtime_min.

Stage A: every other version of the kernels that already have an OK run (tests "if one version runs, others will too").
Stage B: every static-EASY version in --comps that has not been run yet.
Versions already in --results, or longer than --max-kaggle-min on Kaggle, are skipped (the long ones are counted).
Rows are sorted longest first, so assigning them round-robin to shards balances the shards.

Usage:
  python src/make_sweep.py --versions <triage dir>/versions.csv --out sweep.tsv
"""

import argparse
import json
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--versions", type=Path, required=True)
    ap.add_argument("--results", type=Path, default=REPO / "results/runs.jsonl")
    ap.add_argument("--comps", nargs="+",
                    default=["learning-agency-lab-automated-essay-scoring-2", "google-quest-challenge"])
    ap.add_argument("--max-kaggle-min", type=float, default=15)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    V = pd.read_csv(args.versions, dtype={"key_id": str})
    V = V[V.has_code]
    runs = pd.DataFrame([json.loads(l) for l in args.results.read_text().splitlines() if l.strip()])
    runs = runs[runs.key_id.notna() & runs.version.notna()]
    ran = set(zip(runs.key_id.astype(str), runs.version.astype(int)))
    ok_kernels = set(runs[runs.status == "OK"].key_id.astype(str))

    todo = V[[(k, int(v)) not in ran for k, v in zip(V.key_id, V.version)]]
    a = todo[todo.key_id.isin(ok_kernels)].assign(stage="A")
    b = todo[~todo.key_id.isin(ok_kernels) & todo.comp.isin(args.comps) & (todo.status == "EASY")].assign(stage="B")
    both = pd.concat([a, b])
    long = both.kaggle_runtime_min > args.max_kaggle_min
    for stage, d in both.groupby("stage"):
        print(f"stage {stage}: {int((~long[d.index]).sum())} to run, {int(long[d.index].sum())} skipped "
              f"(> {args.max_kaggle_min:g} min on Kaggle)")
    out = both[~long].sort_values("kaggle_runtime_min", ascending=False)
    out[["comp", "key_id", "version", "stage", "kaggle_runtime_min"]].to_csv(args.out, sep="\t", index=False, header=False)
    print(f"wrote {args.out}: {len(out)} versions")


if __name__ == "__main__":
    main()

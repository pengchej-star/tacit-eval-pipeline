"""Resources needed to run the best version of each selected expert notebook: triage/top_versions.csv.

For each of Yaqing's 70 kernels (top 10 per paired comp, triage/selection.csv) takes the version with the best
Kaggle score and lists what running it would need, from the static triage in triage/selection_versions.csv:
workload type, GPU, Kaggle runtime, external Kaggle inputs (located or not, and their size where probed), and
the competition data size. Nothing is executed. Prints a per-competition summary.

Kaggle runtimes are from Kaggle's own hardware (P100 / 2xT4, ~30 GB RAM, sessions capped at 12 h). For notebooks
in code competitions, the committed run only sees Kaggle's small public test set, so inference on our MLE-bench
test split takes longer than this number.

Usage:
  python src/top_versions.py
"""

import argparse
from pathlib import Path

import pandas as pd

from runnable_cases import SHORT

REPO = Path(__file__).resolve().parents[1]


def workload(v):
    if v.dl_train:
        return "DL training"
    if v.load_weights:
        return "inference, saved models"
    if v.classical_fit:
        return "classical fit"
    return "blend / other"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selection", type=Path, default=REPO / "triage/selection.csv")
    ap.add_argument("--versions", type=Path, default=REPO / "triage/selection_versions.csv")
    ap.add_argument("--competitions", type=Path, default=REPO / "triage/competitions.csv")
    ap.add_argument("--input-sizes", type=Path, default=REPO / "triage/selection_input_sizes.csv")
    ap.add_argument("--out", type=Path, default=REPO / "triage/top_versions.csv")
    args = ap.parse_args()

    S = pd.read_csv(args.selection, dtype={"key_id": str})
    V = pd.read_csv(args.versions, dtype={"key_id": str}).dropna(subset=["kaggle_score"])
    C = pd.read_csv(args.competitions).set_index("comp")
    size = pd.read_csv(args.input_sizes).dropna(subset=["bytes"]).set_index("spec").bytes

    rows = []
    for s in S.itertuples():
        vs = V[V.key_id == s.key_id]
        higher = C.loc[s.comp, "score_direction"] == "higher"
        v = vs.loc[vs.kaggle_score.idxmax() if higher else vs.kaggle_score.idxmin()]
        located = [x for x in str(v.available_external).split(";") if x and x != "nan"]
        missing = [x for x in str(v.missing_external).split(";") if x and x != "nan"]
        data_gb = C.loc[s.comp, "mlebench_dataset_gb"]
        rows.append({
            "comp": SHORT[s.comp],
            "rank": s.rank,
            "key_id": s.key_id,
            "kernel": v.kernel_ref,
            "tier": s.tier,
            "version": v.version,
            "kaggle_score": v.kaggle_score,
            "kaggle_runtime_min": round(v.kaggle_runtime_min, 1),
            "workload": workload(v),
            "gpu": bool(v.gpu or v.dl_train),
            "internet": bool(v.internet),
            "external_located": len(located),
            "external_missing": len(missing),
            "external_gb_sized": round(sum(size.get(x, 0) for x in located) / 1e9, 1),
            "external_unsized": sum(x not in size for x in located),
            "comp_data_gb": data_gb if pd.notna(data_gb) else C.loc[s.comp, "kaggle_listed_gb"],
            "grader": "mlebench" if C.loc[s.comp, "in_mlebench"] else "none yet",
            "static_status": v.status,
            "kaggle_url": f"https://www.kaggle.com/code/{v.kernel_ref}",
        })
    out = pd.DataFrame(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)

    rt = out.kaggle_runtime_min
    print(f"wrote {args.out}: {len(out)} versions; GPU {int(out.gpu.sum())}, "
          f"all external inputs located {int((out.external_missing == 0).sum())}; "
          f"Kaggle runtime median {rt.median():.0f} min, total {rt.sum() / 60:.0f} h "
          f"(GPU {rt[out.gpu].sum() / 60:.0f} h, CPU {rt[~out.gpu].sum() / 60:.0f} h)")
    print(out.groupby("comp", sort=False).agg(
        gpu=("gpu", "sum"),
        dl_train=("workload", lambda w: int((w == "DL training").sum())),
        median_min=("kaggle_runtime_min", "median"),
        max_min=("kaggle_runtime_min", "max"),
        total_h=("kaggle_runtime_min", lambda r: round(r.sum() / 60, 1)),
        inputs_located=("external_missing", lambda m: int((m == 0).sum())),
        max_external_gb=("external_gb_sized", "max"),
        comp_data_gb=("comp_data_gb", "first"),
    ).to_string())
    print(out.workload.value_counts().to_string())
    bins = pd.cut(rt, [0, 15, 60, 180, 24 * 60], labels=["<15 min", "15-60 min", "1-3 h", ">3 h"])
    print(bins.value_counts(sort=False).to_string())


if __name__ == "__main__":
    main()

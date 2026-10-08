"""Phase 4 prep: statically scan expert versions and rank (key_id, v_k -> v_k+1) cases by ease of running.

Nothing is executed. For each human version with code in the given competitions we record
  - /kaggle/input/<x> (or ../input/<x>) folders it reads; anything other than the comp slug is external
  - training signals: deep-learning training (backward/optimizer.step/Trainer/keras fit) vs classical
    fitting (sklearn/LightGBM/XGBoost/CatBoost .fit / .train)
  - pretrained-weight loading, GPU use, internet use (pip install, wget, requests, HF hub)
  - Kaggle runtime (trajectory.json running_time_ms) and Kaggle public score
Then pairs consecutive versions and keeps pairs where both versions are Kaggle-scored, the code
changed, and neither reads external inputs.

Usage:
  python src/propose_cases.py --traceml-dir /data/user_data/$USER/traceml/hf \
      --human-dir /data/user_data/$USER/traceml/extracted/human \
      --comps google-quest-challenge learning-agency-lab-automated-essay-scoring-2 \
      --features-out /data/user_data/$USER/traceml/version_features.csv --top 15
"""

import argparse
import json
import re
from pathlib import Path

import pandas as pd

INPUT_RE = re.compile(r"""(?:/kaggle/input|\.\./input|\./input)/([A-Za-z0-9_.\-]+)""")
PATTERNS = {
    "dl_train": r"\.backward\(|optimizer\.step\(|\bTrainer\(|trainer\.train\(|\.fit_generator\(|"
                r"model\.fit\(\s*(?:train_dataset|train_ds|train_gen|x_train_tf|dataset)|keras\.callbacks|"
                r"pl\.Trainer|lightning",
    "classical_fit": r"\.fit\(|lgb\.train\(|xgb\.train\(|lightgbm|xgboost|catboost|LGBM|XGB",
    "dl_lib": r"^\s*(?:import|from)\s+(?:torch|tensorflow|keras|transformers|pytorch_lightning|lightning)\b",
    "pretrained_load": r"from_pretrained\(|load_state_dict\(|torch\.load\(|load_model\(|load_weights\(|tensorflow_hub|hub\.KerasLayer",
    "gpu": r"\bcuda\b|\.to\(device\)|torch\.device\(|tf\.distribute|TPUStrategy|\bTPU\b|cupy|cudf|cuml|tree_method\s*=\s*['\"]gpu|device\s*=\s*['\"]gpu",
    "internet": r"^\s*[!%]\s*pip\s+install(?!.*(?:--no-index|/kaggle/input|\.\./input))|wget\s|curl\s|requests\.get\(|urlopen\(|hf_hub_download|snapshot_download",
    "writes_submission": r"submission\.csv",
}
COMPILED = {k: re.compile(v, re.M) for k, v in PATTERNS.items()}


def read_code(path: Path) -> str:
    if path.suffix == ".py":
        return path.read_text(errors="replace")
    nb = json.loads(path.read_text())
    cells = [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]
    return "\n\n".join("".join(c["source"]) if isinstance(c["source"], list) else c["source"] for c in cells)


def code_path(human_dir: Path, key_id: str, v: int):
    for ext in (".ipynb", ".py"):
        p = human_dir / key_id / "versions" / f"v{v:03d}{ext}"
        if p.exists():
            return p
    return None


def scan(code: str, comp: str) -> dict:
    inputs = sorted(set(INPUT_RE.findall(code)))
    external = [x for x in inputs if x != comp]
    feats = {k: bool(r.search(code)) for k, r in COMPILED.items()}
    feats.update(inputs=";".join(inputs), external_inputs=";".join(external), n_external=len(external),
                 code_lines=sum(1 for l in code.splitlines() if l.strip()))
    return feats


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--traceml-dir", type=Path, required=True)
    ap.add_argument("--human-dir", type=Path, required=True)
    ap.add_argument("--comps", nargs="+", required=True)
    ap.add_argument("--features-out", type=Path)
    ap.add_argument("--top", type=int, default=15)
    args = ap.parse_args()

    st = pd.read_parquet(args.traceml_dir / "data/paired/state.parquet",
                         columns=["key_id", "version_number", "comp", "is_agent", "score", "raw_code_path", "group"])
    st = st[~st.is_agent & st.comp.isin(args.comps) & st.raw_code_path.notna()]

    runtime = {}
    for k in st.key_id.unique():
        t = json.loads((args.human_dir / k / "trajectory.json").read_text())
        for v in t["versions"]:
            runtime[(k, v["version_number"])] = v.get("running_time_ms")

    rows, codes = [], {}
    for r in st.itertuples():
        p = code_path(args.human_dir, r.key_id, r.version_number)
        code = read_code(p)
        codes[(r.key_id, r.version_number)] = code
        rows.append({"key_id": r.key_id, "version": r.version_number, "comp": r.comp, "group": r.group,
                     "kaggle_score": r.score, "kaggle_runtime_min": (runtime.get((r.key_id, r.version_number)) or float("nan")) / 60000,
                     "file": str(p), **scan(code, r.comp)})
    F = pd.DataFrame(rows)
    if args.features_out:
        F.to_csv(args.features_out, index=False)
        print(f"wrote {args.features_out} ({len(F)} versions)")

    # light = no DL training, no external inputs, no internet
    F["clean"] = (F.n_external == 0) & ~F.internet
    print("\nper comp:", F.groupby("comp").agg(versions=("key_id", "size"), no_external=("n_external", lambda s: int((s == 0).sum())),
                                               no_dl_train=("dl_train", lambda s: int((~s).sum())),
                                               clean_and_no_dl=("clean", lambda s: int((s & ~F.loc[s.index, "dl_train"]).sum()))).to_string())

    nxt = F.assign(version=F.version - 1)  # row for v_{k+1}, keyed by k
    P = F.merge(nxt, on=["key_id", "version", "comp", "group"], suffixes=("_k", "_k1"))
    P["code_changed"] = [codes[(k, v)] != codes[(k, v + 1)] for k, v in zip(P.key_id, P.version)]
    P = P[P.kaggle_score_k.notna() & P.kaggle_score_k1.notna() & P.code_changed & P.clean_k & P.clean_k1]

    act = pd.read_parquet(args.traceml_dir / "data/paired/action.parquet",
                          columns=["key_id", "v_old", "v_new", "coarse_actions", "goal_nl", "diff_summary", "score_effect"])
    P = P.merge(act, left_on=["key_id", "version"], right_on=["key_id", "v_old"], how="left")

    P["dl_any"] = P.dl_train_k | P.dl_train_k1
    P["gpu_any"] = P.gpu_k | P.gpu_k1
    P["fit_any"] = P.classical_fit_k | P.classical_fit_k1
    P["pretrained_any"] = P.pretrained_load_k | P.pretrained_load_k1
    P["max_runtime_min"] = P[["kaggle_runtime_min_k", "kaggle_runtime_min_k1"]].max(axis=1)
    P["max_lines"] = P[["code_lines_k", "code_lines_k1"]].max(axis=1)
    P = P.sort_values(["dl_any", "gpu_any", "pretrained_any", "max_runtime_min", "max_lines"])
    show = ["comp", "key_id", "version", "kaggle_score_k", "kaggle_score_k1", "kaggle_runtime_min_k", "kaggle_runtime_min_k1",
            "dl_any", "gpu_any", "fit_any", "pretrained_any", "max_lines", "inputs_k", "coarse_actions", "diff_summary"]
    pd.set_option("display.width", 300); pd.set_option("display.max_colwidth", 140)
    print(f"\neligible pairs: {len(P)}  (by comp: {P.comp.value_counts().to_dict()})")
    print(P[show].head(args.top).to_string(index=False))


if __name__ == "__main__":
    main()

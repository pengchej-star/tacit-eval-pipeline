"""One table of the agent-vs-expert pivot cases we ran end to end, for handing over to the team.

Reads the agent outputs in results/agent_pilot/<case>/ (meta.json), the agent grades in results/agent_runs.jsonl
and the expert runs in results/runs.jsonl. Writes handoff/pivots.csv: one row per pivot (key_id, v_k -> v_k+1),
with the kernel, Kaggle links to both exact versions, expert and agent scores on our split, Kaggle's scores,
the agent's cost, the inputs and environment used, and where the code is.

Usage:
  python src/handoff_pivots.py
"""

import argparse
import getpass
import json
from pathlib import Path

import pandas as pd

USER_DATA = Path("/data/user_data") / getpass.getuser()
REPO = Path(__file__).resolve().parents[1]
SHORT = {"learning-agency-lab-automated-essay-scoring-2": "aes2", "google-quest-challenge": "gquest",
         "hms-harmful-brain-activity-classification": "hms", "ranzcr-clip-catheter-line-classification": "ranzcr",
         "amex-default-prediction": "amex", "commonlitreadabilityprize": "commonlit",
         "equity-post-hct-survival-predictions": "equity"}
# Whether the notebook trains its model on our train split, or loads weights trained on all of Kaggle's train set
# (which contains our test rows: leakage). Read off each case's code.
MODEL_SOURCE = {"49981285": "trained in notebook", "54551628": "trained in notebook",
                "73937748": "trained in notebook", "13848868": "attached weights", "15173072": "attached weights",
                "15164527": "attached weights", "49524919": "attached weights"}


def rows(path):
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def specs(run):
    return ";".join(x["spec"] for x in run.get("external_inputs") or [])


def patches(run):
    return ";".join(p["name"] for p in run.get("patches_applied") or [])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--traceml-dir", type=Path, default=USER_DATA / "traceml/hf")
    ap.add_argument("--out", type=Path, default=REPO / "handoff/pivots.csv")
    args = ap.parse_args()

    expert = {}  # (key_id, version) -> latest OK run
    for r in sorted(rows(REPO / "results/runs.jsonl"), key=lambda r: r["timestamp"]):
        if r["status"] == "OK" and r.get("key_id"):
            expert[(str(r["key_id"]), int(r["version"]))] = r
    agent = {Path(r["code_file"]).parent.name: r for r in rows(REPO / "results/agent_runs.jsonl")}

    kern = pd.read_parquet(args.traceml_dir / "extras/kernels.parquet",
                           columns=["kernel_id", "kernel_slug", "author_username", "author_tier"])
    kern = kern.assign(key_id=kern.kernel_id.astype(str)).set_index("key_id")
    state = pd.read_parquet(args.traceml_dir / "data/paired/state.parquet",
                            columns=["key_id", "version_number", "version_id"])
    version_id = {(str(k), int(v)): int(i) for k, v, i in zip(state.key_id, state.version_number, state.version_id)
                  if pd.notna(i)}
    comps = json.loads((args.traceml_dir / "manifests/competitions.json").read_text())

    out = []
    for case in sorted((REPO / "results/agent_pilot").iterdir()):
        meta = json.loads((case / "meta.json").read_text())
        key, comp, vk = str(meta["key_id"]), meta["comp"], int(meta["v_k"])
        a, b, g = expert[(key, vk)], expert[(key, vk + 1)], agent[meta["run_id"]]
        higher = comps[comp]["score_direction"] == "higher"
        slug = kern.kernel_slug[key]
        diff = (g["score"] - b["score"]) * (1 if higher else -1)
        out.append({
            "comp": SHORT[comp],
            "key_id": key,
            "kernel": slug,
            "author_tier": kern.author_tier[key],
            "v_k": vk,
            "v_k1": vk + 1,
            "metric": comps[comp].get("metric", ""),
            "higher_is_better": higher,
            "model_source": MODEL_SOURCE[key],
            "score_expert_v_k": a["score"],
            "score_expert_v_k1": b["score"],
            "score_agent_v_k1": g["score"],
            "agent_minus_expert": round(diff, 5),
            "kaggle_score_v_k": a.get("kaggle_score"),
            "kaggle_score_v_k1": b.get("kaggle_score"),
            "agent_model": meta["model"],
            "agent_minutes": round(meta["agent_s"] / 60, 1),
            "agent_cost_usd": round(meta["cost_usd_reported"], 2),
            "agent_turns": meta["num_turns"],
            "runtime_s_v_k": a["runtime_s"],
            "runtime_s_v_k1": b["runtime_s"],
            "runtime_s_agent": g["runtime_s"],
            "external_inputs": specs(b) or specs(a),
            "external_inputs_agent": specs(g),
            "run_env": Path(b["run_env"]).name,
            "patches": ";".join(sorted({p for r in (a, b, g) for p in patches(r).split(";") if p})),
            "kaggle_url_v_k": f"https://www.kaggle.com/code/{slug}?scriptVersionId={version_id[(key, vk)]}",
            "kaggle_url_v_k1": f"https://www.kaggle.com/code/{slug}?scriptVersionId={version_id[(key, vk + 1)]}",
            "expert_code": f"trajectories_human.tar.gz: human/{key}/versions/v{vk:03d}.ipynb, v{vk + 1:03d}.ipynb",
            "agent_dir": str(case.relative_to(REPO)),
            "expert_run_ids": f"{a['run_id']};{b['run_id']}",
            "agent_run_id": g["run_id"],
        })
    df = pd.DataFrame(out).sort_values(["model_source", "comp", "key_id"], ascending=[False, True, True])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"wrote {args.out}: {len(df)} pivots")
    print(df[["comp", "key_id", "kernel", "author_tier", "v_k", "v_k1", "model_source", "score_expert_v_k",
              "score_expert_v_k1", "score_agent_v_k1", "kaggle_score_v_k", "kaggle_score_v_k1",
              "agent_cost_usd"]].to_string(index=False))


if __name__ == "__main__":
    main()

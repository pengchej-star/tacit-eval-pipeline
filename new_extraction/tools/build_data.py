"""How data/ was derived from the raw sources (only needed to rebuild it; the repository ships the result).

    python tools/build_data.py --selection <selection.csv> --episode-items <episode_items.jsonl> \\
        --actions <TraceML data/paired/action.parquet> --trajectories <TraceML human trajectories dir> --comps <competitions.json>

Writes data/selection.csv, data/episode_items.jsonl (restricted to the selected experts), data/actions.parquet (version transitions of the
selected human experts) and data/scores.json ({kernel id: {version: public leaderboard score}}).
"""
import argparse, json, shutil
from pathlib import Path

import pandas as pd

ap = argparse.ArgumentParser()
for k in ("selection", "episode-items", "actions", "trajectories"):
    ap.add_argument("--" + k, required=True)
a = ap.parse_args()
out = Path(__file__).resolve().parent.parent / "data"
out.mkdir(exist_ok=True)
sel = pd.read_csv(a.selection, dtype={"key_id": str})
keys = set(sel.key_id)
shutil.copy(a.selection, out / "selection.csv")
with open(a.episode_items, encoding="utf-8") as f, open(out / "episode_items.jsonl", "w", encoding="utf-8") as g:
    for l in f:
        if json.loads(l)["key_id"] in keys:
            g.write(l)
act = pd.read_parquet(a.actions)
act["key_id"] = act.key_id.astype(str)
act = act[(~act.is_agent) & act.key_id.isin(keys)]
act[["key_id", "comp", "group", "v_old", "v_new", "coarse_actions", "fine_actions", "magnitude", "goal_nl", "diff_summary", "score_old", "score_new", "edge_kind"]] \
    .to_parquet(out / "actions.parquet", index=False)
scores = {}
for k in keys:
    t = json.load(open(Path(a.trajectories) / k / "trajectory.json", encoding="utf-8"))
    scores[k] = {str(v["version_number"]): (v.get("linked_score") or {}).get("public") for v in t["versions"]}
json.dump(scores, open(out / "scores.json", "w"))
print(f"{len(keys)} experts, {len(act)} transitions, scores for {len(scores)} kernels")

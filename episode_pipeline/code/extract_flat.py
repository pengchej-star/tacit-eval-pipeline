"""Run the flat instance/general EPISODE_EXTRACT_SYSTEM over episodes (default: the 70 selected experts in results/selection.csv).

    python extract_flat.py                                  # all 70 -> ../results/episode_items.{jsonl,md}  (resumable)
    python extract_flat.py --kernels 13848868 --out ../results/x

Runs from the episode_pipeline copy but uses the root data layer in arxived/extraction_zheyuan (action.parquet, notebooks).
"""
import importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_DIR = HERE.parents[1] / "arxived" / "extraction_zheyuan"
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location("data", ROOT_DIR / "data.py")
sys.modules["data"] = root = importlib.util.module_from_spec(spec); spec.loader.exec_module(root)

from dotenv import load_dotenv
load_dotenv(HERE.parents[1] / ".env")
import episode_extract as E
from llm import call_model, parse_json, pmap_jsonl
from prompts import EPISODE_EXTRACT_SYSTEM

import argparse, functools
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--kernels", nargs="*")
ap.add_argument("--out", default=str(HERE.parent / "results" / "episode_items"))
ap.add_argument("--workers", type=int, default=6)
a = ap.parse_args()

E.ACT = root.load_actions()
kernels = set(a.kernels) if a.kernels else set(pd.read_csv(HERE.parent / "results" / "selection.csv").key_id.astype(str))
recs = [json.loads(l) for l in open(HERE.parent / "results" / "episodes.jsonl", encoding="utf-8")]
jobs = E.jobs_from(recs, kernels)


@functools.lru_cache(maxsize=None)
def traj(k):
    return root.annotate_trajectory(root.trajectory(E.ACT, k))


def run(job):
    k = job["key_id"]
    p = E.prompt(job, traj(k), job["comp"], job["tier"])
    try:
        out = parse_json(call_model(EPISODE_EXTRACT_SYSTEM, p, model=E.MODEL, temperature=0, max_tokens=E.MAX_TOKENS))
    except Exception as e:
        out = {"_error": repr(e)}
    valid = set(job["step_ids"])
    for it in out.get("items") or []:
        ms = [E.re.search(r"v?(\d+)\s*(?:->|→|-|to)\s*v?(\d+)", str(s)) for s in it.get("steps") or []]
        it["steps"] = [f"{k}:{m.group(1)}->{m.group(2)}" for m in ms if m and f"{k}:{m.group(1)}->{m.group(2)}" in valid]
    return dict(ep_id=job["ep_id"], key_id=k, comp=job["comp"], tier=job["tier"],
                episode={x: job[x] for x in ("start_v", "end_v", "objective", "lever", "pattern", "outcome", "n_transitions", "n_scored")},
                items=out.get("items") or [], error=out.get("_error"), raw=out.get("_raw"), model=E.MODEL)


out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
res = pmap_jsonl(jobs, run, out.with_suffix(".jsonl"), key=lambda r: r["ep_id"], workers=a.workers, desc="extract_flat")
md = [f"# Episode-level knowledge items (instance + general)\n\nModel: {E.MODEL}; {len(res)} episodes from {len({r['key_id'] for r in res})} kernels\n"]
for r in res:
    e = r["episode"]
    md.append(f"## {r['ep_id']}  v{e['start_v']}-v{e['end_v']}  ({r['comp']}, {r['tier']}; {e['pattern']}; {e['n_transitions']} transitions)\n\n- Objective: {e['objective']}\n- Lever: {e['lever']}\n- Outcome: {e['outcome']}\n")
    if r["error"] or r["raw"]:
        md.append(f"```\n{r['error'] or str(r['raw'])[:500]}\n```\n"); continue
    for i, it in enumerate(r["items"], 1):
        x, g = it.get("instance", {}), it.get("general", {})
        md.append(f"### {r['ep_id']}#{i}  (steps: {', '.join(it.get('steps') or [])})\n\n**Instance**\n- Goal: {x.get('goal')}\n- Context: {x.get('context')}\n- Action: {x.get('action')}\n\n"
                  f"**General**\n- Goal: {g.get('goal')}\n- Context: {g.get('context')}\n- Action: {g.get('action')}\n")
    if not r["items"]:
        md.append("(no items)\n")
out.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
print(len(res), "episodes,", sum(len(r["items"]) for r in res), "items,", sum(1 for r in res if r["error"] or r["raw"]), "errors ->", out.with_suffix(".md"))

"""Build the working directory for the attention-map agent (method 2 for steps 5-8). Usage: python prep_attention.py codex <workdir>
Contents: tree.json, desiderata.json (check ids), jobs.jsonl (one line per edit, everything needed to judge it), transitions.json, competitions.json."""
import json, os, sys
from pathlib import Path

agent, work = sys.argv[1], Path(sys.argv[2])
HERE = Path(__file__).resolve().parent
os.environ["NE_SUFFIX"] = f"_agent_{agent}"
sys.path.insert(0, str(HERE.parent))
import data, visits                         # noqa: E402
from common import CFG, OUT, TASKS, jload   # noqa: E402

tree, dd, items, trans = (jload(OUT / f) for f in ("3_merged_tree.json", "4_desiderata.json", "2a_items.json", "trans.json"))
ctx = visits.Ctx(trans, items, tree, dd)
jobs = visits.make_jobs(ctx, trans)

def drop(n):
    n = {k: v for k, v in n.items() if k not in ("all_items", "experts", "comps", "actions", "n_edits", "depth")}
    n["children"] = [drop(c) for c in n["children"]]
    return n
work.mkdir(parents=True, exist_ok=True)
json.dump(drop(tree), open(work / "tree.json", "w"), indent=1)
json.dump({"checks": dd["registry"] and {e: dict(check=r["check"], how=r["how"]) for e, r in dd["registry"].items()},
           "nodes": {nid: {"groups": d["groups"], "guessed_pushes": {e: c["guessed_pushes"] for e, c in d["checks"].items()}} for nid, d in dd["nodes"].items()}},
          open(work / "desiderata.json", "w"), indent=1)
json.dump(trans, open(work / "transitions.json", "w"))
json.dump({c: dict(direction=t["direction"], description=t["description"].strip()) for c, t in TASKS.items()}, open(work / "competitions.json", "w"), indent=1)
by_id = {i["id"]: i for i in items}
with open(work / "jobs.jsonl", "w") as f:
    for r, hist, its in jobs:
        rec = dict(step_id=r["step_id"], comp=r["comp"], expert=r["key_id"], tier=r["tier"], seq=r["v_old"],
                   magnitude=r["magnitude"], labels=r["fine"] or r["coarse"], goal=r["goal"], change_summary=r["change"] or r["goal"],
                   score_before=r["score_old"], earlier_edits=hist, items=[])
        for it in its:
            walk = []
            for a, b in ctx.walk_for(it):
                kids = {y["id"] for y in a["children"]}
                tried = sorted({x["id"] for r2 in ctx.ex[r["key_id"]] if r2["v_new"] <= r["v_old"] for i2 in ctx.by_step.get(r2["step_id"], [])
                                if i2["id"] in ctx.term for x in ctx.paths[ctx.term[i2["id"]]] if x["id"] in kids})
                walk.append(dict(node=a["id"], name=a["name"], decision=a.get("decision", ""), options=[dict(id=c["id"], name=c["name"]) for c in a["children"]],
                                 taken=b["id"], taken_earlier_by_this_expert=tried, checks=list(ctx.nodes_d[a["id"]]["checks"])))
            rec["items"].append(dict(item=it["id"], what=it["what"], why=it["why"], walk=walk))
        f.write(json.dumps(rec) + "\n")
print(f"{work}: {len(jobs)} edits, {sum(len(j[2]) for j in jobs)} items, {len(dd['nodes'])} decision nodes")
